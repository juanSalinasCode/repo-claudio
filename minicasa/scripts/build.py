"""Construye la mini casa del video en Blender (bpy 5.x, sin GUI) y exporta .blend + .glb.

Convenciones (coordenadas Blender, metros, Z arriba):
  - Frente de la casa (puerta) en y=0, fondo en y=L. Ancho interior x in [-W/2, W/2].
  - Piso interior en z=0. El terreno está en z=GROUND.
  - Objetos interactivos: el origen del objeto es su bisagra/pivote y llevan
    propiedades personalizadas que el exportador glTF guarda como "extras":
      interact = "rot" | "slide" | "combo" | "light" | "water" | "loft"
      axis/angle (en coords three.js), vec (three.js), label (texto en español), group
"""
import math, os, sys
import bpy, bmesh
from mathutils import Vector, Matrix

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEX = os.path.join(ROOT, "tex")
OUT = os.path.join(ROOT, "out")

# ----------------------------------------------------------------- medidas
W = 2.40          # ancho interior
L = 6.00          # largo interior
T = 0.12          # espesor de pared
EAVE = 2.45       # altura de pared lateral (interior)
RIDGE = 3.60      # altura de la cumbrera (interior)
GROUND = -0.50    # nivel del terreno
BATH_Y = 4.40     # tabique del baño
LOFT_Z = 2.10     # piso del altillo (= cielorraso del baño)
XL, XR = -W / 2, W / 2

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = "METRIC"

# ----------------------------------------------------------------- materiales
MATS = {}

def mat(name, color=(0.8, 0.8, 0.8), tex=None, rough=0.7, metal=0.0, alpha=1.0, emit=None, emit_strength=1.0):
    if name in MATS:
        return MATS[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    if tex:
        img = bpy.data.images.load(os.path.join(TEX, tex), check_existing=True)
        tn = nt.nodes.new("ShaderNodeTexImage")
        tn.image = img
        nt.links.new(tn.outputs["Color"], bsdf.inputs["Base Color"])
    if alpha < 1:
        bsdf.inputs["Alpha"].default_value = alpha
        try:
            m.surface_render_method = "BLENDED"
        except Exception:
            m.blend_method = "BLEND"
    if emit:
        bsdf.inputs["Emission Color"].default_value = (*emit, 1)
        bsdf.inputs["Emission Strength"].default_value = emit_strength
    MATS[name] = m
    return m

M = dict(
    plywood=mat("Multilaminado", tex="plywood.jpg"),
    floor=mat("Piso madera", tex="floor.jpg", rough=0.45),
    siding=mat("Revestimiento exterior", tex="siding.jpg"),
    trim=mat("Marco blanco", (0.93, 0.93, 0.92), rough=0.5),
    yellow=mat("Puerta amarilla", (0.98, 0.80, 0.08), rough=0.4),
    chalk=mat("Pizarron negro", tex="chalk.jpg", rough=0.9),
    black=mat("Negro", (0.03, 0.03, 0.035), rough=0.5),
    blackmetal=mat("Metal negro", (0.02, 0.02, 0.02), rough=0.35, metal=0.6),
    steel=mat("Acero", (0.75, 0.76, 0.78), rough=0.25, metal=1.0),
    glass=mat("Vidrio", (0.75, 0.88, 0.95), rough=0.05, alpha=0.25),
    cabinet=mat("Madera mueble", tex="cabinet.jpg", rough=0.5),
    counter=mat("Mesada madera clara", (0.86, 0.72, 0.52), rough=0.5),
    mint=mat("Verde agua heladera", (0.62, 0.86, 0.76), rough=0.35),
    fridge_in=mat("Interior heladera", (0.92, 0.95, 0.97), rough=0.3),
    teal=mat("Tapizado turquesa", (0.04, 0.33, 0.36), rough=0.9),
    teal_light=mat("Turquesa claro", (0.25, 0.75, 0.72), rough=0.4),
    white=mat("Blanco", (0.96, 0.96, 0.95), rough=0.6),
    white_planks=mat("Machimbre blanco", tex="white_planks.jpg"),
    marble=mat("Marmol", tex="marble.jpg", rough=0.2),
    mural=mat("Mural triangulos", tex="mural.jpg"),
    pine=mat("Pino claro", (0.88, 0.72, 0.48), rough=0.6),
    slat=mat("Madera listones", (0.48, 0.30, 0.16), rough=0.6),
    ceramic=mat("Ceramica", (0.97, 0.97, 0.97), rough=0.15),
    mattress=mat("Colchon", (0.97, 0.97, 0.96), rough=0.9),
    blanket=mat("Manta", (0.82, 0.70, 0.55), rough=0.95),
    pillow=mat("Almohadon", (0.93, 0.55, 0.50), rough=0.95),
    rug=mat("Alfombra", tex="rug.jpg", rough=0.95),
    roof=mat("Techo chapa", tex="roof.jpg", rough=0.4, metal=0.3),
    deck=mat("Deck", tex="deck.jpg", rough=0.8),
    grass=mat("Pasto", tex="grass.jpg", rough=1.0),
    bark=mat("Corteza", tex="bark.jpg", rough=1.0),
    leaves=mat("Follaje", (0.16, 0.38, 0.12), rough=1.0),
    leaves2=mat("Follaje 2", (0.22, 0.45, 0.16), rough=1.0),
    bulb=mat("Lamparita", (1.0, 0.92, 0.75), emit=(1.0, 0.85, 0.6), emit_strength=6.0),
    water=mat("Agua", (0.55, 0.75, 0.95), rough=0.05, alpha=0.55),
    panel=mat("Tablero", (0.65, 0.68, 0.72), rough=0.4, metal=0.5),
    copper=mat("Cobre", (0.85, 0.48, 0.30), rough=0.3, metal=1.0),
    gray=mat("Gris", (0.45, 0.46, 0.48), rough=0.6),
    picture=mat("Lamina", (0.88, 0.88, 0.84), rough=0.8),
    plant=mat("Planta", (0.18, 0.50, 0.22), rough=0.9),
    terracotta=mat("Maceta", (0.72, 0.38, 0.24), rough=0.9),
)

# ----------------------------------------------------------------- geometría
COLL = {}

def coll(name):
    if name not in COLL:
        c = bpy.data.collections.new(name)
        scene.collection.children.link(c)
        COLL[name] = c
    return COLL[name]

CUR = ["Estructura"]

def link(ob):
    coll(CUR[0]).objects.link(ob)
    return ob

def box_uv(bm, tile=1.0, offset=Vector((0, 0, 0))):
    """Proyección cúbica en metros reales: las texturas no se estiran."""
    uv = bm.loops.layers.uv.verify()
    for f in bm.faces:
        n = f.normal
        ax = max(range(3), key=lambda i: abs(n[i]))
        for lp in f.loops:
            co = lp.vert.co + offset
            if ax == 0:
                u, v = co.y, co.z
            elif ax == 1:
                u, v = co.x, co.z
            else:
                u, v = co.x, co.y
            lp[uv].uv = (u / tile, v / tile)

def make_obj(name, bm, mats, pivot=(0, 0, 0), tile=1.0, props=None):
    me = bpy.data.meshes.new(name)
    box_uv(bm, tile, Vector(pivot))
    bm.to_mesh(me)
    bm.free()
    for m_ in mats:
        me.materials.append(m_)
    ob = bpy.data.objects.new(name, me)
    ob.location = pivot
    if props:
        for k, v in props.items():
            ob[k] = v
    return link(ob)

def add_box(bm, x0, x1, y0, y1, z0, z1, pivot=(0, 0, 0), mi=0):
    px, py, pz = pivot
    res = bmesh.ops.create_cube(bm, size=1.0)
    vs = res["verts"]
    for v in vs:
        v.co.x = (x0 if v.co.x < 0 else x1) - px
        v.co.y = (y0 if v.co.y < 0 else y1) - py
        v.co.z = (z0 if v.co.z < 0 else z1) - pz
    faces = {f for v in vs for f in v.link_faces}
    for f in faces:
        f.material_index = mi
    return faces

def box(name, x0, x1, y0, y1, z0, z1, m_, pivot=None, tile=1.0, props=None):
    bm = bmesh.new()
    pv = pivot if pivot else ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)
    add_box(bm, x0, x1, y0, y1, z0, z1, pv)
    bm.normal_update()
    return make_obj(name, bm, [m_], pv, tile, props)

def multi(name, parts, mats, pivot=(0, 0, 0), tile=1.0, props=None):
    """parts: lista de (x0,x1,y0,y1,z0,z1, material_index)."""
    bm = bmesh.new()
    for p in parts:
        add_box(bm, *p[:6], pivot=pivot, mi=p[6] if len(p) > 6 else 0)
    bm.normal_update()
    return make_obj(name, bm, mats, pivot, tile, props)

def cyl(name, x, y, z0, z1, r, m_, verts=16, axis="Z", props=None, pivot=None):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=verts, radius1=r, radius2=r, depth=z1 - z0)
    if axis == "X":
        bmesh.ops.rotate(bm, verts=bm.verts, matrix=Matrix.Rotation(math.pi / 2, 3, "Y"))
    elif axis == "Y":
        bmesh.ops.rotate(bm, verts=bm.verts, matrix=Matrix.Rotation(math.pi / 2, 3, "X"))
    c = Vector((x, y, (z0 + z1) / 2)) if axis == "Z" else Vector((x, y, z0))
    pv = Vector(pivot) if pivot else c
    bmesh.ops.translate(bm, verts=bm.verts, vec=c - pv)
    bm.normal_update()
    return make_obj(name, bm, [m_], tuple(pv), 1.0, props)

def cone(name, x, y, z0, z1, r0, r1, m_, verts=10):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=verts, radius1=r0, radius2=r1, depth=z1 - z0)
    bm.normal_update()
    return make_obj(name, bm, [m_], (x, y, (z0 + z1) / 2), 1.0)

def sphere(name, x, y, z, r, m_, sx=1, sy=1, sz=1, seg=12):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=seg // 2 + 2, radius=r)
    bmesh.ops.scale(bm, vec=(sx, sy, sz), verts=bm.verts)
    bm.normal_update()
    return make_obj(name, bm, [m_], (x, y, z), 1.0)

def prism(name, pts2d, plane, d0, d1, m_, tile=1.0):
    """Polígono en el plano XZ (plane='y': extruido en y de d0 a d1)."""
    bm = bmesh.new()
    vs0 = [bm.verts.new((p[0], d0, p[1])) for p in pts2d]
    vs1 = [bm.verts.new((p[0], d1, p[1])) for p in pts2d]
    bm.faces.new(vs0[::-1]); bm.faces.new(vs1)
    n = len(pts2d)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new([vs0[i], vs0[j], vs1[j], vs1[i]])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.normal_update()
    return make_obj(name, bm, [m_], (0, 0, 0), tile)

def wall_with_openings(name, axis, const0, const1, s0, s1, z0, z1, openings, mats, inside_mi, outside_mi, inside_sign):
    """Pared plana con huecos. axis='x': pared paralela a Y (x entre const0..const1).
    openings: (s_a, s_b, z_a, z_b). inside_sign: +1 si el interior está hacia +eje normal.
    El material de cada cara depende de si mira hacia adentro o afuera."""
    ss = sorted({s0, s1, *[o[0] for o in openings], *[o[1] for o in openings]})
    zs = sorted({z0, z1, *[o[2] for o in openings], *[o[3] for o in openings]})
    bm = bmesh.new()
    for i in range(len(ss) - 1):
        for k in range(len(zs) - 1):
            a, b, c, d = ss[i], ss[i + 1], zs[k], zs[k + 1]
            if a < s0 or b > s1:
                continue
            mid_s, mid_z = (a + b) / 2, (c + d) / 2
            if any(o[0] <= mid_s <= o[1] and o[2] <= mid_z <= o[3] for o in openings):
                continue
            if axis == "x":
                add_box(bm, const0, const1, a, b, c, d)
            else:
                add_box(bm, a, b, const0, const1, c, d)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)
    bm.normal_update()
    nidx = 0 if axis == "x" else 1
    for f in bm.faces:
        n = f.normal[nidx]
        if abs(n) > 0.5:
            f.material_index = inside_mi if n * inside_sign > 0 else outside_mi
        else:
            f.material_index = outside_mi if False else inside_mi
    return make_obj(name, bm, mats, (0, 0, 0), 1.0)

# ----------------------------------------------------------------- interacción
def three_axis(blender_axis, angle):
    """Convierte eje de rotación Blender -> three.js (Y arriba)."""
    return {"X": ("x", angle), "Y": ("z", -angle), "Z": ("y", angle)}[blender_axis]

def three_vec(v):
    return [v[0], v[2], -v[1]]

def interactive(ob, kind, label, group=None, axis=None, angle=0.0, vec=None, extra=None):
    ob["interact"] = kind
    ob["label"] = label
    ob["group"] = group or ob.name
    if axis:
        a, ang = three_axis(axis, angle)
        ob["axis"] = a
        ob["angle"] = ang
    if vec is not None:
        ob["vec"] = three_vec(vec)
    if extra:
        for k, v in extra.items():
            ob[k] = v
    return ob

# =================================================================== EXTERIOR
CUR[0] = "Exterior"
# terreno y senderos
box("Terreno", -25, 25, -25, 25, GROUND - 0.1, GROUND, M["grass"], tile=4.0)
# pilotes / zócalo
multi("Zocalo", [(XL - T, XR + T, -T, L + T, GROUND, -0.02)], [M["gray"]])
# deck frontal + escalones
box("Deck", XL - 0.6, XR + 0.6, -1.6, -T, -0.10, -0.02, M["deck"], tile=1.5)
box("Escalon 1", -0.7, 0.9, -1.95, -1.6, -0.27, -0.19, M["deck"], tile=1.5)
box("Escalon 2", -0.7, 0.9, -2.30, -1.95, -0.44, -0.36, M["deck"], tile=1.5)
for i, (x, y) in enumerate([(XL - 0.55, -1.55), (XR + 0.55, -1.55)]):
    box(f"Poste deck {i}", x - 0.05, x + 0.05, y - 0.05, y + 0.05, GROUND, -0.02, M["deck"])
box("Felpudo", 0.25, 0.85, -0.75, -0.25, -0.02, -0.005, M["rug"])

# techo a dos aguas (chapa) – vigas de extremo a extremo
OV = 0.30  # alero
def roof_slab(name, side):
    x_e = side * (W / 2 + T + 0.18)
    z_e = EAVE + 0.12
    z_r = RIDGE + 0.22
    pts = [(0, z_r), (x_e, z_e), (x_e, z_e + 0.08), (0, z_r + 0.08)] if side > 0 else [(x_e, z_e), (0, z_r), (0, z_r + 0.08), (x_e, z_e + 0.08)]
    return prism(name, pts, "y", -T - OV, L + T + OV, M["roof"], tile=1.0)
roof_slab("Techo der", 1)
roof_slab("Techo izq", -1)
# cenefas
for s in (-1, 1):
    pass

# lámparas exteriores junto a la puerta
for i, x in enumerate([0.02, 1.08]):
    box(f"Farol {i}", x - 0.07, x + 0.07, -T - 0.12, -T, 1.95, 2.18, M["blackmetal"])
    box(f"Farol vidrio {i}", x - 0.05, x + 0.05, -T - 0.11, -T - 0.01, 1.98, 2.14, M["bulb"])
# unidad exterior de aire acondicionado
box("Condensadora", XL - T - 0.35, XL - T - 0.02, 3.4, 4.2, GROUND + 0.1, GROUND + 0.75, M["white"])
box("Condensadora rejilla", XL - T - 0.36, XL - T - 0.35, 3.55, 4.05, GROUND + 0.2, GROUND + 0.65, M["blackmetal"])
# parrilla y cajones del exterior (vistos en la toma inicial)
box("Parrilla", XL - 1.4, XL - 0.9, -1.2, -0.7, GROUND + 0.55, GROUND + 0.85, M["blackmetal"])
for (dx, dy) in [(-0.2, -0.2), (0.2, -0.2), (-0.2, 0.2), (0.2, 0.2)]:
    box("Pata parrilla", XL - 1.15 + dx - 0.02, XL - 1.15 + dx + 0.02, -0.95 + dy - 0.02, -0.95 + dy + 0.02, GROUND, GROUND + 0.55, M["blackmetal"])

# árboles (bosque alrededor)
import random
random.seed(4)
trees = 0
while trees < 34:
    x, y = random.uniform(-20, 20), random.uniform(-18, 24)
    if -5 < x < 5 and -6 < y < 10:
        continue
    h = random.uniform(7, 13)
    cyl(f"Tronco {trees}", x, y, GROUND, GROUND + h * 0.6, random.uniform(0.12, 0.25), M["bark"], verts=8)
    sphere(f"Copa {trees}", x, y, GROUND + h * 0.7, random.uniform(1.6, 2.8),
           M["leaves"] if trees % 2 else M["leaves2"], sz=random.uniform(1.1, 1.5), seg=10)
    trees += 1

# =================================================================== ESTRUCTURA
CUR[0] = "Estructura"
# pared frontal (y=-T..0): puerta x 0.15..0.95 ; ventana x -0.95..-0.35
FRONT_DOOR = (0.15, 0.95, 0.0, 2.02)
FRONT_WIN = (-0.95, -0.35, 0.95, 1.75)
wall_with_openings("Pared frontal", "y", -T, 0.0, XL - T, XR + T, 0.0, EAVE, [FRONT_DOOR, FRONT_WIN],
                   [M["plywood"], M["siding"]], 0, 1, +1)
# hastial frontal (triángulo)
gable = [(XL - T, EAVE), (XR + T, EAVE), (0, RIDGE + 0.15)]
g = prism("Hastial frontal", gable, "y", -T, 0.0, M["siding"])
g.data.materials.append(M["plywood"])
for p in g.data.polygons:
    if p.normal.y > 0.5:
        p.material_index = 1
# pared trasera (y=L..L+T) con ventanas del altillo
BACK_WINS = [(-0.75, -0.25, 2.35, 2.85), (0.25, 0.75, 2.35, 2.85)]
wall_with_openings("Pared trasera", "y", L, L + T, XL - T, XR + T, 0.0, EAVE, [],
                   [M["white"], M["siding"]], 0, 1, -1)
gb = prism("Hastial trasero", [(XL - T, EAVE), (XR + T, EAVE), (0, RIDGE + 0.15)], "y", L, L + T, M["siding"])
gb.data.materials.append(M["plywood"])
for p in gb.data.polygons:
    if p.normal.y < -0.5:
        p.material_index = 1
for i, (a, b, c, d) in enumerate(BACK_WINS):
    cut = box(f"_corte{i}", a, b, L - 0.1, L + T + 0.1, c, d, M["glass"])
    mod = gb.modifiers.new(f"hueco{i}", "BOOLEAN"); mod.operation = "DIFFERENCE"; mod.object = cut; mod.solver = "EXACT"
    bpy.context.view_layer.objects.active = gb
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cut)
# ventanas del altillo (marcos + vidrio sobre el hastial)
for i, (a, b, c, d) in enumerate(BACK_WINS):
    box(f"Ventana altillo marco {i}", a - 0.05, b + 0.05, L - 0.01, L + T + 0.02, c - 0.05, d + 0.05, M["trim"])
    box(f"Ventana altillo vidrio {i}", a, b, L - 0.02, L + T + 0.03, c, d, M["glass"])

# paredes laterales con huecos
LEFT_WINS = [(0.25, 0.75, 1.20, 1.80), (1.20, 2.25, 1.05, 2.05)]          # x = XL (cocina)
RIGHT_WINS = [(1.15, 1.45, 1.20, 1.85), (3.05, 3.95, 1.00, 1.95), (5.05, 5.55, 1.25, 1.80)]  # x = XR
wall_with_openings("Pared izquierda", "x", XL - T, XL, 0.0, L, 0.0, EAVE, LEFT_WINS,
                   [M["plywood"], M["siding"]], 0, 1, +1)
wall_with_openings("Pared derecha", "x", XR, XR + T, 0.0, L, 0.0, EAVE, RIGHT_WINS,
                   [M["plywood"], M["siding"]], 0, 1, -1)
# revestimiento blanco del baño sobre las paredes laterales y trasera (interior)
box("Baño revest izq", XL, XL + 0.01, BATH_Y, L, 0.0, LOFT_Z, M["white_planks"])
multi("Baño revest der", [(XR - 0.01, XR, BATH_Y, 5.05, 0, LOFT_Z), (XR - 0.01, XR, 5.55, L, 0, LOFT_Z),
                          (XR - 0.01, XR, 5.05, 5.55, 0, 1.25), (XR - 0.01, XR, 5.05, 5.55, 1.80, LOFT_Z)],
      [M["white_planks"]])

def window(name, axis, const, a, b, c, d, outward):
    """Marco oscuro interior (como en el video) + marco blanco exterior + vidrio."""
    th = 0.05
    if axis == "x":
        inner = const - outward * 0.005
        multi(name + " marco", [
            (min(inner, inner - outward * th), max(inner, inner - outward * th), a - 0.06, b + 0.06, c - 0.06, c, 0),
            (min(inner, inner - outward * th), max(inner, inner - outward * th), a - 0.06, b + 0.06, d, d + 0.06, 0),
            (min(inner, inner - outward * th), max(inner, inner - outward * th), a - 0.06, a, c, d, 0),
            (min(inner, inner - outward * th), max(inner, inner - outward * th), b, b + 0.06, c, d, 0)],
            [M["black"]])
        o = const + outward * T
        multi(name + " marco ext", [
            (min(o, o + outward * 0.03), max(o, o + outward * 0.03), a - 0.07, b + 0.07, c - 0.07, c, 0),
            (min(o, o + outward * 0.03), max(o, o + outward * 0.03), a - 0.07, b + 0.07, d, d + 0.07, 0),
            (min(o, o + outward * 0.03), max(o, o + outward * 0.03), a - 0.07, a, c, d, 0),
            (min(o, o + outward * 0.03), max(o, o + outward * 0.03), b, b + 0.07, c, d, 0)],
            [M["trim"]])
        g0 = const + outward * T / 2
        box(name + " vidrio", g0 - 0.005, g0 + 0.005, a, b, c, d, M["glass"])
        box(name + " alfeizar", min(const, const - outward * 0.12), max(const, const - outward * 0.12), a - 0.06, b + 0.06, c - 0.08, c - 0.05, M["pine"])
    else:
        multi(name + " marco", [
            (a - 0.06, b + 0.06, -0.05, 0.005, c - 0.06, c, 0), (a - 0.06, b + 0.06, -0.05, 0.005, d, d + 0.06, 0),
            (a - 0.06, a, -0.05, 0.005, c, d, 0), (b, b + 0.06, -0.05, 0.005, c, d, 0)], [M["black"]])
        multi(name + " marco ext", [
            (a - 0.07, b + 0.07, -T - 0.03, -T, c - 0.07, c, 0), (a - 0.07, b + 0.07, -T - 0.03, -T, d, d + 0.07, 0),
            (a - 0.07, a, -T - 0.03, -T, c, d, 0), (b, b + 0.07, -T - 0.03, -T, c, d, 0),
            (a - 0.05, b + 0.05, -T - 0.03, -T, (c + d) / 2 - 0.015, (c + d) / 2 + 0.015, 0)], [M["trim"]])
        box(name + " vidrio", a, b, -T / 2 - 0.005, -T / 2 + 0.005, c, d, M["glass"])

CUR[0] = "Ventanas"
window("Ventana frente", "y", 0, *FRONT_WIN, -1)
for i, w_ in enumerate(LEFT_WINS):
    window(f"Ventana cocina {i}", "x", XL, *w_, -1)
for i, w_ in enumerate(RIGHT_WINS):
    window(f"Ventana der {i}", "x", XR, *w_, +1)

CUR[0] = "Estructura"
# pisos
box("Piso madera", XL, XR, 0, BATH_Y, -0.02, 0.0, M["floor"], tile=1.6)
box("Piso baño", XL, XR, BATH_Y, L, -0.02, 0.005, M["marble"], tile=1.2)
# cielorraso inclinado de multilaminado (sigue el techo)
def ceiling_slab(name, side):
    xe = side * W / 2
    pts = [(0, RIDGE), (xe, EAVE), (xe, EAVE + 0.03), (0, RIDGE + 0.03)] if side > 0 else [(xe, EAVE), (0, RIDGE), (0, RIDGE + 0.03), (xe, EAVE + 0.03)]
    return prism(name, pts, "y", 0, L, M["plywood"], tile=1.2)
ceiling_slab("Cielorraso der", 1)
ceiling_slab("Cielorraso izq", -1)
# relleno entre el remate de la pared lateral y la chapa
for s_ in (-1, 1):
    a, b = sorted((s_ * W / 2, s_ * (W / 2 + T)))
    box(f"Cenefa {s_}", a, b, -T, L + T, EAVE, EAVE + 0.22, M["siding"])

# tabique del baño con hueco de puerta; frente con mural, lado baño blanco
BATH_DOOR = (-0.30, 0.48, 0.0, 2.00)
part = wall_with_openings("Tabique baño", "y", BATH_Y - 0.08, BATH_Y, XL, XR, 0.0, LOFT_Z, [BATH_DOOR],
                          [M["white_planks"], M["mural"]], 0, 1, +1)
# altillo: piso + baranda/viga
box("Piso altillo", XL, XR, BATH_Y - 0.10, L, LOFT_Z, LOFT_Z + 0.08, M["pine"], tile=1.2)
box("Cielorraso baño", XL, XR, BATH_Y, L, LOFT_Z - 0.01, LOFT_Z, M["white_planks"])
box("Viga altillo", XL, XR, BATH_Y - 0.12, BATH_Y - 0.06, LOFT_Z - 0.12, LOFT_Z + 0.16, M["pine"])
box("Riel granero", -1.05, 0.95, BATH_Y - 0.13, BATH_Y - 0.11, 2.04, 2.07, M["blackmetal"])
# tabique lateral de la escalera (la pared con huecos donde se guardan los escalones)

# =================================================================== COCINA
CUR[0] = "Cocina"
CX0, CX1 = XL, XL + 0.62     # bajo mesada contra pared izquierda
KY0, KY1 = 0.10, 2.55
box("Bajo mesada", CX0, CX1 - 0.02, KY0, KY1, 0.10, 0.88, M["cabinet"], tile=0.8)
box("Zocalo cocina", CX0, CX1 - 0.07, KY0, KY1, 0.0, 0.10, M["black"])
box("Mesada", CX0, CX1 + 0.02, KY0 - 0.02, KY1 + 0.02, 0.88, 0.92, M["counter"])
# bacha bajo la ventana grande + escurridor
box("Bacha", CX0 + 0.08, CX1 - 0.10, 1.45, 1.95, 0.70, 0.921, M["steel"])
box("Bacha hueco", CX0 + 0.10, CX1 - 0.12, 1.47, 1.93, 0.72, 0.925, M["blackmetal"])
canilla = multi("Canilla cocina", [(-0.02, 0.02, -0.02, 0.02, 0.0, 0.32), (-0.02, 0.20, -0.02, 0.02, 0.30, 0.34)],
                [M["blackmetal"]], pivot=(0, 0, 0))
canilla.location = (CX0 + 0.05, 1.70, 0.92)
interactive(canilla, "water", "Canilla de la cocina", group="agua_cocina")
agua_c = cyl("Agua cocina", CX0 + 0.24, 1.70, 0.73, 1.24, 0.012, M["water"], verts=8)
agua_c["water_of"] = "agua_cocina"
multi("Escurridor", [(CX0 + 0.12 + i * 0.045, CX0 + 0.13 + i * 0.045, 1.98, 2.45, 0.925, 0.935, 0) for i in range(9)], [M["steel"]])
box("Tabla", CX0 + 0.05, CX0 + 0.40, 0.30, 0.55, 0.92, 0.94, M["pine"])
box("Horno electrico", CX0 + 0.05, CX0 + 0.42, 0.18, 0.62, 0.92, 1.15, M["black"])
box("Horno vidrio", CX0 + 0.421, CX0 + 0.43, 0.26, 0.52, 0.96, 1.11, M["glass"])
box("Taco cuchillos", CX0 + 0.05, CX0 + 0.17, 2.30, 2.45, 0.92, 1.12, M["cabinet"])
# frentes: cajones (columna cerca del frente, la que abre el presentador) y puertas
CAJ_X = CX1 - 0.02
for i, (z0, z1) in enumerate([(0.68, 0.86), (0.42, 0.66), (0.12, 0.40)]):
    bm = bmesh.new()
    pv = (CAJ_X, 0.15, z0)
    add_box(bm, CAJ_X, CAJ_X + 0.02, 0.15, 0.68, z0, z1, pivot=pv)                       # frente
    add_box(bm, CAJ_X - 0.48, CAJ_X, 0.18, 0.65, z0 + 0.02, z0 + 0.03, pivot=pv)         # fondo
    add_box(bm, CAJ_X - 0.48, CAJ_X, 0.17, 0.18, z0 + 0.02, z1 - 0.04, pivot=pv)         # lados
    add_box(bm, CAJ_X - 0.48, CAJ_X, 0.65, 0.66, z0 + 0.02, z1 - 0.04, pivot=pv)
    add_box(bm, CAJ_X + 0.02, CAJ_X + 0.035, 0.33, 0.50, (z0 + z1) / 2 - 0.008, (z0 + z1) / 2 + 0.008, pivot=pv)  # tirador
    bm.normal_update()
    caj = make_obj(f"Cajon {i + 1}", bm, [M["cabinet"]], pv, 0.8)
    interactive(caj, "slide", f"Cajón {i + 1} de la cocina", vec=(0.40, 0, 0))
for i, (y0, y1) in enumerate([(0.70, 1.15), (1.15, 1.60), (1.60, 2.05), (2.05, 2.52)]):
    box(f"Puerta alacena {i}", CAJ_X, CAJ_X + 0.02, y0 + 0.01, y1 - 0.01, 0.12, 0.86, M["cabinet"], tile=0.8)
    box(f"Tirador {i}", CAJ_X + 0.02, CAJ_X + 0.035, y1 - 0.08, y1 - 0.06, 0.55, 0.75, M["steel"])
# estantes abiertos sobre la mesada (cerca del frente) con vajilla
for k, z in enumerate([1.50, 1.85]):
    box(f"Estante cocina {k}", XL, XL + 0.28, 0.12, 1.05, z, z + 0.035, M["cabinet"])
    for j in range(4):
        cyl(f"Taza {k}{j}", XL + 0.12, 0.25 + j * 0.2, z + 0.035, z + 0.13, 0.045, M["teal_light"], verts=10)
    multi(f"Platos {k}", [(XL + 0.05, XL + 0.25, 0.95 - 0.02 * n, 0.96 - 0.02 * n, z + 0.035, z + 0.25, 0) for n in range(4)], [M["black"]])
# mueble negro de cubos con anafe y cafetera (lado derecho, junto a la puerta)
SX0, SX1, SY0, SY1 = XR - 0.40, XR - 0.01, 0.95, 1.62
multi("Mueble cubos", [(SX0, SX1, SY0, SY1, 0.0, 0.03), (SX0, SX1, SY0, SY1, 0.43, 0.46), (SX0, SX1, SY0, SY1, 0.86, 0.90),
                       (SX0, SX1, SY0, SY0 + 0.03, 0, 0.9), (SX0, SX1, SY1 - 0.03, SY1, 0, 0.9), (SX0, SX1, (SY0 + SY1) / 2 - 0.015, (SY0 + SY1) / 2 + 0.015, 0, 0.9),
                       (SX1 - 0.02, SX1, SY0, SY1, 0, 0.9)], [M["black"]])
box("Cesto azul", SX0 + 0.05, SX1 - 0.05, SY0 + 0.06, SY0 + 0.30, 0.46, 0.80, mat("Azul", (0.15, 0.30, 0.65)))
box("Cesto rojo", SX0 + 0.05, SX1 - 0.05, SY0 + 0.06, SY0 + 0.30, 0.03, 0.38, mat("Rojo", (0.70, 0.12, 0.12)))
box("Tapa turquesa", SX0, SX1, SY0, SY1, 0.90, 0.91, M["teal_light"])
cyl("Anafe", SX0 + 0.2, SY0 + 0.18, 0.91, 0.97, 0.15, M["black"], verts=20)
cyl("Hornalla", SX0 + 0.2, SY0 + 0.18, 0.97, 0.975, 0.09, M["gray"], verts=20)
box("Cafetera", SX0 + 0.06, SX0 + 0.30, SY1 - 0.30, SY1 - 0.06, 0.91, 1.22, M["teal_light"])
cyl("Jarra", SX0 + 0.18, SY1 - 0.20, 0.93, 1.05, 0.06, M["glass"], verts=12)
box("Toallero", XR - 0.06, XR - 0.01, 1.05, 1.55, 1.30, 1.32, M["white"])
box("Repasador", XR - 0.05, XR - 0.04, 1.10, 1.50, 1.05, 1.31, M["teal_light"])
box("Espejo marco", XR - 0.03, XR - 0.005, 2.35, 2.85, 1.00, 1.85, M["black"])
box("Espejo", XR - 0.035, XR - 0.03, 2.39, 2.81, 1.04, 1.81, M["steel"])
box("Termostato", XR - 0.02, XR - 0.005, 1.70, 1.80, 1.45, 1.60, M["white"])
# alfombras
box("Alfombra entrada", 0.10, 0.95, 0.15, 0.95, 0.0, 0.008, M["rug"], tile=0.8)
box("Alfombra cocina", -0.50, 0.20, 0.90, 2.40, 0.0, 0.008, M["rug"], tile=1.5)
# láminas y mandala
box("Cuadro frente", -0.35, 0.35, -0.01, 0.0, 2.55, 3.15, M["black"])
box("Lamina frente", -0.30, 0.30, -0.012, -0.005, 2.60, 3.10, M["picture"])
cyl("Mandala", XR - 0.01, 2.05, 1.95, 1.97, 0.16, M["cabinet"], verts=12, axis="X")
box("Pizarra menu", XL, XL + 0.02, 2.60, 3.10, 1.55, 2.05, M["chalk"])

# =================================================================== HELADERA, MESA, SILLAS
CUR[0] = "Living"
FX0, FX1, FY0, FY1 = XL + 0.02, XL + 0.66, 2.58, 3.20
FZ_D = 0.55   # división freezer (abajo) / heladera (arriba)
multi("Heladera cuerpo", [(FX0, FX1 - 0.04, FY0, FY1, 0.03, 1.52)], [M["fridge_in"]])
for k, z in enumerate([0.85, 1.15]):
    box(f"Heladera estante {k}", FX0 + 0.05, FX1 - 0.08, FY0 + 0.04, FY1 - 0.04, z, z + 0.01, M["glass"])
multi("Heladera laterales", [(FX0, FX1 - 0.04, FY0, FY0 + 0.03, 0.03, 1.52), (FX0, FX1 - 0.04, FY1 - 0.03, FY1, 0.03, 1.52),
                             (FX0, FX1 - 0.04, FY0, FY1, 1.49, 1.55), (FX0, FX0 + 0.03, FY0, FY1, 0.03, 1.52),
                             (FX0, FX1 - 0.04, FY0, FY1, 0.0, 0.05)], [M["mint"]])
# puerta superior (bisagra en el lado y=FY1, abre hacia el pasillo)
bm = bmesh.new(); pv = (FX1, FY1, FZ_D + 0.02)
add_box(bm, FX1 - 0.04, FX1, FY0, FY1, FZ_D + 0.02, 1.55, pivot=pv)
add_box(bm, FX1, FX1 + 0.03, FY0 + 0.04, FY0 + 0.07, 0.95, 1.30, pivot=pv)    # manija cromada
bm.normal_update()
pu = make_obj("Heladera puerta", bm, [M["mint"]], pv)
interactive(pu, "rot", "Puerta de la heladera", axis="Z", angle=105)
# freezer: cajón inferior que se tira hacia afuera
bm = bmesh.new(); pv = (FX1, FY0, 0.05)
add_box(bm, FX1 - 0.04, FX1, FY0, FY1, 0.05, FZ_D, pivot=pv)
add_box(bm, FX1 - 0.45, FX1 - 0.04, FY0 + 0.04, FY1 - 0.04, 0.07, 0.08, pivot=pv)
add_box(bm, FX1 - 0.45, FX1 - 0.04, FY0 + 0.04, FY0 + 0.05, 0.07, 0.40, pivot=pv)
add_box(bm, FX1 - 0.45, FX1 - 0.04, FY1 - 0.05, FY1 - 0.04, 0.07, 0.40, pivot=pv)
add_box(bm, FX1, FX1 + 0.03, FY0 + 0.15, FY1 - 0.15, FZ_D - 0.08, FZ_D - 0.05, pivot=pv)
bm.normal_update()
fz = make_obj("Freezer", bm, [M["mint"]], pv)
interactive(fz, "slide", "Freezer (cajón)", vec=(0.38, 0, 0))

# mesa plegable de listones y 2 sillas plegables guardadas entre heladera y tabique
TY = 3.32
bm = bmesh.new(); pv = (XL + 0.05, TY + 0.35, 0.72)
# tapa (plegada: vertical contra la pared). Coordenadas en estado "abierto" rotadas -90 en Y => la armamos vertical.
for k in range(7):
    add_box(bm, XL + 0.03, XL + 0.06, TY + 0.02 + k * 0.10, TY + 0.10 + k * 0.10, 0.72, 1.42, pivot=pv)
add_box(bm, XL + 0.06, XL + 0.09, TY + 0.02, TY + 0.70, 0.75, 0.79, pivot=pv)
add_box(bm, XL + 0.06, XL + 0.09, TY + 0.02, TY + 0.70, 1.33, 1.37, pivot=pv)
bm.normal_update()
mesa = make_obj("Mesa plegable", bm, [M["slat"]], pv)
# al abrir: gira 90° (de vertical a horizontal hacia +x) y baja/se corre
interactive(mesa, "rot", "Mesa plegable", group="mesa", axis="Y", angle=90)
for j in range(2):
    x0 = XL + 0.10 + j * 0.04
    pl = multi(f"Silla plegada {j + 1}", [(x0, x0 + 0.03, 3.42, 3.88, 0.0, 0.86, 0)] +
               [(x0 + 0.03, x0 + 0.04, 3.46, 3.84, 0.45 + k * 0.1, 0.51 + k * 0.1, 0) for k in range(4)], [M["slat"]])
    interactive(pl, "vis", f"Silla plegable {j + 1}", group="mesa", extra={"vis_state": "closed"})
    cx, cy = XL + 0.98, TY + 0.15 + j * 0.42
    parts = [(cx - 0.20, cx + 0.20, cy - 0.19, cy + 0.19, 0.44, 0.47, 0)]
    parts += [(cx + 0.17, cx + 0.20, cy - 0.19, cy + 0.19, 0.47 + k * 0.1, 0.53 + k * 0.1, 0) for k in range(4)]
    parts += [(cx + lx - 0.015, cx + lx + 0.015, cy + ly - 0.015, cy + ly + 0.015, 0.0, 0.44, 0)
              for lx in (-0.18, 0.18) for ly in (-0.17, 0.17)]
    parts += [(cx + 0.17, cx + 0.20, cy + ly - 0.015, cy + ly + 0.015, 0.44, 0.88, 0) for ly in (-0.17, 0.17)]
    ab = multi(f"Silla abierta {j + 1}", parts, [M["slat"]])
    interactive(ab, "vis", f"Silla plegable {j + 1}", group="mesa", extra={"vis_state": "open"})
mens = multi("Mensula mesa", [(XL + 0.0, XL + 0.35, TY + 0.33, TY + 0.37, 0.69, 0.72, 0), (XL + 0.0, XL + 0.03, TY + 0.33, TY + 0.37, 0.35, 0.72, 0)], [M["slat"]])
interactive(mens, "vis", "Mesa plegable", group="mesa", extra={"vis_state": "open"})

# sillón turquesa (loveseat) contra pared derecha
SOX0, SOX1, SOY0, SOY1 = XR - 0.78, XR - 0.02, 3.00, 4.25
multi("Sillon", [(SOX0 + 0.05, SOX1, SOY0, SOY1, 0.18, 0.45, 0), (SOX1 - 0.20, SOX1, SOY0, SOY1, 0.45, 0.85, 0),
                 (SOX0 + 0.05, SOX1, SOY0, SOY0 + 0.14, 0.45, 0.68, 0), (SOX0 + 0.05, SOX1, SOY1 - 0.14, SOY1, 0.45, 0.68, 0)],
      [M["teal"]])
for (x, y) in [(SOX0 + 0.12, SOY0 + 0.08), (SOX0 + 0.12, SOY1 - 0.08), (SOX1 - 0.08, SOY0 + 0.08), (SOX1 - 0.08, SOY1 - 0.08)]:
    cyl("Pata sillon", x, y, 0.0, 0.18, 0.02, M["pine"], verts=8)
box("Almohadon 1", SOX1 - 0.32, SOX1 - 0.20, SOY0 + 0.20, SOY0 + 0.62, 0.45, 0.85, M["pillow"])
box("Almohadon 2", SOX1 - 0.32, SOX1 - 0.20, SOY0 + 0.66, SOY0 + 1.06, 0.45, 0.85, M["white"])
box("Manta sillon", SOX1 - 0.22, SOX1 - 0.02, SOY1 - 0.55, SOY1 - 0.14, 0.70, 0.88, M["white"])
# aire acondicionado split (arriba, pared izquierda, sobre la heladera)
box("Split AA", XL, XL + 0.22, 2.55, 3.45, 2.05, 2.35, M["white"])
# tablero eléctrico sobre el mural
box("Tablero electrico", -0.95, -0.65, BATH_Y - 0.10, BATH_Y - 0.08, 1.15, 1.55, M["panel"])

# =================================================================== ESCALERA ESCONDIDA
CUR[0] = "Escalera"
# panel con ranuras en la pared derecha (sobre el sillón)
box("Panel escalera", XR - 0.03, XR - 0.005, 2.95, BATH_Y - 0.08, 0.90, LOFT_Z, M["pine"])
STEPS = 6
for i in range(STEPS):
    y = 3.02 + i * 0.22
    z = 0.95 + i * 0.20   # bisagra de cada escalón
    bm = bmesh.new(); pv = (XR - 0.035, y, z)
    # plegado: vertical (sobresale hacia arriba), al desplegar gira -90° en Y => horizontal hacia -x
    add_box(bm, XR - 0.065, XR - 0.035, y, y + 0.38, z, z + 0.26, pivot=pv)
    bm.normal_update()
    st = make_obj(f"Escalon oculto {i + 1}", bm, [M["pine"]], pv)
    interactive(st, "rot", "Escalera escondida", group="escalera", axis="Y", angle=-90)
# acceso al altillo (zona clickeable invisible sobre el último escalón)
acc = box("Subir al altillo", XR - 0.45, XR - 0.05, 4.05, BATH_Y - 0.10, 1.95, 2.40, M["glass"])
interactive(acc, "loft", "Subir / bajar del altillo", group="altillo", extra={"needs": "escalera"})
acc.hide_render = True

# =================================================================== BAÑO
CUR[0] = "Baño"
# puerta corrediza tipo granero
bm = bmesh.new(); pv = (BATH_DOOR[0] - 0.05, BATH_Y - 0.16, 0.02)
for k in range(5):
    add_box(bm, BATH_DOOR[0] - 0.05 + k * 0.176, BATH_DOOR[0] - 0.05 + (k + 1) * 0.176 - 0.004, BATH_Y - 0.16, BATH_Y - 0.12, 0.02, 2.04, pivot=pv)
add_box(bm, BATH_DOOR[0], BATH_DOOR[0] + 0.03, BATH_Y - 0.17, BATH_Y - 0.12, 2.00, 2.12, pivot=pv)   # colgador
add_box(bm, BATH_DOOR[1] - 0.04, BATH_DOOR[1] - 0.01, BATH_Y - 0.17, BATH_Y - 0.12, 2.00, 2.12, pivot=pv)
add_box(bm, BATH_DOOR[0] + 0.05, BATH_DOOR[0] + 0.07, BATH_Y - 0.19, BATH_Y - 0.16, 0.85, 1.20, pivot=pv)  # manija
bm.normal_update()
gran = make_obj("Puerta granero", bm, [M["pine"]], pv)
interactive(gran, "slide", "Puerta corrediza del baño", vec=(0.82, 0, 0))
# inodoro (pared izquierda, junto a la entrada)
TX, TY_ = XL + 0.35, 4.85
box("Inodoro mochila", XL + 0.01, XL + 0.20, TY_ - 0.20, TY_ + 0.20, 0.40, 0.78, M["ceramic"])
cyl("Inodoro taza", TX + 0.05, TY_, 0.0, 0.40, 0.19, M["ceramic"], verts=16)
tapa = cyl("Inodoro tapa", TX + 0.05, TY_, 0.40, 0.43, 0.20, M["ceramic"], verts=16, pivot=(XL + 0.20, TY_, 0.43))
interactive(tapa, "rot", "Tapa del inodoro", axis="Y", angle=-95)
cyl("Portarrollo", XL + 0.02, TY_ + 0.38, 0.70, 0.71, 0.06, M["ceramic"], verts=12, axis="X")
# ducha esquinera (fondo izquierda)
SHX1, SHY0 = XL + 0.92, L - 0.90
box("Plato ducha", XL, SHX1, SHY0, L, 0.0, 0.06, M["white"])
multi("Ducha perfiles", [(SHX1 - 0.02, SHX1, SHY0, SHY0 + 0.02, 0.06, 1.95), (XL, SHX1, SHY0, SHY0 + 0.02, 1.93, 1.95),
                         (SHX1 - 0.02, SHX1, SHY0, L, 1.93, 1.95), (SHX1 - 0.02, SHX1, L - 0.02, L, 0.06, 1.95)], [M["steel"]])
box("Ducha vidrio fijo", XL, SHX1 - 0.02, SHY0, SHY0 + 0.01, 0.06, 1.93, M["glass"])
bm = bmesh.new(); pv = (SHX1 - 0.01, SHY0 + 0.02, 0.06)
add_box(bm, SHX1 - 0.015, SHX1 - 0.005, SHY0 + 0.02, L - 0.03, 0.06, 1.92, pivot=pv)
add_box(bm, SHX1 - 0.005, SHX1 + 0.015, L - 0.25, L - 0.22, 0.90, 1.20, pivot=pv, mi=1)
bm.normal_update()
mampara = make_obj("Mampara ducha", bm, [M["glass"], M["steel"]], pv)
interactive(mampara, "rot", "Puerta de la ducha", axis="Z", angle=-80)
cyl("Flor ducha", XL + 0.40, L - 0.10, 1.85, 1.87, 0.10, M["steel"], verts=16)
box("Brazo ducha", XL + 0.38, XL + 0.42, L - 0.10, L - 0.01, 1.85, 1.95, M["steel"])
box("Canasto ducha", XL + 0.02, XL + 0.12, L - 0.55, L - 0.20, 1.10, 1.40, M["blackmetal"])
agua_d = cyl("Agua ducha", XL + 0.40, L - 0.10, 0.06, 1.85, 0.06, M["water"], verts=10)
agua_d["water_of"] = "agua_ducha"
grif = box("Grifo ducha", XL + 0.02, XL + 0.06, L - 0.45, L - 0.35, 1.05, 1.15, M["blackmetal"])
interactive(grif, "water", "Abrir la ducha", group="agua_ducha")
# vanitorio de madera con bacha negra (pared del fondo, lado derecho)
VX0, VX1 = 0.10, XR - 0.05
multi("Vanitorio", [(VX0, VX1, L - 0.50, L - 0.02, 0.80, 0.85, 0), (VX0, VX1, L - 0.50, L - 0.02, 0.18, 0.21, 0),
                    (VX0, VX0 + 0.05, L - 0.50, L - 0.45, 0.0, 0.85, 0), (VX1 - 0.05, VX1, L - 0.50, L - 0.45, 0.0, 0.85, 0),
                    (VX0, VX0 + 0.05, L - 0.07, L - 0.02, 0.0, 0.85, 0), (VX1 - 0.05, VX1, L - 0.07, L - 0.02, 0.0, 0.85, 0)],
      [M["pine"]])
box("Bacha negra", 0.45, 0.85, L - 0.42, L - 0.12, 0.85, 1.00, M["black"])
canilla_b = multi("Canilla baño", [(-0.02, 0.02, -0.03, 0.0, -0.02, 0.02), (-0.015, 0.015, -0.20, -0.03, -0.015, 0.015)],
                  [M["blackmetal"]], pivot=(0, 0, 0))
canilla_b.location = (0.65, L - 0.01, 1.12)
interactive(canilla_b, "water", "Canilla del baño", group="agua_bano")
agua_b = cyl("Agua baño", 0.65, L - 0.20, 0.92, 1.11, 0.010, M["water"], verts=8)
agua_b["water_of"] = "agua_bano"
for k in range(3):
    box(f"Toalla {k}", VX0 + 0.12 + k * 0.28, VX0 + 0.36 + k * 0.28, L - 0.45, L - 0.10, 0.21, 0.30 + 0.0 * k, M["teal"] if k != 1 else M["white"])
box("Espejo baño marco", 0.30, 1.00, L - 0.02, L - 0.005, 1.25, 1.95, M["black"])
box("Espejo baño", 0.34, 0.96, L - 0.025, L - 0.02, 1.29, 1.91, M["steel"])
box("Barra luces baño", 0.25, 1.05, L - 0.12, L - 0.08, 2.00, 2.04, M["blackmetal"])
for k in range(5):
    sphere(f"Lamparita baño {k}", 0.33 + k * 0.17, L - 0.10, 1.96, 0.035, M["bulb"], seg=8)
multi("Estante baño", [(XR - 0.20, XR - 0.01, L - 0.95, L - 0.45, z, z + 0.02, 0) for z in (1.10, 1.35, 1.60, 1.85)] +
      [(XR - 0.20, XR - 0.01, L - 0.95, L - 0.93, 1.10, 1.87, 0), (XR - 0.20, XR - 0.01, L - 0.47, L - 0.45, 1.10, 1.87, 0)], [M["pine"]])
multi("Toallero escalera", [(0.02, 0.05, L - 0.55, L - 0.52, 0.0, 1.90, 0), (0.02, 0.05, L - 0.05, L - 0.02, 0.0, 1.90, 0)] +
      [(0.02, 0.05, L - 0.55, L - 0.02, z, z + 0.02, 0) for z in (0.4, 0.8, 1.2, 1.6)], [M["blackmetal"]])

# =================================================================== ALTILLO
CUR[0] = "Altillo"
box("Colchon", XL + 0.15, XR - 0.15, BATH_Y + 0.15, L - 0.10, LOFT_Z + 0.08, LOFT_Z + 0.30, M["mattress"])
box("Edredon", XL + 0.15, XR - 0.15, BATH_Y + 0.15, L - 0.60, LOFT_Z + 0.30, LOFT_Z + 0.36, M["mattress"])
box("Manta altillo", XL + 0.25, 0.40, BATH_Y + 0.25, L - 0.65, LOFT_Z + 0.36, LOFT_Z + 0.40, M["blanket"])
for k in range(2):
    box(f"Almohada {k}", XL + 0.30 + k * 1.0, XL + 0.95 + k * 1.0, L - 0.55, L - 0.15, LOFT_Z + 0.30, LOFT_Z + 0.42, M["white"])
box("Baranda altillo", XL, XR - 0.50, BATH_Y - 0.10, BATH_Y - 0.06, LOFT_Z + 0.08, LOFT_Z + 0.25, M["pine"])

# =================================================================== PUERTA DE ENTRADA + LUCES
CUR[0] = "Puerta y luces"
d0, d1 = FRONT_DOOR[0], FRONT_DOOR[1]
multi("Marco puerta", [(d0 - 0.05, d0, -T - 0.02, 0.01, 0, 2.07), (d1, d1 + 0.05, -T - 0.02, 0.01, 0, 2.07),
                       (d0 - 0.05, d1 + 0.05, -T - 0.02, 0.01, 2.02, 2.07)], [M["trim"]])
bm = bmesh.new(); pv = (d1 - 0.01, -0.06, 0.0)
add_box(bm, d0 + 0.01, d1 - 0.01, -0.085, -0.035, 0.01, 2.01, pivot=pv)
bm.normal_update()
for f in bm.faces:
    f.material_index = 0 if f.normal.y < -0.5 else 1
add_box(bm, d0 + 0.06, d0 + 0.09, -0.11, -0.085, 0.95, 1.10, pivot=pv, mi=2)   # manija exterior
add_box(bm, d0 + 0.06, d0 + 0.09, -0.035, -0.01, 0.95, 1.10, pivot=pv, mi=2)   # manija interior
door = make_obj("Puerta entrada", bm, [M["yellow"], M["chalk"], M["steel"]], pv)
interactive(door, "rot", "Puerta de entrada", axis="Z", angle=-100)
# puerta mosquitero blanca (exterior, abierta hacia afuera como en el video)
bm = bmesh.new(); pv = (d0 - 0.02, -T - 0.05, 0.0)
add_box(bm, d0, d1, -T - 0.07, -T - 0.04, 0.02, 2.00, pivot=pv)
bm.normal_update()
mosq = make_obj("Puerta mosquitero", bm, [M["trim"]], pv)
interactive(mosq, "rot", "Puerta mosquitero", axis="Z", angle=-95)
# araña negra con 6 lamparitas + llave de luz
CHY = 2.30
cyl("Araña barra", 0, CHY, 2.75, RIDGE, 0.008, M["blackmetal"], verts=6)
for k in range(6):
    a = k * math.pi / 3
    x, y = 0.30 * math.cos(a), CHY + 0.30 * math.sin(a)
    multi(f"Araña brazo {k}", [(min(0, x) - 0.008, max(0, x) + 0.008, min(CHY, y) - 0.008, max(CHY, y) + 0.008, 2.74, 2.76, 0)], [M["blackmetal"]])
    cyl(f"Araña vela {k}", x, y, 2.76, 2.84, 0.012, M["blackmetal"], verts=6)
    sphere(f"Araña lamparita {k}", x, y, 2.88, 0.035, M["bulb"], seg=8)
for k in range(3):
    sphere(f"Spot cocina {k}", XL + 0.25, 1.30 + k * 0.40, 2.25, 0.04, M["bulb"], seg=8)
box("Riel spots", XL + 0.02, XL + 0.06, 1.20, 2.20, 2.28, 2.31, M["blackmetal"])
llave = box("Llave de luz", 1.00 + 0.05, 1.00 + 0.13, 0.0, 0.015, 1.15, 1.27, M["white"])
interactive(llave, "light", "Llave de luz")
for name, (x, y, z) in {"luz_arana": (0, CHY, 2.70), "luz_cocina": (XL + 0.4, 1.6, 2.2), "luz_bano": (0.6, L - 0.4, 1.9),
                        "luz_altillo": (0, 5.2, 3.1), "luz_frente": (0.5, -0.6, 2.1)}.items():
    e = bpy.data.objects.new(name, None)
    e.location = (x, y, z)
    e["light_point"] = 1
    link(e)
# punto de partida de la cámara
spawn = bpy.data.objects.new("spawn", None); spawn.location = (0.55, -4.5, 0.0); spawn["spawn"] = 1; link(spawn)
loftspot = bpy.data.objects.new("loft_spot", None); loftspot.location = (0.0, 4.48, LOFT_Z + 0.08); loftspot["loft_spot"] = 1; link(loftspot)
downspot = bpy.data.objects.new("down_spot", None); downspot.location = (0.2, 3.4, 0.0); downspot["down_spot"] = 1; link(downspot)

# ----------------------------------------------------------------- export
os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "minicasa.blend"))
bpy.ops.export_scene.gltf(
    filepath=os.path.join(OUT, "minicasa.glb"), export_format="GLB", export_extras=True,
    export_apply=True, export_image_format="JPEG", export_jpeg_quality=85, export_lights=False,
)
n = sum(1 for o in bpy.data.objects if o.type == "MESH")
ni = sum(1 for o in bpy.data.objects if "interact" in o.keys())
print(f"OK objetos={n} interactivos={ni}")
