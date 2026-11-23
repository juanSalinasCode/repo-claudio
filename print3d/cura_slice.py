#!/usr/bin/env python3
"""Lamina un STL con CuraEngine (sin GUI) resolviendo los perfiles igual que Cura.

CuraEngine por sí solo no evalúa las fórmulas de los .def.json ni aplica
perfiles de calidad/material. Este script reproduce la pila de Cura:

    fdmprinter -> creality_base -> creality_ender3v2neo (máquina)
    fdmextruder -> creality_base_extruder_0              (extrusor)
    variante de boquilla -> material (XML) -> calidad material -> calidad global
    -> ajustes del usuario (-s clave=valor)

y pasa todos los valores ya resueltos a CuraEngine.

Uso:
    cura_slice.py modelo.stl -o salida.gcode [--material PLA|PETG|ABS|TPU]
                  [--quality standard|super|low|adaptive|draft|ultra]
                  [-s infill_sparse_density=20 -s support_enable=True ...]
                  [--dump-settings ajustes.json]
"""
import argparse, ast, json, math, os, re, subprocess, sys
import xml.etree.ElementTree as ET
from configparser import ConfigParser

CURA = os.environ.get("CURA_DIR", "/opt/3d/cura")
RES = os.path.join(CURA, "share/cura/resources")
DEF_DIR = os.path.join(RES, "definitions")
EXT_DIR = os.path.join(RES, "extruders")

MATERIAL_XML_MAP = {
    "print temperature": "material_print_temperature",
    "heated bed temperature": "material_bed_temperature",
    "standby temperature": "material_standby_temperature",
    "print cooling": "cool_fan_speed",
    "retraction amount": "retraction_amount",
    "retraction speed": "retraction_speed",
}


def load_def(name, folder):
    path = os.path.join(folder, name + ".def.json")
    return json.load(open(path, encoding="utf-8"))


def flatten(settings, out):
    for key, props in settings.items():
        children = props.get("children")
        if props.get("type") != "category":
            out[key] = {k: v for k, v in props.items() if k != "children"}
        if children:
            flatten(children, out)


def load_chain(name, folder):
    """Devuelve (settings, metadata) resolviendo 'inherits'."""
    d = load_def(name, folder if os.path.exists(os.path.join(folder, name + ".def.json")) else DEF_DIR)
    if "inherits" in d:
        settings, meta = load_chain(d["inherits"], DEF_DIR)
    else:
        settings, meta = {}, {}
    if "settings" in d:
        flatten(d["settings"], settings)
    for key, ov in d.get("overrides", {}).items():
        settings.setdefault(key, {}).update(ov)
    meta = {**meta, **d.get("metadata", {})}
    return settings, meta


def read_cfg(path):
    cp = ConfigParser(interpolation=None)
    cp.optionxform = str
    cp.read(path, encoding="utf-8")
    return dict(cp["values"]) if cp.has_section("values") else {}


def read_material(path):
    ns = {"m": "http://www.ultimaker.com/material"}
    root = ET.parse(path).getroot()
    vals = {}
    settings = root.find("m:settings", ns)
    for s in settings.findall("m:setting", ns):
        k = MATERIAL_XML_MAP.get(s.get("key"))
        if k:
            vals[k] = s.text.strip()
    return vals


START_GCODE = """; --- Ender 3 V2 Neo (CR Touch) ---
M140 S{material_bed_temperature_layer_0} ; calentar cama
M104 S150 ; precalentar boquilla sin gotear
G92 E0
G28 ; home
M190 S{material_bed_temperature_layer_0} ; esperar cama
G29 ; malla CR Touch
M109 S{material_print_temperature_layer_0} ; esperar boquilla
G1 Z2.0 F3000
G1 X10.1 Y20 Z0.28 F5000.0
G1 X10.1 Y200.0 Z0.28 F1500.0 E15 ; linea de purga 1
G1 X10.4 Y200.0 Z0.28 F5000.0
G1 X10.4 Y20 Z0.28 F1500.0 E30 ; linea de purga 2
G92 E0
G1 Z2.0 F3000"""

ENDER_FIXES = {
    "machine_width": "220",       # el perfil de Cura dice 230 (error conocido)
    "machine_depth": "220",
    "machine_start_gcode": START_GCODE,
}

MATERIAL_TUNING = {   # valores de partida para Bowden; calibrar con torres
    "PLA": {"retraction_amount": "5", "retraction_speed": "45",
            "material_print_temperature": "205", "material_bed_temperature": "60"},
    "PETG": {"retraction_amount": "5", "retraction_speed": "35",
             "material_print_temperature": "235", "material_bed_temperature": "75",
             "cool_fan_speed": "40"},
}


def fill_tokens(text, r):
    return re.sub(r"\{(\w+)\}", lambda m: str(r.get(m.group(1))) if m.group(1) in r.d else m.group(0), text)


class Resolver:
    def __init__(self, definition, layers):
        self.d = definition          # key -> props
        self.layers = layers         # lista de dicts (de menor a mayor prioridad), valores str
        self.cache = {}
        self.stack = set()

    def convert(self, key, v):
        t = self.d.get(key, {}).get("type")
        if not isinstance(v, str):
            return v
        try:
            if t == "float":
                return float(v)
            if t == "int":
                return int(float(v))
            if t == "bool":
                return v.strip().lower() in ("true", "1", "yes")
            if t in ("[int]", "polygon", "polygons", "vec3"):
                return ast.literal_eval(v)
            if t in ("extruder", "optional_extruder"):
                return str(v)
        except Exception:
            pass
        return v

    def eval_expr(self, expr):
        tree = ast.parse(expr, mode="eval")
        names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
        env = dict(self.funcs())
        for n in names:
            if n in self.d and n not in env:
                env[n] = self.get(n)
        return eval(compile(tree, "<expr>", "eval"), env)

    def funcs(self):
        g = self.get
        return {
            "math": math, "max": max, "min": min, "round": round, "sum": sum,
            "len": len, "float": float, "int": int, "all": all, "any": any,
            "map": map, "abs": abs, "str": str, "bool": bool, "list": list,
            "extruderValue": lambda e, k: g(k),
            "extruderValues": lambda k: [g(k)],
            "resolveOrValue": lambda k: g(k),
            "anyExtruderWithMaterial": lambda k: 0,
            "anyExtruderNrWithOrDefault": lambda k: 0,
            "defaultExtruderPosition": lambda: "0",
            "valueFromContainer": lambda k, i: g(k),
            "valueFromExtruderContainer": lambda k, i: g(k),
            "__builtins__": {},
        }

    def get(self, key):
        if key in self.cache:
            return self.cache[key]
        if key in self.stack:
            raise RecursionError(key)
        self.stack.add(key)
        try:
            raw = None
            for layer in reversed(self.layers):
                if key in layer:
                    raw = layer[key]
                    break
            props = self.d.get(key, {})
            if raw is not None:
                if isinstance(raw, str) and raw.startswith("="):
                    val = self.eval_expr(raw[1:])
                else:
                    val = self.convert(key, raw)
            elif "value" in props:
                v = props["value"]
                val = self.eval_expr(v) if isinstance(v, str) else v
            else:
                val = props.get("default_value")
            val = self.convert(key, val) if isinstance(val, str) and props.get("type") not in ("str", "enum") else val
            self.cache[key] = val
            return val
        finally:
            self.stack.discard(key)


def to_engine_str(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, float) and v.is_integer():
        return str(v)
    return str(v)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("models", nargs="+")
    ap.add_argument("-o", "--output", required=True)
    ap.add_argument("--machine", default="creality_ender3v2neo")
    ap.add_argument("--nozzle", default="0.4")
    ap.add_argument("--material", default="PLA")
    ap.add_argument("--quality", default="standard")
    ap.add_argument("-s", "--set", action="append", default=[], metavar="KEY=VALUE")
    ap.add_argument("--dump-settings")
    ap.add_argument("--stock", action="store_true", help="perfil de Cura sin mis correcciones")
    ap.add_argument("--no-g29", action="store_true", help="usar M420 S1 (malla guardada) en vez de G29")
    a = ap.parse_args()

    machine, mmeta = load_chain(a.machine, DEF_DIR)
    ext_name = mmeta["machine_extruder_trains"]["0"]
    extruder, _ = load_chain(ext_name, EXT_DIR)
    definition = {**machine}
    for k, v in extruder.items():
        definition.setdefault(k, {}).update(v)

    qdef = mmeta.get("quality_definition", a.machine)
    vendor = "creality"
    layers = []
    variant = os.path.join(RES, "variants", vendor, f"{a.machine}_{a.nozzle}.inst.cfg")
    if os.path.exists(variant):
        layers.append(read_cfg(variant))
    mat = os.path.join(RES, "materials", f"generic_{a.material.lower()}_175.xml.fdm_material")
    if os.path.exists(mat):
        layers.append(read_material(mat))
    qbase = qdef.split("_")[-1] if qdef.startswith(vendor) else qdef
    qdir = os.path.join(RES, "quality", vendor, qbase)
    qmat = os.path.join(qdir, f"{qbase}_{a.nozzle}_{a.material.upper()}_{a.quality}.inst.cfg")
    qglob = os.path.join(qdir, f"{qbase}_global_{a.quality}.inst.cfg")
    for q in (qglob, qmat):  # calidad global < calidad de material (Cura: quality del extrusor gana)
        if os.path.exists(q):
            layers.append(read_cfg(q))
        else:
            print(f"aviso: no existe el perfil {q}", file=sys.stderr)
    # Correcciones propias para la Ender 3 V2 Neo (ver print3d/README.md)
    mine = dict(ENDER_FIXES) if a.machine == "creality_ender3v2neo" and not a.stock else {}
    mine.update(MATERIAL_TUNING.get(a.material.upper(), {}) if not a.stock else {})
    if a.no_g29:
        mine["machine_start_gcode"] = mine.get("machine_start_gcode", "").replace(
            "G29 ; malla CR Touch", "M420 S1 ; cargar malla guardada")
    layers.append(mine)
    user = {}
    for kv in a.set:
        k, v = kv.split("=", 1)
        if k not in definition:
            sys.exit(f"ajuste desconocido: {k}")
        user[k] = v
    layers.append(user)

    r = Resolver(definition, layers)
    resolved, errors = {}, {}
    for key, props in definition.items():
        if props.get("type") == "category":
            continue
        try:
            resolved[key] = r.get(key)
        except Exception as e:  # noqa
            errors[key] = repr(e)
    for k in ("machine_start_gcode", "machine_end_gcode"):
        if isinstance(resolved.get(k), str):
            resolved[k] = fill_tokens(resolved[k], r)
    # Igual que StartSliceJob de Cura: no anteponer calentamiento si el start G-code ya lo hace
    sg = resolved.get("machine_start_gcode") or ""
    resolved["material_bed_temp_prepend"] = not any(c in sg for c in ("M140", "M190"))
    resolved["material_bed_temp_wait"] = "M190" not in sg
    resolved["material_print_temp_prepend"] = not any(c in sg for c in ("M104", "M109"))
    resolved["material_print_temp_wait"] = "M109" not in sg
    if errors:
        print(f"aviso: {len(errors)} ajustes sin resolver: {list(errors)[:10]}", file=sys.stderr)

    if a.dump_settings:
        json.dump(resolved, open(a.dump_settings, "w"), indent=1, default=str)

    env = dict(os.environ)
    env["CURA_ENGINE_SEARCH_PATH"] = f"{DEF_DIR}:{EXT_DIR}"
    env["LD_LIBRARY_PATH"] = CURA + (":" + env["LD_LIBRARY_PATH"] if env.get("LD_LIBRARY_PATH") else "")
    sets = []
    for k, v in resolved.items():
        if v is None:
            continue
        sets += ["-s", f"{k}={to_engine_str(v)}"]
    cmd = ["/lib64/ld-linux-x86-64.so.2", os.path.join(CURA, "CuraEngine"), "slice",
           "-j", os.path.join(DEF_DIR, a.machine + ".def.json")] + sets + ["-e0"] + sets
    for m in a.models:
        cmd += ["-l", os.path.abspath(m)]
    cmd += ["-o", os.path.abspath(a.output)]
    p = subprocess.run(cmd, env=env, capture_output=True, text=True)
    log = p.stdout + p.stderr
    errs = [l for l in log.splitlines() if "[error]" in l]
    if p.returncode != 0 or not os.path.exists(a.output):
        print(log[-3000:], file=sys.stderr)
        sys.exit(p.returncode or 1)
    for l in errs[:5]:
        print(l, file=sys.stderr)
    # Resumen
    head = open(a.output, encoding="utf-8", errors="ignore").read(4000)
    t = re.search(r";TIME:(\d+)", head)
    f = re.search(r";Filament used: ([\d.]+)m", head)
    print(f"OK -> {a.output}")
    print(f"  material={a.material} calidad={a.quality} capa={resolved.get('layer_height')} mm "
          f"relleno={resolved.get('infill_sparse_density')}% soporte={resolved.get('support_enable')} "
          f"adhesión={resolved.get('adhesion_type')}")
    print(f"  temp boquilla={resolved.get('material_print_temperature_layer_0')}/{resolved.get('material_print_temperature')} °C "
          f"cama={resolved.get('material_bed_temperature')} °C")
    if t:
        s = int(t.group(1)); print(f"  tiempo estimado: {s//3600} h {s%3600//60} min")
    if f:
        print(f"  filamento: {float(f.group(1)):.2f} m (~{float(f.group(1))*2.98:.0f} g PLA)")


if __name__ == "__main__":
    main()
