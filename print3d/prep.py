#!/opt/3d/venv/bin/python
"""Prepara un STL para imprimir en la Ender 3 V2 Neo usando Blender (bpy 5.x) sin GUI.

Pasos (en este orden, todos opcionales salvo análisis/ubicación):
  1. importar STL/OBJ/3MF(*)       5. reparar (merge by distance, normales, rellenar agujeros)
  2. escalar (--scale / --fit)     6. apoyar en Z=0 y centrar en la cama
  3. rotar (--rotate X,Y,Z grados) 7. comprobar que entra en 220x220x250
  4. auto-orientar (--orient)      8. exportar STL + vista previa PNG + informe JSON

(*) 3MF vía trimesh.

Ejemplos:
  prep.py pieza.stl -o pieza_lista.stl --rotate 90,0,0 --preview pieza.png
  prep.py pieza.stl -o pieza_lista.stl --scale 1.5 --repair
  prep.py pieza.stl -o pieza_lista.stl --fit 200          # lado mayor = 200 mm
  prep.py pieza.stl -o pieza_lista.stl --orient            # cara plana mayor abajo
  prep.py pieza.stl --info                                 # solo analizar
  prep.py pieza.stl -o out.stl --script mis_cambios.py     # ejecuta un script bpy extra
                                                           # (recibe la variable `obj`)
"""
import argparse, json, math, os, sys

import bpy
import bmesh
import mathutils
import numpy as np

BED = (220.0, 220.0, 250.0)   # volumen real de la Ender 3 V2 Neo (mm)


def log(*a):
    print(*a, flush=True)


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def import_mesh(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".stl":
        bpy.ops.wm.stl_import(filepath=path)
    elif ext == ".obj":
        bpy.ops.wm.obj_import(filepath=path)
    elif ext in (".3mf", ".ply", ".off", ".glb", ".gltf"):
        import trimesh
        m = trimesh.load(path, force="mesh")
        me = bpy.data.meshes.new(os.path.basename(path))
        me.from_pydata(m.vertices.tolist(), [], m.faces.tolist())
        ob = bpy.data.objects.new(me.name, me)
        bpy.context.scene.collection.objects.link(ob)
        ob.select_set(True)
        bpy.context.view_layer.objects.active = ob
    else:
        sys.exit(f"formato no soportado: {ext}")
    objs = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    if len(objs) > 1:
        bpy.context.view_layer.objects.active = objs[0]
        for o in objs:
            o.select_set(True)
        bpy.ops.object.join()
    obj = bpy.context.view_layer.objects.active or objs[0]
    return obj


def apply_transform(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)


def world_bbox(obj):
    v = np.array([obj.matrix_world @ x.co for x in obj.data.vertices])
    return v.min(0), v.max(0)


def analyze(obj):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.transform(obj.matrix_world)
    non_manifold = sum(1 for e in bm.edges if not e.is_manifold)
    boundary = sum(1 for e in bm.edges if e.is_boundary)
    vol = bm.calc_volume(signed=True)
    area = sum(f.calc_area() for f in bm.faces)
    # voladizos: caras cuya normal apunta hacia abajo más de 45°
    down = mathutils.Vector((0, 0, -1))
    over_area = sum(f.calc_area() for f in bm.faces
                    if f.normal.angle(down, 0) < math.radians(45) and f.calc_center_median().z > 0.3)
    bm.free()
    mn, mx = world_bbox(obj)
    size = mx - mn
    return {
        "triangulos": len(obj.data.polygons),
        "dimensiones_mm": [round(float(x), 2) for x in size],
        "volumen_cm3": round(abs(vol) / 1000, 2),
        "peso_pla_100pct_g": round(abs(vol) / 1000 * 1.24, 1),
        "area_cm2": round(area / 100, 1),
        "aristas_no_manifold": non_manifold,
        "aristas_borde_abiertas": boundary,
        "estanca": non_manifold == 0,
        "normales_invertidas": vol < 0,
        "area_voladizos_cm2": round(over_area / 100, 1),
        "entra_en_cama": bool(all(size[i] <= BED[i] - (10 if i < 2 else 0) for i in range(3))),
    }


def repair(obj, merge_dist=0.0001):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=merge_dist)
    loose = [v for v in bm.verts if not v.link_edges]
    bmesh.ops.delete(bm, geom=loose, context="VERTS")
    degenerate = [f for f in bm.faces if f.calc_area() < 1e-10]
    bmesh.ops.delete(bm, geom=degenerate, context="FACES")
    edges = [e for e in bm.edges if e.is_boundary]
    if edges:
        bmesh.ops.holes_fill(bm, edges=edges, sides=0)
    bmesh.ops.triangulate(bm, faces=bm.faces)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.update()


def auto_orient(obj):
    """Apoya la pieza sobre su pose estable más probable (trimesh)."""
    import trimesh
    v = np.array([x.co for x in obj.data.vertices])
    f = np.array([p.vertices[:] for p in obj.data.polygons])
    m = trimesh.Trimesh(v, f, process=True)
    tfs, probs = trimesh.poses.compute_stable_poses(m, n_samples=1)
    if len(tfs):
        obj.matrix_world = mathutils.Matrix(tfs[0].tolist()) @ obj.matrix_world
        apply_transform(obj)
        return float(probs[0])
    return None


def place_on_bed(obj):
    mn, mx = world_bbox(obj)
    c = (mn + mx) / 2
    obj.location.x -= c[0]
    obj.location.y -= c[1]
    obj.location.z -= mn[2]
    apply_transform(obj)


def render_preview(obj, path, size=900):
    sc = bpy.context.scene
    mn, mx = world_bbox(obj)
    dim = mx - mn
    # cama
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, -0.01))
    bed = bpy.context.active_object
    bed.scale = (BED[0], BED[1], 1)
    mat = bpy.data.materials.new("bed")
    mat.diffuse_color = (0.15, 0.15, 0.17, 1)
    bed.data.materials.append(mat)
    m2 = bpy.data.materials.new("pieza")
    m2.diffuse_color = (0.95, 0.55, 0.15, 1)
    obj.data.materials.clear()
    obj.data.materials.append(m2)
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
    sc.collection.objects.link(cam)
    sc.camera = cam
    r = max(float(np.linalg.norm(dim)), 40.0) * 1.15
    target = mathutils.Vector((0, 0, float(dim[2]) / 2))
    cam.location = target + mathutils.Vector((r * 0.75, -r * 0.95, r * 0.7))
    cam.rotation_euler = (target - cam.location).to_track_quat("-Z", "Y").to_euler()
    cam.data.lens = 50
    cam.data.clip_end = 10000
    sc.render.engine = "BLENDER_WORKBENCH"
    sh = sc.display.shading
    sh.light = "STUDIO"
    sh.color_type = "MATERIAL"
    sh.show_cavity = True
    sh.show_shadows = True
    sc.render.resolution_x = sc.render.resolution_y = size
    sc.render.film_transparent = False
    sc.world = sc.world or bpy.data.worlds.new("w")
    sc.render.filepath = os.path.abspath(path)
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(bed)
    bpy.data.objects.remove(cam)


def main():
    argv = sys.argv[1:]
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input")
    ap.add_argument("-o", "--output")
    ap.add_argument("--info", action="store_true", help="solo analizar")
    ap.add_argument("--scale", type=float)
    ap.add_argument("--fit", type=float, help="escalar para que el lado mayor mida N mm")
    ap.add_argument("--units", choices=["mm", "cm", "m", "in"], default="mm",
                    help="unidades del archivo de entrada")
    ap.add_argument("--rotate", help="X,Y,Z en grados")
    ap.add_argument("--mirror", choices=["x", "y", "z"])
    ap.add_argument("--orient", action="store_true", help="auto-orientar sobre la pose más estable")
    ap.add_argument("--repair", action="store_true")
    ap.add_argument("--script", help="script bpy extra; recibe `obj`, `bpy`, `bmesh`, `mathutils`")
    ap.add_argument("--preview", help="PNG de vista previa sobre la cama")
    ap.add_argument("--report", help="guardar informe JSON")
    a = ap.parse_args(argv)

    reset()
    obj = import_mesh(os.path.abspath(a.input))
    apply_transform(obj)
    info = {"entrada": a.input, "antes": analyze(obj)}
    log(json.dumps(info["antes"], ensure_ascii=False))
    if a.info and not a.output:
        if a.preview:
            place_on_bed(obj); render_preview(obj, a.preview)
        return

    unit = {"mm": 1, "cm": 10, "m": 1000, "in": 25.4}[a.units]
    if unit != 1:
        obj.scale = (unit,) * 3; apply_transform(obj)
    if a.scale:
        obj.scale = (a.scale,) * 3; apply_transform(obj)
    if a.fit:
        mn, mx = world_bbox(obj)
        k = a.fit / float((mx - mn).max())
        obj.scale = (k,) * 3; apply_transform(obj)
        info["factor_fit"] = round(k, 4)
    if a.mirror:
        s = {"x": (-1, 1, 1), "y": (1, -1, 1), "z": (1, 1, -1)}[a.mirror]
        obj.scale = s; apply_transform(obj)
        bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.mesh.normals_make_consistent(inside=False); bpy.ops.object.mode_set(mode="OBJECT")
    if a.rotate:
        rx, ry, rz = (math.radians(float(x)) for x in a.rotate.split(","))
        obj.rotation_euler = (rx, ry, rz); apply_transform(obj)
    if a.orient:
        info["orientacion_prob"] = auto_orient(obj)
    if a.repair or info["antes"]["normales_invertidas"] or not info["antes"]["estanca"]:
        repair(obj)
        info["reparado"] = True
    if a.script:
        code = open(a.script, encoding="utf-8").read()
        exec(compile(code, a.script, "exec"),
             {"obj": obj, "bpy": bpy, "bmesh": bmesh, "mathutils": mathutils, "np": np, "math": math})
        obj = bpy.context.view_layer.objects.active or obj
        apply_transform(obj)
    place_on_bed(obj)
    info["despues"] = analyze(obj)
    log(json.dumps(info["despues"], ensure_ascii=False))
    if not info["despues"]["entra_en_cama"]:
        log(f"⚠ NO ENTRA en la cama {BED} (dejando 5 mm de margen por lado)")
    if not info["despues"]["estanca"]:
        log("⚠ la malla sigue sin ser estanca; el laminador puede fallar en zonas")

    if a.output:
        bpy.ops.object.select_all(action="DESELECT"); obj.select_set(True)
        bpy.ops.wm.stl_export(filepath=os.path.abspath(a.output), export_selected_objects=True,
                              global_scale=1.0, use_scene_unit=False, ascii_format=False)
        log(f"STL listo -> {a.output}")
    if a.preview:
        render_preview(obj, a.preview)
        log(f"vista previa -> {a.preview}")
    if a.report:
        json.dump(info, open(a.report, "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
