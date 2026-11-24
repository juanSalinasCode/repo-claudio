"""Construye la mini casa: ejecuta core.py y cada zona en un espacio de nombres compartido, luego exporta.

Uso: python build.py [--out DIR] [--zones exterior,cocina,...]
Cada zona (zones/<nombre>.py) usa los helpers, materiales y constantes de core.py y de las zonas anteriores.
"""
import os, sys, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("--out", default=os.path.join(os.path.dirname(HERE), "out"))
ap.add_argument("--zones", default="exterior,estructura,cocina,living,escalera,bano,altillo,puerta_luces")
ap.add_argument("--no-glb", action="store_true")
args = ap.parse_args([a for a in sys.argv[1:] if a != "--"])
ns = {"__name__": "minicasa_build", "__file__": os.path.join(HERE, "core.py")}
exec(compile(open(os.path.join(HERE, "core.py")).read(), "core.py", "exec"), ns)
for z in args.zones.split(","):
    p = os.path.join(HERE, "zones", z + ".py")
    exec(compile(open(p).read(), p, "exec"), ns)
ns["OUT"] = args.out
ns["NO_GLB"] = args.no_glb
EXPORT = '# ----------------------------------------------------------------- export\nos.makedirs(OUT, exist_ok=True)\nbpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "minicasa.blend"))\nif not NO_GLB:\n  bpy.ops.export_scene.gltf(\n    filepath=os.path.join(OUT, "minicasa.glb"), export_format="GLB", export_extras=True,\n    export_apply=True, export_image_format="JPEG", export_jpeg_quality=85, export_lights=False,\n)\nn = sum(1 for o in bpy.data.objects if o.type == "MESH")\nni = sum(1 for o in bpy.data.objects if "interact" in o.keys())\nprint(f"OK objetos={n} interactivos={ni}")\n'
exec(compile(EXPORT, "export", "exec"), ns)
