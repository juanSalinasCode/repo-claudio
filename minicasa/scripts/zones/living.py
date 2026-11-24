# Zona: living. Se ejecuta en el espacio de nombres compartido de core.py (ver build.py).
# Heladera retro + freezer, mesa y sillas plegables (guardadas entre heladera y tabique), sillón, split, tablero.
# Todas las posiciones son relativas a XL, XR, BATH_Y, LOFT_Z, EAVE y al fin de la mesada de la cocina (KY1).
# Colores muestreados de los fotogramas (sRGB mediana -> lineal): heladera f0097/f0100 (168,207,204),
# tapizado f0106/f0109 (40,74,87), pino escalera f0106 (189,154,115), listones sillas f0115 (95,62,40).
# =================================================================== HELADERA, MESA, SILLAS
CUR[0] = "Living"

M["mint"] = mat("Verde agua heladera v2", (0.40, 0.62, 0.60), rough=0.25)
M["teal"] = mat("Tapizado turquesa v2", (0.022, 0.068, 0.095), rough=0.95)
M_chrome = mat("Cromo", (0.85, 0.86, 0.88), rough=0.12, metal=1.0)
M_gasket = mat("Burlete gris", (0.55, 0.60, 0.60), rough=0.6)
M_slat = mat("Listones acacia", (0.115, 0.050, 0.022), rough=0.6)
M_logo = mat("Logo heladera", (0.40, 0.62, 0.60), tex="living_logo.jpg", rough=0.25)
M_pillow = mat("Almohadon elefante", (0.9, 0.9, 0.88), tex="living_almohadon.jpg", rough=0.95)
M_fleece = mat("Manta piel blanca", (0.90, 0.88, 0.84), rough=1.0)
M_display = mat("Display tablero", (0.10, 0.35, 0.85), rough=0.3, emit=(0.1, 0.3, 0.9), emit_strength=0.5)
M_leg = mat("Patas madera", (0.38, 0.20, 0.08), rough=0.5)


def decal(name, plane, c, a0, a1, b0, b1, m_, facing=+1):
    """Calcomanía de un quad con UV 0..1 (u de a0 a a1, v de b0 a b1).
    plane='x': quad en x=c (a=y, b=z); plane='y': quad en y=c (a=x, b=z). facing: signo de la normal."""
    bm = bmesh.new()
    uv = bm.loops.layers.uv.verify()
    P = (lambda a, b: (c, a, b)) if plane == "x" else (lambda a, b: (a, c, b))
    corners = [((a0, b0), (0, 0)), ((a1, b0), (1, 0)), ((a1, b1), (1, 1)), ((a0, b1), (0, 1))]
    vs = [bm.verts.new(P(*ab)) for ab, _ in corners]
    f = bm.faces.new(vs)
    f.normal_update()
    nidx = 0 if plane == "x" else 1
    if f.normal[nidx] * facing < 0:
        f.normal_flip()
    for lp in f.loops:
        k = min(range(4), key=lambda i: (lp.vert.co - Vector(P(*corners[i][0]))).length)
        lp[uv].uv = corners[k][1]
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    me.materials.append(m_)
    return link(bpy.data.objects.new(name, me))


def add_cyl(bm, axis, a, b, s0, s1, r, pivot, segs=12, mi=0):
    """Cilindro dentro de un bmesh (axis 'y': centro (x=a, z=b), de y=s0 a s1; axis 'x': centro (y=a, z=b))."""
    res = bmesh.ops.create_cone(bm, cap_ends=True, segments=segs, radius1=r, radius2=r, depth=s1 - s0)
    vs = res["verts"]
    rot = Matrix.Rotation(math.pi / 2, 3, "X" if axis == "y" else "Y")
    bmesh.ops.rotate(bm, verts=vs, matrix=rot)
    if axis == "y":
        c = Vector((a, (s0 + s1) / 2, b))
    else:
        c = Vector(((s0 + s1) / 2, a, b))
    bmesh.ops.translate(bm, verts=vs, vec=c - Vector(pivot))
    for f in {f for v in vs for f in v.link_faces}:
        f.material_index = mi


# ------------------------------------------------------------------ heladera retro (tipo Galanz/Classic)
# Contra la pared izquierda, pegada al final de la mesada; frente hacia el pasillo (+x).
# Posiciones del presupuesto de paredes definido en cocina.py (FRIDGE_Y0/Y1, SOFA_*, PY, STORE_Y1).
FW, FD, FH = FRIDGE_Y1 - FRIDGE_Y0, 0.60, 1.47   # ancho (y), profundidad (x), alto
FX0 = XL + 0.04
FX1 = FX0 + FD                          # plano de las puertas
# En el video la heladera está pegada a la mesada y deja ~0.5 m hasta el tabique para guardar mesa y sillas.
# La auditoría con cámaras (heladera1/2) confirma que va pegada a la mesada: se ancla a KY1.
FY0, FY1 = FRIDGE_Y0, FRIDGE_Y1
FZ0 = 0.06                              # zócalo
FZ_D = 0.60                             # división freezer (abajo) / heladera (arriba)
RR = 0.06                               # radio de los cantos superiores redondeados
DT = 0.055                              # espesor de puerta
# carcasa: laterales + fondo + techo con cantos redondeados (cilindros a lo largo de y y de x)
bm = bmesh.new()
for (x0, x1, y0, y1, z0, z1) in [(FX0, FX1, FY0, FY0 + 0.03, FZ0, FH - RR), (FX0, FX1, FY1 - 0.03, FY1, FZ0, FH - RR),
                                 (FX0, FX0 + 0.03, FY0, FY1, FZ0, FH - RR), (FX0 + RR, FX1 - 0.005, FY0 + RR, FY1 - RR, FH - 0.03, FH),
                                 (FX0 + RR, FX1 - 0.005, FY0, FY1, FH - RR, FH - 0.03), (FX0, FX0 + RR, FY0 + RR, FY1 - RR, FH - RR, FH - 0.03),
                                 (FX0, FX1, FY0, FY1, FZ_D - 0.02, FZ_D + 0.02), (FX0, FX1, FY0, FY1, FZ0, FZ0 + 0.03)]:
    add_box(bm, x0, x1, y0, y1, z0, z1)
add_cyl(bm, "x", FY0 + RR, FH - RR, FX0 + RR, FX1 - 0.005, RR, (0, 0, 0))
add_cyl(bm, "x", FY1 - RR, FH - RR, FX0 + RR, FX1 - 0.005, RR, (0, 0, 0))
add_cyl(bm, "y", FX0 + RR, FH - RR, FY0 + RR, FY1 - RR, RR, (0, 0, 0))
bm.normal_update()
make_obj("Heladera cuerpo", bm, [M["mint"]])
box("Heladera zocalo", FX0 + 0.04, FX1 - 0.04, FY0 + 0.03, FY1 - 0.03, 0.0, FZ0, M["black"])
_e = 0.006                              # revestimiento interior (hueco, no macizo)
_lin_parts = []
for (za, zb) in [(FZ0 + 0.032, FZ_D - 0.022), (FZ_D + 0.022, FH - 2 * RR - 0.004)]:
    _lin_parts += [(FX0 + 0.032, FX0 + 0.032 + _e, FY0 + 0.032, FY1 - 0.032, za, zb, 0),           # fondo
                   (FX0 + 0.032 + _e, FX1 - 0.012, FY0 + 0.032, FY0 + 0.032 + _e, za, zb, 0),     # laterales
                   (FX0 + 0.032 + _e, FX1 - 0.012, FY1 - 0.032 - _e, FY1 - 0.032, za, zb, 0),
                   (FX0 + 0.032 + _e, FX1 - 0.012, FY0 + 0.032 + _e, FY1 - 0.032 - _e, za, za + _e, 0),   # piso
                   (FX0 + 0.032 + _e, FX1 - 0.012, FY0 + 0.032 + _e, FY1 - 0.032 - _e, zb - _e, zb, 0)]   # techo
multi("Heladera interior", _lin_parts, [M["fridge_in"]])
for k, z in enumerate([0.88, 1.12]):
    box(f"Heladera estante {k}", FX0 + 0.06, FX1 - 0.06, FY0 + 0.04, FY1 - 0.04, z, z + 0.008, M["glass"])
# (los estantes apoyan en los laterales del revestimiento: 2 mm de luz)
box("Freezer cajon interior", FX0 + 0.08, FX1 - 0.04, FY0 + 0.05, FY1 - 0.05, FZ0 + 0.04, FZ_D - 0.12, M["glass"])
# puerta superior: bisagra en el canto y=FY1 (hacia el tabique), abre hacia el pasillo (como en f0094)
bm = bmesh.new(); pv = (FX1 + DT, FY1, FZ_D + 0.02)
add_box(bm, FX1 + 0.002, FX1 + DT, FY0, FY1, FZ_D + 0.025, FH - DT / 2, pivot=pv)
add_cyl(bm, "y", FX1 + 0.002 + (DT - 0.002) / 2, FH - DT / 2, FY0, FY1, (DT - 0.002) / 2, pv)   # canto superior curvo
add_box(bm, FX1 + 0.0, FX1 + 0.002, FY0 + 0.01, FY1 - 0.01, FZ_D + 0.04, FH - 0.04, pivot=pv, mi=2)   # burlete
# manija cromada horizontal abajo a la izquierda (lado de la mesada) + soportes
hz = FZ_D + 0.12
add_box(bm, FX1 + DT + 0.035, FX1 + DT + 0.05, FY0 + 0.05, FY0 + 0.26, hz - 0.012, hz + 0.012, pivot=pv, mi=1)
add_box(bm, FX1 + DT, FX1 + DT + 0.04, FY0 + 0.05, FY0 + 0.07, hz - 0.01, hz + 0.01, pivot=pv, mi=1)
add_box(bm, FX1 + DT, FX1 + DT + 0.04, FY0 + 0.24, FY0 + 0.26, hz - 0.01, hz + 0.01, pivot=pv, mi=1)
# barra cromada del logo
add_box(bm, FX1 + DT, FX1 + DT + 0.006, FY0 + 0.05, FY0 + 0.33, FH - 0.215, FH - 0.205, pivot=pv, mi=1)
bm.normal_update()
pu = make_obj("Heladera puerta", bm, [M["mint"], M_chrome, M_gasket], pv)
interactive(pu, "rot", "Puerta de la heladera", axis="Z", angle=100)
lg = decal("Heladera logo", "x", FX1 + DT + 0.007, FY0 + 0.06, FY0 + 0.32, FH - 0.25, FH - 0.17, M_logo)
lg.parent = pu
lg.matrix_parent_inverse = pu.matrix_basis.inverted()
# freezer: puerta inferior con la misma bisagra (en el video se abre como puerta, con cajones transparentes adentro)
bm = bmesh.new(); pv = (FX1 + DT, FY1, FZ0)
add_box(bm, FX1 + 0.002, FX1 + DT, FY0, FY1, FZ0 + 0.005, FZ_D - 0.025, pivot=pv)
add_box(bm, FX1 + 0.0, FX1 + 0.002, FY0 + 0.01, FY1 - 0.01, FZ0 + 0.03, FZ_D - 0.04, pivot=pv, mi=2)
hz = FZ_D - 0.10
add_box(bm, FX1 + DT + 0.035, FX1 + DT + 0.05, FY0 + 0.05, FY0 + 0.24, hz - 0.012, hz + 0.012, pivot=pv, mi=1)
add_box(bm, FX1 + DT, FX1 + DT + 0.04, FY0 + 0.05, FY0 + 0.07, hz - 0.01, hz + 0.01, pivot=pv, mi=1)
add_box(bm, FX1 + DT, FX1 + DT + 0.04, FY0 + 0.22, FY0 + 0.24, hz - 0.01, hz + 0.01, pivot=pv, mi=1)
bm.normal_update()
fz = make_obj("Freezer", bm, [M["mint"], M_chrome, M_gasket], pv)
interactive(fz, "rot", "Freezer (puerta inferior)", axis="Z", angle=90)
box("Heladera cartel", FX0 + 0.20, FX0 + 0.34, FY0 - 0.002, FY0, FH - 0.32, FH - 0.16, M["white"])   # papelito en el lateral

# ------------------------------------------------------------------ mesa y sillas plegables (grupo "mesa")
# Guardadas de pie en el hueco entre el lateral de la heladera (FY1) y el tabique del baño (como en f0112-f0124):
# la mesa plegada contra el tabique y las dos sillas plegadas delante.
# PY (cara del tabique con el mural) y STORE_Y1 vienen de cocina.py. La hoja granero abierta barre y 3.73-3.80
# hasta x=XL, así que mesa y sillas se guardan delante (y <= STORE_Y1).
TY = STORE_Y1 - 0.20                    # (constante compartida) zona de guardado de mesa/sillas
SOX0, SOX1 = SOFA_X0, SOFA_X1           # sillón (ver abajo)
SOY0, SOY1 = SOFA_Y0, SOFA_Y1
SY_ = STORE_Y1                          # cara trasera del paquete mesa plegada
TOP = 0.60                              # tapa cuadrada de listones 60x60
# mesa abierta: en el pasillo, delante del sillón
MCX = (FX1 + DT + SOX0) / 2; MCY = STORE_Y1 - 0.63; MZ = 0.72   # en el pasillo frente al sillón; la silla del fondo queda delante de la hoja granero
# mesa plegada (estado inicial): tapa vertical contra el tabique, apoyada en el piso, patas plegadas detrás
pv = (XL + 0.015 + TOP / 2, SY_ - 0.05, 0.10 + TOP / 2)
bm = bmesh.new()
n_sl = 9
for k in range(n_sl):
    z0 = 0.10 + k * TOP / n_sl
    add_box(bm, XL + 0.015, XL + 0.015 + TOP, SY_ - 0.06, SY_ - 0.04, z0 + 0.006, z0 + TOP / n_sl - 0.006, pivot=pv)
for x0 in (XL + 0.035, XL + 0.015 + TOP - 0.06):      # travesaños bajo la tapa + patas plegadas
    add_box(bm, x0, x0 + 0.04, SY_ - 0.04, SY_ - 0.02, 0.10, 0.10 + TOP, pivot=pv)
    add_box(bm, x0 + 0.005, x0 + 0.035, SY_ - 0.02, SY_ + 0.0, 0.0, 0.10 + TOP + 0.08, pivot=pv)
bm.normal_update()
mesa = make_obj("Mesa plegable", bm, [M_slat], pv)
interactive(mesa, "combo", "Mesa plegable", group="mesa", axis="X", angle=-90,
            vec=(MCX - pv[0], MCY - pv[1], MZ - 0.02 - pv[2]))
# patas abiertas en X (solo visibles con la mesa armada); conserva el nombre "Mensula mesa"
legs = []
for dx in (-TOP / 2 + 0.05, TOP / 2 - 0.08):
    for s_ in (-1, 1):
        for t in range(6):
            yy = MCY + s_ * (0.24 - t * 0.04)
            zz = t * (MZ - 0.09) / 6
            legs.append((MCX + dx, MCX + dx + 0.03, yy - 0.025, yy + 0.025, zz, zz + (MZ - 0.09) / 6 + 0.01, 0))
legs.append((MCX - TOP / 2 + 0.05, MCX + TOP / 2 - 0.05, MCY - 0.015, MCY + 0.015, 0.30, 0.33, 0))
mens = multi("Mensula mesa", legs, [M_slat])
interactive(mens, "vis", "Mesa plegable", group="mesa", extra={"vis_state": "open"})


def chair_folded(name, y0):
    """Silla bistro plegada: paquete plano de ~6 cm, de pie (plano XZ)."""
    x0 = XL + 0.12
    parts = [(x0, x0 + 0.03, y0, y0 + 0.03, 0.0, 0.86, 0), (x0 + 0.39, x0 + 0.42, y0, y0 + 0.03, 0.0, 0.86, 0)]
    parts += [(x0 + 0.03, x0 + 0.39, y0, y0 + 0.02, 0.60 + k * 0.07, 0.65 + k * 0.07, 0) for k in range(4)]   # respaldo
    parts += [(x0 + 0.03, x0 + 0.39, y0 + 0.03, y0 + 0.05, 0.12 + k * 0.065, 0.17 + k * 0.065, 0) for k in range(6)]  # asiento plegado
    parts += [(x0 + 0.03, x0 + 0.06, y0 + 0.03, y0 + 0.06, 0.0, 0.52, 0), (x0 + 0.36, x0 + 0.39, y0 + 0.03, y0 + 0.06, 0.0, 0.52, 0)]
    return multi(name, parts, [M_slat])


def chair_open(name, cx, cy, face):
    """Silla bistro abierta. face=+1: el que se sienta mira hacia +y (respaldo en y-)."""
    w, d = 0.21, 0.21
    by = cy - face * d                   # línea del respaldo
    parts = [(cx - w, cx + w, cy - d + 0.01 + k * 0.07, cy - d + 0.06 + k * 0.07, 0.44, 0.465, 0) for k in range(6)]
    for sx in (-1, 1):
        x = cx + sx * (w - 0.015)
        parts.append((x - 0.015, x + 0.015, min(by, by - face * 0.03), max(by, by - face * 0.03), 0.0, 0.88, 0))  # pata trasera/respaldo
        fy = cy + face * (d - 0.02)
        parts.append((x - 0.015, x + 0.015, fy - 0.015, fy + 0.015, 0.0, 0.44, 0))                             # pata delantera
    for k in range(4):
        parts.append((cx - w, cx + w, min(by, by - face * 0.02), max(by, by - face * 0.02), 0.60 + k * 0.07, 0.65 + k * 0.07, 0))
    return multi(name, parts, [M_slat])


for j in range(2):
    pl = chair_folded(f"Silla plegada {j + 1}", SY_ - 0.13 - j * 0.07)
    interactive(pl, "vis", f"Silla plegable {j + 1}", group="mesa", extra={"vis_state": "closed"})
    face = 1 if j == 0 else -1
    ab = chair_open(f"Silla abierta {j + 1}", MCX, MCY - face * (TOP / 2 + 0.12), face)
    interactive(ab, "vis", f"Silla plegable {j + 1}", group="mesa", extra={"vis_state": "open"})

# ------------------------------------------------------------------ sillón turquesa tipo loveseat (pared derecha)
# Respaldo contra la pared derecha, termina junto al tabique; apoyabrazos curvos tipo "tub", patas de madera abiertas.
SZ_SEAT, SZ_BASE, SZ_BACK, SZ_ARM = 0.45, 0.17, 0.74, 0.62   # respaldo bajo tipo "tub": las pedadas pasan por encima
AR = 0.08                                # radio de los rollos (apoyabrazos/respaldo)
bm = bmesh.new()
add_box(bm, SOX0 + 0.02, SOX1, SOY0, SOY1, SZ_BASE, SZ_SEAT - 0.10)                       # base
add_box(bm, SOX0 + 0.04, SOX1 - 0.16, SOY0 + 0.15, SOY1 - 0.15, SZ_SEAT - 0.10, SZ_SEAT)   # almohadón de asiento
add_box(bm, SOX1 - 0.18, SOX1, SOY0, SOY1, SZ_SEAT - 0.10, SZ_BACK - AR)                  # respaldo
add_cyl(bm, "y", SOX1 - 0.095, SZ_BACK - AR, SOY0 + AR, SOY1 - AR, 0.09, (0, 0, 0), segs=12)
for (y0, y1) in [(SOY0, SOY0 + 0.15), (SOY1 - 0.15, SOY1)]:                               # apoyabrazos
    add_box(bm, SOX0 + 0.02, SOX1, y0, y1, SZ_SEAT - 0.10, SZ_ARM - AR)
    add_cyl(bm, "x", (y0 + y1) / 2, SZ_ARM - AR, SOX0 + 0.02, SOX1 - 0.09, 0.075, (0, 0, 0), segs=12)
    # transición curva apoyabrazos -> respaldo
    add_box(bm, SOX1 - 0.18, SOX1, y0, y1, SZ_ARM - AR, SZ_BACK - AR)
bm.normal_update()
make_obj("Sillon", bm, [M["teal"]])
for (x, y, sx, sy) in [(SOX0 + 0.10, SOY0 + 0.10, -1, -1), (SOX0 + 0.10, SOY1 - 0.10, -1, 1),
                       (SOX1 - 0.10, SOY0 + 0.10, 1, -1), (SOX1 - 0.10, SOY1 - 0.10, 1, 1)]:
    p = cone("Pata sillon", x + sx * 0.02, y + sy * 0.02, 0.0, SZ_BASE, 0.012, 0.022, M_leg, verts=8)
    p.rotation_euler = (math.radians(-sy * 10), math.radians(sx * 10), 0)
# almohadones: 1 blanco liso al fondo + 2 estampados con elefante (textura real f0106), apoyados en el respaldo
_pw = (SOY1 - SOY0 - 0.30 - 0.04) / 3     # 3 almohadones entre los apoyabrazos, sin superponerse
for k, (y0, y1, m_) in enumerate([(SOY1 - 0.16 - _pw, SOY1 - 0.16, M["white"]),
                                  (SOY1 - 0.18 - 2 * _pw, SOY1 - 0.18 - _pw, M_pillow),
                                  (SOY0 + 0.16, SOY0 + 0.16 + _pw, M_pillow)]):
    xb = SOX1 - 0.20 - k * 0.015
    box(f"Almohadon {k + 1}", xb - 0.14, xb, y0, y1, SZ_SEAT + 0.012, SZ_SEAT + 0.43, M["white"])
    if m_ is M_pillow:
        decal(f"Almohadon {k + 1} estampado", "x", xb - 0.141, y1 - 0.02, y0 + 0.02, SZ_SEAT + 0.02, SZ_SEAT + 0.42, M_pillow, facing=-1)
# manta de piel blanca sobre el apoyabrazos del fondo (f0171)
box("Manta sillon", SOX0 + 0.10, SOX1 - 0.19, SOY1 - 0.15, SOY1, SZ_ARM + 0.002, SZ_ARM + 0.06, M_fleece)
box("Manta sillon caida", SOX1 - 0.17, SOX1 - 0.02, SOY1 - 0.15, SOY1, SZ_BACK + 0.02, SZ_BACK + 0.07, M_fleece)

# ------------------------------------------------------------------ aire acondicionado split (pared izquierda, alto)
SPZ1 = EAVE - 0.06
bm = bmesh.new()
add_box(bm, XL, XL + 0.20, FY0 - 0.45, FY0 + 0.40, SPZ1 - 0.28, SPZ1 - 0.06)
add_cyl(bm, "y", XL + 0.14, SPZ1 - 0.08, FY0 - 0.45, FY0 + 0.40, 0.06, (0, 0, 0), segs=10)
add_box(bm, XL, XL + 0.14, FY0 - 0.45, FY0 + 0.40, SPZ1 - 0.08, SPZ1)
bm.normal_update()
make_obj("Split AA", bm, [M["white"]])
box("Split AA rejilla", XL + 0.12, XL + 0.205, FY0 - 0.42, FY0 + 0.37, SPZ1 - 0.285, SPZ1 - 0.27, M["gray"])

# ------------------------------------------------------------------ tablero eléctrico sobre el mural (izq. de la puerta granero)
_bd0 = globals().get("BATH_DOOR", (-0.30, 0.48, 0, 2))[0]
TBX0, TBX1 = _bd0 - 0.33, _bd0 - 0.10
box("Tablero electrico", TBX0, TBX1, PY - 0.03, PY, 1.22, 1.60, M["panel"])
box("Tablero display", TBX0 + 0.04, TBX1 - 0.04, PY - 0.032, PY - 0.03, 1.48, 1.55, M_display)
box("Tablero termica", TBX0 + 0.06, TBX1 - 0.06, PY - 0.045, PY - 0.03, 1.30, 1.40, M["gray"])
