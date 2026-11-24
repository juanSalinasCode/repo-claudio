"""Auditoría foto vs render (bpy, sin GUI).

Renderiza el modelo actual desde las cámaras de cameras.json y arma, para cada una, una lámina
[fotograma | render | superposición de bordes] usando tools/overlay.py de openhouse-3d.

  /opt/3d/venv/bin/python scripts/audit.py --blend out/minicasa.blend --cams audit/cameras.json --out DIR [--only kitchen1,bath2]

cameras.json: lista de {"name", "frame": ruta al fotograma, "loc": [x,y,z], "target": [x,y,z]  (o "quat": [w,x,y,z]),
                         "fov_h": grados de campo horizontal (default 70), "roll": grados (opcional)}
Coordenadas: las del modelo Blender (metros, Z arriba, frente de la casa en y=0, fondo en y=6).
"""
import argparse, json, math, os, sys, subprocess
import bpy
from mathutils import Vector, Quaternion, Euler

ap = argparse.ArgumentParser()
ap.add_argument("--blend", required=True)
ap.add_argument("--cams", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--only", default="")
ap.add_argument("--width", type=int, default=360)
a = ap.parse_args([x for x in sys.argv[1:] if x != "--"])
os.makedirs(a.out, exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=os.path.abspath(a.blend))
sc = bpy.context.scene
sc.render.engine = "BLENDER_WORKBENCH"
sh = sc.display.shading
sh.light = "STUDIO"; sh.color_type = "TEXTURE"; sh.show_cavity = True; sh.show_shadows = False
for o in bpy.data.objects:                      # ocultar ayudas invisibles
    if o.get("interact") == "loft" or o.get("water_of") or (o.get("vis_state") == "open"):
        o.hide_render = True
cam = bpy.data.objects.new("audit_cam", bpy.data.cameras.new("audit_cam"))
sc.collection.objects.link(cam); sc.camera = cam
cam.data.sensor_fit = "HORIZONTAL"; cam.data.clip_start = 0.03
cams = json.load(open(a.cams))
only = set(filter(None, a.only.split(",")))
from PIL import Image
for c in cams:
    if only and c["name"] not in only:
        continue
    im = Image.open(c["frame"]); W, H = im.size
    sc.render.resolution_x = a.width; sc.render.resolution_y = round(a.width * H / W)
    cam.data.angle = math.radians(c.get("fov_h", 70))
    cam.location = Vector(c["loc"])
    if "quat" in c:
        cam.rotation_mode = "QUATERNION"; cam.rotation_quaternion = Quaternion(c["quat"])
    else:
        cam.rotation_mode = "XYZ"
        q = (Vector(c["target"]) - cam.location).to_track_quat("-Z", "Y")
        if c.get("roll"):
            q = q @ Quaternion((0, 0, 1), math.radians(c["roll"]))
        cam.rotation_euler = q.to_euler()
    rp = os.path.join(a.out, f"{c['name']}_render.png")
    sc.render.filepath = rp
    bpy.ops.render.render(write_still=True)
    ov = os.path.join(a.out, f"{c['name']}_overlay.png")
    subprocess.run([sys.executable, "/opt/3d/openhouse/tools/overlay.py", c["frame"], rp, "--out", ov, "--mode", "edges"], check=False)
    ph = im.convert("RGB").resize((a.width, sc.render.resolution_y))
    rd = Image.open(rp).convert("RGB")
    ovi = Image.open(ov).convert("RGB")
    ovi = ovi.resize((a.width, round(ovi.height * a.width / ovi.width)))
    sheet = Image.new("RGB", (a.width * 2 + ovi.width, max(ph.height, ovi.height)), "black")
    sheet.paste(ph, (0, 0)); sheet.paste(rd, (a.width, 0)); sheet.paste(ovi, (a.width * 2, 0))
    sheet.save(os.path.join(a.out, f"{c['name']}_audit.jpg"), quality=85)
    print("audit", c["name"])
