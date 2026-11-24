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
    m.diffuse_color = (*color, alpha)          # color visible en Workbench (auditoría)
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

