# Zona: bano. Se ejecuta en el espacio de nombres compartido de core.py (ver build.py).
# =================================================================== BAÑO
# Distribución según el video (f0125–f0165), mirando desde la puerta hacia el fondo (+y):
#   - izquierda (pared XL): inodoro junto al tabique, mirando a +x; ducha neo-angular en la esquina (XL, L)
#     con la puerta en la cara a 45°, bisagra en el extremo delantero, abre hacia afuera (+x, −y).
#   - derecha (pared XR): toallero/estante negro junto al tabique, vanitorio abierto de madera hasta el
#     fondo; encima espejo de marco negro + barra de lamparitas; ventana de la pared XR al fondo.
#   - pared del fondo (y=L), lado derecho: estante de madera abierto con ganchos negros.
# Todo se expresa respecto de XL, XR, L, BATH_Y, LOFT_Z, BATH_DOOR y RIGHT_WINS.
CUR[0] = "Baño"

def _bb(name, default):
    """Caja envolvente (xmin,xmax,ymin,ymax,zmin,zmax) de un objeto ya creado por otra zona."""
    ob = bpy.data.objects.get(name)
    if not ob or ob.type != "MESH" or not ob.data.vertices:
        return default
    cs = [ob.location + v.co for v in ob.data.vertices]   # matrix_world aún no está actualizada
    return (min(c.x for c in cs), max(c.x for c in cs), min(c.y for c in cs), max(c.y for c in cs),
            min(c.z for c in cs), max(c.z for c in cs))

def seg_box(bm, p0, p1, th, z0, z1, pivot=(0, 0, 0), mi=0, inset=0.0):
    """Caja de espesor th a lo largo del segmento p0→p1 (planta), de z0 a z1."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    ln = math.hypot(dx, dy)
    ux, uy = dx / ln, dy / ln
    nx, ny = -uy, ux
    a0, a1 = inset, ln - inset
    res = bmesh.ops.create_cube(bm, size=1.0)
    for v in res["verts"]:
        s = a0 if v.co.x < 0 else a1
        t = -th / 2 if v.co.y < 0 else th / 2
        v.co.x = p0[0] + ux * s + nx * t - pivot[0]
        v.co.y = p0[1] + uy * s + ny * t - pivot[1]
        v.co.z = (z0 if v.co.z < 0 else z1) - pivot[2]
    for f in {f for v in res["verts"] for f in v.link_faces}:
        f.material_index = mi

def poly_z(name, pts, z0, z1, m_):
    """Polígono en planta (XY) extruido en Z."""
    bm = bmesh.new()
    b = [bm.verts.new((x, y, z0)) for x, y in pts]
    t = [bm.verts.new((x, y, z1)) for x, y in pts]
    bm.faces.new(b[::-1]); bm.faces.new(t)
    n = len(pts)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new([b[i], b[j], t[j], t[i]])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.normal_update()
    return make_obj(name, bm, [m_], (0, 0, 0))

def scale_mesh(ob, sx=1, sy=1, sz=1):
    ob.data.transform(Matrix.Diagonal((sx, sy, sz, 1.0)))

# ----------------------------------------------------------------- materiales (muestreados del video)
M_door = mat("Pino puerta granero", (0.74, 0.58, 0.40), tex="bano_granero.jpg", rough=0.6)
M_wood = mat("Madera vanitorio", (0.62, 0.38, 0.20), tex="bano_madera.jpg", rough=0.55)
M_marb = mat("Marmol baño", (0.80, 0.80, 0.80), tex="bano_marmol.jpg", rough=0.2)
M_sink = mat("Bacha negra brillante", (0.015, 0.014, 0.018), rough=0.08)
M_chrome = mat("Perfil cromado", (0.80, 0.81, 0.83), rough=0.18, metal=1.0)
M_shbase = mat("Plato ducha", (0.95, 0.95, 0.95), rough=0.3)
M_tw1 = mat("Toalla azul petroleo", (0.10, 0.28, 0.34), rough=0.95)
M_tw2 = mat("Toalla azul marino", (0.08, 0.11, 0.20), rough=0.95)
M_tw3 = mat("Toalla celeste", (0.45, 0.70, 0.82), rough=0.95)
M_twg = mat("Toalla rayada gris", (0.55, 0.58, 0.62), rough=0.95)
M_mirror = mat("Espejo", (0.80, 0.84, 0.86), rough=0.02, metal=1.0)

# piso de mármol con textura real (el objeto lo crea estructura)
pb = bpy.data.objects.get("Piso baño")
if pb:
    pb.data.materials[0] = M_marb
# paredes del baño: en el video son paneles lisos blancos (el machimbre sólo está en el cielorraso)
M_wallb = mat("Panel blanco baño", (0.90, 0.90, 0.90), rough=0.4)
for n_ in ("Baño revest izq", "Baño revest der", "Baño revest fondo"):
    ob_ = bpy.data.objects.get(n_)
    if ob_:
        ob_.data.materials[0] = M_wallb

# referencias de la estructura
PF = _bb("Tabique baño", (XL, XR, BATH_Y - 0.08, BATH_Y, 0, LOFT_Z))[2]          # cara living del tabique
VIGA_Y = _bb("Viga altillo", (XL, XR, BATH_Y - 0.12, BATH_Y - 0.06, 0, 0))[2]      # frente de la viga/cenefa
BD = BATH_DOOR
BY = BATH_Y                     # cara del tabique del lado baño
DEPTH = L - BY                  # profundidad interior del baño
# ventana del baño en la pared XR (la que cae entre BATH_Y y L)
BWIN = next(((i, w) for i, w in enumerate(RIGHT_WINS) if BY < (w[0] + w[1]) / 2 < L), None)

# =================================================================== PUERTA GRANERO (lado living)
# Tablón de pino claro (3 tablas verticales), cuelga de dos herrajes negros tipo "strap" con ruedas
# sobre un riel negro plano bajo la cenefa del altillo. Abre deslizando hacia −x (hacia el tablero eléctrico).
old = bpy.data.objects.get("Riel granero")
if old:
    bpy.data.objects.remove(old)
DX0 = BD[0] - 0.06                          # en f0110 la hoja cerrada deja ver la jamba derecha:
DW = BD[1] - DX0                            # solapa sólo del lado izquierdo (hacia donde abre)
DZ1 = LOFT_Z - 0.11                         # borde superior de la hoja
RZ0, RZ1 = LOFT_Z - 0.075, LOFT_Z - 0.035   # riel (planchuela 4 cm)
RY0, RY1 = VIGA_Y - 0.012, VIGA_Y           # riel atornillado a la cenefa
DY1 = RY0 - 0.006                           # cara trasera de la hoja (lo más pegada posible al tabique:
                                            # delante quedan el sillón y las sillas colgadas)
DY0 = DY1 - 0.038                           # hoja 38 mm
box("Riel granero", XL + 0.005, BD[1] + 0.30, RY0, RY1, RZ0, RZ1, M["blackmetal"])
for k, x in enumerate((XL + 0.06, BD[0] - 0.20, BD[1] + 0.24)):     # bulones (cabeza delante del riel, bajo las ruedas)
    cyl(f"Soporte riel {k}", x, RY0 - 0.0035, RZ0 + 0.005, RZ0 + 0.020, 0.0075, M["blackmetal"], verts=8)
bm = bmesh.new(); pv = (DX0, DY0, 0.0)
NB = 3
for k in range(NB):
    add_box(bm, DX0 + k * DW / NB + (0.002 if k else 0), DX0 + (k + 1) * DW / NB - 0.002, DY0, DY1, 0.015, DZ1, pivot=pv)
for k, xs in enumerate((DX0 + 0.16, DX0 + DW - 0.20)):       # herrajes: planchuela + rueda
    add_box(bm, xs, xs + 0.04, DY0 - 0.008, DY0, DZ1 - 0.30, DZ1, pivot=pv, mi=1)
    add_box(bm, xs, xs + 0.04, DY0 - 0.008, RY0 - 0.004, DZ1, RZ1 + 0.03, pivot=pv, mi=1)
    add_box(bm, xs - 0.025, xs + 0.065, RY0 - 0.015, RY0 - 0.004, RZ1 - 0.01, RZ1 + 0.06, pivot=pv, mi=1)
add_box(bm, DX0 + 0.05, DX0 + 0.07, DY0 - 0.035, DY0, 0.90, 1.20, pivot=pv, mi=1)         # tirador
add_box(bm, DX0 + DW - 0.07, DX0 + DW - 0.05, DY0 - 0.035, DY0, 0.90, 1.20, pivot=pv, mi=1)
bm.normal_update()
gran = make_obj("Puerta granero", bm, [M_door, M["blackmetal"]], pv)
# abre hacia −x hasta 1,5 cm de la pared XL (el hueco queda libre ≈55 cm: la pared no deja correrla más)
interactive(gran, "slide", "Puerta corrediza del baño", vec=(-(DX0 - (XL + 0.015)), 0, 0))
box("Guia piso granero", BD[0] + 0.0, BD[0] + 0.03, DY0 - 0.016, DY0 - 0.003, 0.0, 0.05, M["blackmetal"])
# contramarco de pino: jambas y dintel forrando el hueco + tapajuntas en ambas caras (envuelve el hueco
# sin atravesar el tabique; 1 mm de luz con el tabique)
CW, CT, e = 0.05, 0.015, 0.001
_mp = [(BD[0] + e, BD[0] + e + CT, PF + e, BY - e, 0, BD[3] - e, 0),
       (BD[1] - e - CT, BD[1] - e, PF + e, BY - e, 0, BD[3] - e, 0),
       (BD[0] + e, BD[1] - e, PF + e, BY - e, BD[3] - e - CT, BD[3] - e, 0)]
for ya, yb in ((PF - e - CT, PF - e), (BY + e, BY + e + CT)):
    _mp += [(BD[0] - CW, BD[0] + e + CT, ya, yb, 0, BD[3] + CW, 0), (BD[1] - e - CT, BD[1] + CW, ya, yb, 0, BD[3] + CW, 0),
            (BD[0] + e + CT, BD[1] - e - CT, ya, yb, BD[3] - e - CT, BD[3] + CW, 0)]
multi("Marco puerta baño", _mp, [M["pine"]])

# =================================================================== DUCHA NEO-ANGULAR (esquina XL, L)
SD = min(0.92, DEPTH - 0.62)     # lado del plato sobre cada pared
SR = 0.30                        # retornos fijos perpendiculares a las paredes
SZ0, SZ1 = 0.08, 1.95
P_A = (XL, L - SD)               # sobre la pared XL
P_B = (XL + SR, L - SD)          # bisagra de la puerta
P_C = (XL + SD, L - SR)          # lado manija
P_D = (XL + SD, L)               # sobre la pared del fondo
poly_z("Plato ducha", [(XL, L), P_A, P_B, P_C, P_D], 0.0, SZ0, M_shbase)
cyl("Rejilla ducha", XL + SD * 0.45, L - SD * 0.45, SZ0, SZ0 + 0.002, 0.04, M_chrome, verts=12)
# Vidrios fijos y perfiles a tope: cada perfil está en el BORDE del vidrio (arriba, abajo, contra la pared y
# en el parante de la bisagra/manija), con 1 mm de luz; ningún perfil cruza un vidrio.
PE, PT, PW = 0.022, 0.025, 0.02          # perfil: alto de los horizontales, ancho de los verticales, espesor
def _sub(p, q, s0, s1):
    ln = math.hypot(q[0] - p[0], q[1] - p[1]); ux_, uy_ = (q[0] - p[0]) / ln, (q[1] - p[1]) / ln
    return (p[0] + ux_ * s0, p[1] + uy_ * s0), (p[0] + ux_ * (ln - s1), p[1] + uy_ * (ln - s1))
bm = bmesh.new()
a_, b_ = _sub(P_A, P_B, 0.002 + PT + 0.001, 0.016 + 0.001)       # de la pared XL al parante de la bisagra
seg_box(bm, a_, b_, 0.008, SZ0 + 0.001 + PE + 0.001, SZ1 - PE - 0.001)
a_, b_ = _sub(P_C, P_D, 0.016 + 0.001, 0.002 + PT + 0.001)       # del parante de la manija a la pared del fondo
seg_box(bm, a_, b_, 0.008, SZ0 + 0.001 + PE + 0.001, SZ1 - PE - 0.001)
bm.normal_update()
make_obj("Ducha vidrio fijo", bm, [M["glass"]])
bm = bmesh.new()
for p, q, s0, s1 in ((P_A, P_B, 0.002 + PT + 0.001, 0.016), (P_C, P_D, 0.016, 0.002 + PT + 0.001)):
    a_, b_ = _sub(p, q, s0, s1)
    seg_box(bm, a_, b_, PW, SZ1 - PE, SZ1)                    # perfil superior (sobre el vidrio)
    seg_box(bm, a_, b_, PW, SZ0 + 0.001, SZ0 + 0.001 + PE)    # perfil inferior (bajo el vidrio)
seg_box(bm, P_B, P_C, PW, SZ1 - PE, SZ1, inset=0.016)         # dintel sobre la puerta
for p, q in ((P_A, P_B), (P_D, P_C)):                         # perfiles de pared (U) en el canto del vidrio
    a_, b_ = _sub(p, q, 0.002, 0.0)
    seg_box(bm, a_, (a_[0] + (b_[0] - a_[0]) * PT / math.dist(a_, b_), a_[1] + (b_[1] - a_[1]) * PT / math.dist(a_, b_)),
            PW, SZ0 + 0.001, SZ1)
for p in (P_B, P_C):                                          # parantes bisagra / manija
    add_box(bm, p[0] - 0.015, p[0] + 0.015, p[1] - 0.015, p[1] + 0.015, SZ0 + 0.001, SZ1)
bm.normal_update()
make_obj("Ducha perfiles", bm, [M_chrome])
# puerta: toda la cara a 45°, bisagra en P_B, abre hacia afuera (giro −Z)
bm = bmesh.new(); pv = (P_B[0], P_B[1], SZ0)
# vidrio enmarcado a tope por 4 perfiles (no lo cruzan)
seg_box(bm, P_B, P_C, 0.008, SZ0 + 0.056, SZ1 - 0.056, pivot=pv, inset=0.046)
for zz in ((SZ0 + 0.03, SZ0 + 0.055), (SZ1 - 0.055, SZ1 - 0.03)):
    seg_box(bm, P_B, P_C, 0.022, *zz, pivot=pv, mi=1, inset=0.025)
dl = math.hypot(P_C[0] - P_B[0], P_C[1] - P_B[1])
ux, uy = (P_C[0] - P_B[0]) / dl, (P_C[1] - P_B[1]) / dl
for s0, s1 in ((0.025, 0.045), (dl - 0.045, dl - 0.025)):
    seg_box(bm, (P_B[0] + ux * s0, P_B[1] + uy * s0), (P_B[0] + ux * s1, P_B[1] + uy * s1), 0.022, SZ0 + 0.056, SZ1 - 0.056, pivot=pv, mi=1)
hx, hy = P_B[0] + ux * (dl - 0.07), P_B[1] + uy * (dl - 0.07)
add_box(bm, hx - 0.02, hx + 0.02, hy - 0.02, hy + 0.02, 1.00, 1.04, pivot=pv, mi=1)      # pomo cromado
bm.normal_update()
mampara = make_obj("Mampara ducha", bm, [M["glass"], M_chrome], pv)
interactive(mampara, "rot", "Puerta de la ducha", axis="Z", angle=-85)
# grifería en la pared XL (dentro de la ducha): monocomando negro, brazo y flor, canasto colgante
SYC = L - SD * 0.5
box("Brazo ducha", XL, XL + 0.22, SYC - 0.012, SYC + 0.012, SZ1 + 0.06, SZ1 + 0.085, M["blackmetal"])
cyl("Flor ducha", XL + 0.22, SYC, SZ1 + 0.01, SZ1 + 0.05, 0.075, M["blackmetal"], verts=16)
grif = multi("Grifo ducha", [(XL, XL + 0.012, SYC - 0.06, SYC + 0.06, 1.04, 1.16, 0),
                             (XL + 0.012, XL + 0.07, SYC - 0.012, SYC + 0.012, 1.09, 1.11, 0)], [M["blackmetal"]])
interactive(grif, "water", "Abrir la ducha", group="agua_ducha")
multi("Canasto ducha", [(XL + 0.04, XL + 0.05, SYC - 0.13, SYC + 0.13, 1.30, 1.88, 0)] +
      [(XL + 0.05, XL + 0.16, SYC - 0.13, SYC + 0.13, z, z + 0.015, 0) for z in (1.35, 1.58)] +
      [(XL + 0.15, XL + 0.16, SYC - 0.13, SYC + 0.13, z, z + 0.07, 0) for z in (1.35, 1.58)], [M["blackmetal"]])
for k in range(3):
    cyl(f"Frasco ducha {k}", XL + 0.10, SYC - 0.07 + k * 0.07, 1.368, 1.50, 0.025, (M["white"], M_tw1, M["copper"])[k], verts=8)
agua_d = cyl("Agua ducha", XL + 0.22, SYC, SZ0, SZ1 + 0.01, 0.06, M["water"], verts=10)
agua_d["water_of"] = "agua_ducha"

# =================================================================== INODORO (pared XL, junto al tabique)
TYC = BY + min(0.40, (L - SD - BY) / 2)
box("Inodoro mochila", XL + 0.02, XL + 0.21, TYC - 0.21, TYC + 0.21, 0.40, 0.76, M["ceramic"])
box("Inodoro mochila tapa", XL + 0.01, XL + 0.23, TYC - 0.225, TYC + 0.225, 0.76, 0.79, M["ceramic"])
cyl("Inodoro boton", XL + 0.12, TYC, 0.79, 0.80, 0.02, M_chrome, verts=10)
TSX = 1.1                              # taza alargada en x (≈0,42 m de largo; total desde la pared ≈0,67 m)
HX = XL + 0.255                        # bisagra de la tapa: 2,5 cm delante de la mochila (abierta no la toca)
TBX = HX + 0.19 * TSX                  # centro de la taza
ped = cyl("Inodoro pie", TBX - 0.04, TYC, 0.0, 0.24, 0.12, M["ceramic"], verts=16)
scale_mesh(ped, 1.4, 1.0, 1.0)
taza = cyl("Inodoro taza", TBX, TYC, 0.24, 0.40, 0.19, M["ceramic"], verts=20)
scale_mesh(taza, TSX, 1.0, 1.0)
asi = cyl("Inodoro asiento", TBX, TYC, 0.40, 0.42, 0.19, M["white"], verts=20)
scale_mesh(asi, TSX, 1.0, 1.0)
hinge = (HX, TYC, 0.43)
tapa = cyl("Inodoro tapa", TBX, TYC, 0.42, 0.445, 0.19, M["white"], verts=20, pivot=hinge)
scale_mesh(tapa, TSX, 1.0, 1.0)
interactive(tapa, "rot", "Tapa del inodoro", axis="Y", angle=-92)
# portarrollos de pie cromado (entre inodoro y ducha, f0156)
PRY = min(TYC + 0.36, L - SD - 0.10)
cyl("Portarrollo base", XL + 0.14, PRY, 0.0, 0.02, 0.09, M_chrome, verts=12)
cyl("Portarrollo varilla", XL + 0.08, PRY, 0.02, 0.62, 0.008, M_chrome, verts=6)
cyl("Portarrollo", XL + 0.14, PRY - 0.06, 0.48, 0.58, 0.055, M["white"], verts=12, axis="Y")
cyl("Portarrollo reserva", XL + 0.14, PRY, 0.02, 0.30, 0.06, M["white"], verts=12)

# =================================================================== PARED XR: VANITORIO, ESPEJO, LUCES
VD = 0.50                       # profundidad del vanitorio (en x)
VY1 = L - 0.03
VY0 = max(BY + 0.48, VY1 - 1.30)     # f0144: la mesada va desde el toallero hasta el rincón del fondo
VX0, VX1 = XR - VD, XR - 0.01
VZ = 0.83
lg = 0.06
legs = [(x0, x0 + lg, y0, y0 + lg, 0.0, VZ - 0.05, 0) for x0 in (VX0 + 0.02, VX1 - lg - 0.01) for y0 in (VY0 + 0.02, VY1 - lg - 0.02)]
multi("Vanitorio", [(VX0, VX1, VY0, VY1, VZ - 0.05, VZ, 0),                         # tapa maciza
                    (VX0 + 0.04, VX1 - 0.02, VY0 + 0.04, VY1 - 0.04, 0.12, 0.15, 0),     # estante inferior
                    (VX0 + 0.02, VX0 + 0.04, VY0 + 0.08, VY1 - 0.08, VZ - 0.15, VZ - 0.05, 0),   # faldón frontal
                    (VX0 + 0.04, VX1 - 0.02, VY0 + 0.02, VY0 + 0.04, VZ - 0.15, VZ - 0.05, 0),
                    (VX0 + 0.04, VX1 - 0.02, VY1 - 0.04, VY1 - 0.02, VZ - 0.15, VZ - 0.05, 0)] + legs, [M_wood])
# toallas dobladas en el estante inferior
for k, mt in enumerate((M_twg, M["white"], M_twg)):
    y0 = VY0 + 0.10 + k * 0.28
    box(f"Toalla {k}", VX0 + 0.08, VX1 - 0.06, y0, y0 + 0.24, 0.153, 0.27 - 0.03 * (k == 1), mt)   # 3 mm sobre el estante
# bacha negra rectangular de apoyo + grifería de pared negra (pico + 2 llaves en cruz)
SYC2 = (BWIN[1][0] - 0.30) if BWIN else (VY0 + VY1) / 2   # bacha bajo el espejo, justo antes de la ventana
SX = XR - 0.27
multi("Bacha negra", [(SX - 0.18, SX + 0.18, SYC2 - 0.24, SYC2 + 0.24, VZ, VZ + 0.015, 0),
                      (SX - 0.18, SX - 0.165, SYC2 - 0.24, SYC2 + 0.24, VZ, VZ + 0.13, 0),
                      (SX + 0.165, SX + 0.18, SYC2 - 0.24, SYC2 + 0.24, VZ, VZ + 0.13, 0),
                      (SX - 0.165, SX + 0.165, SYC2 - 0.24, SYC2 - 0.225, VZ, VZ + 0.13, 0),
                      (SX - 0.165, SX + 0.165, SYC2 + 0.225, SYC2 + 0.24, VZ, VZ + 0.13, 0)], [M_sink])
FZ = VZ + 0.29
canilla_b = multi("Canilla baño", [(-0.03, 0.0, -0.03, 0.03, -0.03, 0.03),            # roseta
                                   (-0.20, -0.03, -0.011, 0.011, -0.011, 0.011),        # pico
                                   (-0.20, -0.18, -0.011, 0.011, -0.05, -0.011)],       # caída
                  [M["blackmetal"]], pivot=(0, 0, 0))
canilla_b.location = (XR - 0.01, SYC2, FZ)
interactive(canilla_b, "water", "Canilla del baño", group="agua_bano")
for k, dy in enumerate((-0.15, 0.15)):
    multi(f"Llave bacha {k}", [(XR - 0.05, XR - 0.01, SYC2 + dy - 0.02, SYC2 + dy + 0.02, FZ - 0.02, FZ + 0.02, 0),
                               (XR - 0.065, XR - 0.05, SYC2 + dy - 0.045, SYC2 + dy + 0.045, FZ - 0.008, FZ + 0.008, 0),
                               (XR - 0.065, XR - 0.05, SYC2 + dy - 0.008, SYC2 + dy + 0.008, FZ - 0.045, FZ + 0.045, 0)],
          [M["blackmetal"]])
agua_b = cyl("Agua baño", XR - 0.20, SYC2, VZ + 0.02, FZ - 0.05, 0.008, M["water"], verts=8)
agua_b["water_of"] = "agua_bano"
# accesorios sobre la mesada
box("Caja pañuelos", VX0 + 0.08, VX0 + 0.20, VY1 - 0.30, VY1 - 0.08, VZ, VZ + 0.10, mat("Caja celeste", (0.62, 0.78, 0.85)))
for k in range(2):
    cyl(f"Jabonera {k}", XR - 0.08, VY1 - 0.12 - k * 0.09, VZ, VZ + 0.16, 0.028, M["white"], verts=8)
box("Toallita mesada", VX0 + 0.05, VX0 + 0.25, SYC2 + 0.27, min(SYC2 + 0.45, VY1 - 0.32), VZ, VZ + 0.015, mat("Toallita verde agua", (0.55, 0.85, 0.80)))
# ventana XR del baño: marco interior blanco como en el video (la crea estructura)
if BWIN:
    WA, WB, WC, WD = BWIN[1]
    for suf in (" marco", " alfeizar"):
        ob = bpy.data.objects.get(f"Ventana der {BWIN[0]}{suf}")
        if ob:
            for i_ in range(len(ob.data.materials)):
                ob.data.materials[i_] = M["trim"]
    multi("Ventana baño hoja", [(XR + T / 2 - 0.03, XR + T / 2 - 0.01, WA + 0.002, WB - 0.002, (WC + WD) / 2 - 0.02, (WC + WD) / 2 + 0.02, 0)], [M["trim"]])
    MY1 = WA - 0.10
else:
    WA, WC, WD = VY1, 1.15, 1.85
    MY1 = VY1 - 0.30
# espejo grande de marco negro, sobre la mesada, entre la puerta y la ventana
MY0 = max(min(VY0 - 0.04, BY + 0.50) + 0.03, MY1 - 0.90)   # arranca después del toallero
MZ0, MZ1 = VZ + 0.33, min(VZ + 0.33 + 0.72, LOFT_Z - 0.18)
multi("Espejo baño marco", [(XR - 0.03, XR - 0.005, MY0, MY1, MZ0, MZ0 + 0.03, 0), (XR - 0.03, XR - 0.005, MY0, MY1, MZ1 - 0.03, MZ1, 0),
                            (XR - 0.03, XR - 0.005, MY0, MY0 + 0.03, MZ0, MZ1, 0), (XR - 0.03, XR - 0.005, MY1 - 0.03, MY1, MZ0, MZ1, 0)], [M["black"]])
box("Espejo baño", XR - 0.02, XR - 0.012, MY0 + 0.03, MY1 - 0.03, MZ0 + 0.03, MZ1 - 0.03, M_mirror)
# barra de luces: caño negro horizontal separado de la pared, con 5 portalámparas colgantes y lamparitas
LZ = MZ1 + 0.10
LY0, LY1 = MY0 - 0.02, MY1 + 0.05
cyl("Barra luces baño base", XR - 0.01, (LY0 + LY1) / 2, LZ, LZ + 0.02, 0.06, M["blackmetal"], verts=16, axis="X", pivot=None)
multi("Barra luces baño", [(XR - 0.16, XR - 0.14, LY0, LY1, LZ - 0.01, LZ + 0.01, 0),
                           (XR - 0.16, XR - 0.01, (LY0 + LY1) / 2 - 0.01, (LY0 + LY1) / 2 + 0.01, LZ - 0.01, LZ + 0.01, 0)], [M["blackmetal"]])
for k in range(5):
    y = LY0 + 0.06 + k * (LY1 - LY0 - 0.12) / 4
    cyl(f"Portalampara baño {k}", XR - 0.15, y, LZ - 0.10, LZ - 0.01, 0.017, M["blackmetal"], verts=8)
    sphere(f"Lamparita baño {k}", XR - 0.15, y, LZ - 0.14, 0.035, M["bulb"], seg=8)
box("Llave luz baño", XR - 0.012, XR - 0.002, MY1 + 0.02, MY1 + 0.08, MZ0 - 0.12, MZ0 - 0.02, M["black"])

# toallero / estante negro de metal (entre el tabique y el vanitorio): parantes + estantes con toallas
EY0, EY1 = BY + 0.05, min(VY0 - 0.04, BY + 0.50)
EX0, EX1 = XR - 0.40, XR - 0.03
if EY1 - EY0 > 0.25:
    parts = [(x, x + 0.025, y, y + 0.025, 0.0, LOFT_Z - 0.20, 0) for x in (EX0, EX1 - 0.025) for y in (EY0, EY1 - 0.025)]
    for z in (0.10, 0.50, 1.20):
        parts.append((EX0, EX1, EY0, EY1, z, z + 0.02, 0))   # toallas apoyadas encima (z+0.023)
    parts.append((EX0, EX0 + 0.02, EY0, EY1, 1.60, 1.62, 0))      # barra toallero
    parts.append((EX0, EX1, EY1 - 0.02, EY1, 0.80, 0.82, 0))      # barandita
    multi("Toallero escalera", parts, [M["blackmetal"]])
    for k, (z, mt) in enumerate(((0.12, M_tw3), (0.52, M_tw2), (1.22, M_tw1))):
        box(f"Toallas estante {k}", EX0 + 0.04, EX1 - 0.04, EY0 + 0.04, EY1 - 0.04, z + 0.003, z + 0.16, mt)

# =================================================================== PARED DEL FONDO: ESTANTE DE MADERA
SHX1 = XR - 0.38
SHX0 = SHX1 - 0.48
SHZ0, SHZ1 = 1.08, min(1.95, LOFT_Z - 0.12)
SHD = 0.13
parts = [(SHX0, SHX0 + 0.025, L - SHD, L, SHZ0, SHZ1, 0), (SHX1 - 0.025, SHX1, L - SHD, L, SHZ0, SHZ1, 0),
         (SHX0, SHX1, L - SHD, L, SHZ1 - 0.025, SHZ1, 0), (SHX0, SHX1, L - SHD, L, SHZ0, SHZ0 + 0.025, 0),
         (SHX0, SHX1, L - 0.015, L, SHZ0, SHZ1, 0)]
for k in range(1, 5):
    z = SHZ0 + k * (SHZ1 - SHZ0) / 5
    parts.append((SHX0, SHX1, L - SHD + 0.02, L, z, z + 0.018, 0))
    parts.append((SHX0, SHX1, L - SHD, L - SHD + 0.02, z, z + 0.05, 0))     # listón frontal
multi("Estante baño", parts, [M_wood])
for k, (x, z) in enumerate(((SHX0 - 0.06, SHZ1 + 0.02), (SHX1 + 0.03, SHZ0 + 0.10))):
    multi(f"Gancho baño {k}", [(x, x + 0.012, L - 0.012, L, z - 0.05, z, 0), (x, x + 0.012, L - 0.06, L - 0.012, z - 0.05, z - 0.04, 0),
                                (x, x + 0.012, L - 0.07, L - 0.06, z - 0.05, z - 0.01, 0)], [M["blackmetal"]])
