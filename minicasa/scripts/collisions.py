"""Auditoría de choques entre objetos (bpy, sin GUI).

  /opt/3d/venv/bin/python scripts/collisions.py --blend out/minicasa.blend --out audit/colisiones.md [--plan audit/planta.png]

Para cada par de objetos malla cuyas cajas (AABB en mundo) se superponen más que la tolerancia,
verifica con BVH si las mallas realmente se intersecan y estima la penetración como el menor lado
de la caja de superposición. Ignora: el terreno, objetos invisibles (agua, disparador del altillo,
sillas "abiertas"), y pares estructura-estructura. También genera una planta (vista cenital) con el
contorno de cada mueble para revisar proporciones y pasos libres.
"""
import argparse, math, os, sys
import bpy, bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ap = argparse.ArgumentParser()
ap.add_argument("--blend", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--plan")
ap.add_argument("--tol", type=float, default=0.012)    # 1,2 cm: apoyos/contactos normales
a = ap.parse_args([x for x in sys.argv[1:] if x != "--"])
bpy.ops.wm.open_mainfile(filepath=os.path.abspath(a.blend))

SKIP_PREFIX = ("Terreno", "Arbol", "Tronco", "Copa", "Bosque", "Ripio", "Pasto")
STRUCT_COLL = {"Estructura", "Ventanas"}

def coll_of(o):
    return o.users_collection[0].name if o.users_collection else ""

objs = []
for o in bpy.data.objects:
    if o.type != "MESH" or o.name.startswith(SKIP_PREFIX):
        continue
    if o.get("water_of") or o.get("interact") == "loft" or o.get("vis_state") == "open":
        continue
    dg = o.evaluated_get(bpy.context.evaluated_depsgraph_get())
    me = dg.to_mesh()
    if not me.vertices:
        continue
    bm = bmesh.new(); bm.from_mesh(me); bm.transform(o.matrix_world)
    vs = [v.co.copy() for v in bm.verts]
    mn = Vector((min(v.x for v in vs), min(v.y for v in vs), min(v.z for v in vs)))
    mx = Vector((max(v.x for v in vs), max(v.y for v in vs), max(v.z for v in vs)))
    objs.append(dict(o=o, name=o.name, coll=coll_of(o), mn=mn, mx=mx, bvh=BVHTree.FromBMesh(bm)))
    bm.free(); dg.to_mesh_clear()

def inside_mesh(M, p):
    """Paridad de cruces de un rayo +x contra la malla M: True si p está adentro del volumen."""
    n, o, d = 0, Vector(p), Vector((1, 0.0007, 0.0003)).normalized()
    for _ in range(64):
        hit = M["bvh"].ray_cast(o, d)
        if hit[0] is None:
            break
        n += 1; o = hit[0] + d * 1e-4
    return n % 2 == 1

def overlap(A, B):
    lo = Vector([max(A["mn"][i], B["mn"][i]) for i in range(3)])
    hi = Vector([min(A["mx"][i], B["mx"][i]) for i in range(3)])
    d = hi - lo
    return d if min(d) > a.tol else None

hits = []
for i in range(len(objs)):
    A = objs[i]
    for j in range(i + 1, len(objs)):
        B = objs[j]
        if A["coll"] in STRUCT_COLL and B["coll"] in STRUCT_COLL:
            continue
        d = overlap(A, B)
        if d is None:
            continue
        if not A["bvh"].overlap(B["bvh"]):
            # sin cruce de superficies: ¿uno está completamente adentro del otro?
            inside = inside_mesh(A, (B["mn"] + B["mx"]) / 2) or inside_mesh(B, (A["mn"] + A["mx"]) / 2)
            if not inside:
                continue
            kind = "contenido"
        else:
            kind = "cruce"
        pen = min(d)
        hits.append((pen, kind, A, B, d))

hits.sort(key=lambda h: -h[0])
lines = ["# Choques entre objetos", "",
         f"Tolerancia de contacto: {a.tol*100:.1f} cm. Penetración = lado menor de la caja de superposición.", "",
         "| Penetración (cm) | Tipo | Objeto A (zona) | Objeto B (zona) | Caja superpuesta x·y·z (cm) | Centro (x, y, z) |",
         "|---:|---|---|---|---|---|"]
for pen, kind, A, B, d in hits:
    lo = Vector([max(A["mn"][i], B["mn"][i]) for i in range(3)])
    c = lo + d / 2
    lines.append(f"| {pen*100:.1f} | {kind} | {A['name']} ({A['coll']}) | {B['name']} ({B['coll']}) | "
                 f"{d.x*100:.0f}·{d.y*100:.0f}·{d.z*100:.0f} | ({c.x:.2f}, {c.y:.2f}, {c.z:.2f}) |")
open(a.out, "w").write("\n".join(lines) + "\n")
print(f"choques={len(hits)}  (>5 cm: {sum(1 for h in hits if h[0] > 0.05)})")

if a.plan:
    from PIL import Image, ImageDraw
    S = 140  # px por metro
    xs = [o["mn"].x for o in objs] + [o["mx"].x for o in objs]
    ys = [o["mn"].y for o in objs] + [o["mx"].y for o in objs]
    x0, x1, y0, y1 = -1.6, 1.6, -0.6, 6.4
    im = Image.new("RGB", (int((x1 - x0) * S), int((y1 - y0) * S)), "white"); dr = ImageDraw.Draw(im)
    P = lambda x, y: ((x - x0) * S, (y1 - y) * S)
    for o in objs:
        if o["mn"].z > 2.0 or o["mx"].z < 0.05:      # solo lo que ocupa el piso (0–2 m)
            continue
        col = (90, 90, 90) if o["coll"] in STRUCT_COLL else (40, 110, 200)
        if o["coll"] not in STRUCT_COLL and (o["mx"].x - o["mn"].x) * (o["mx"].y - o["mn"].y) < 0.004:
            continue
        dr.rectangle([P(o["mn"].x, o["mx"].y), P(o["mx"].x, o["mn"].y)], outline=col, width=1)
    bad = {h[2]["name"] for h in hits if h[0] > 0.03} | {h[3]["name"] for h in hits if h[0] > 0.03}
    for o in objs:
        if o["name"] in bad and o["mn"].z < 2.0:
            dr.rectangle([P(o["mn"].x, o["mx"].y), P(o["mx"].x, o["mn"].y)], outline=(220, 30, 30), width=2)
    for m in range(0, 7):
        dr.line([P(x0, m), P(x0 + 0.15, m)], fill=(0, 0, 0)); dr.text(P(x0 + 0.17, m + 0.05), f"y={m}", fill=(0, 0, 0))
    im.save(a.plan)
    print("planta ->", a.plan)
