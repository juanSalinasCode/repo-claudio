# Zona: cocina. Se ejecuta en el espacio de nombres compartido de core.py (ver build.py).
# =================================================================== COCINA
# Referencias: f0026/f0034/f0054/f0060 (mesada vista desde el fondo), f0066/f0074 (bacha y ventana),
# f0080 (cajones), f0038/f0040/f0044/f0090 (mueble negro de cubos, pared derecha), f0012/f0014 (desde la puerta).
# Colores: medianas de píxeles en zonas limpias (ver audit/cocina.md), pasados a lineal.
# Todas las posiciones dependen de XL, XR, W, L, EAVE, FRONT_DOOR, FRONT_WIN, LEFT_WINS, RIGHT_WINS.
CUR[0] = "Cocina"

def _lin(r, g, b):
    """sRGB 0..255 -> lineal (lo que espera Base Color)."""
    f = lambda c: (c / 255 / 12.92) if c / 255 <= 0.04045 else ((c / 255 + 0.055) / 1.055) ** 2.4
    return (f(r), f(g), f(b))

MC = dict(
    wood=mat("Cerezo cocina", _lin(140, 66, 28), tex="cocina_mueble.jpg", rough=0.45),
    wood_dark=mat("Cerezo sombra", _lin(70, 30, 12), rough=0.6),
    counter=mat("Mesada maple", _lin(228, 204, 164), tex="cocina_mesada.jpg", rough=0.45),
    pull=mat("Tirador niquel", _lin(200, 200, 205), rough=0.3, metal=1.0),
    sink=mat("Bacha acero", _lin(150, 150, 155), rough=0.3, metal=1.0),
    sink_in=mat("Bacha fondo", _lin(60, 62, 66), rough=0.35, metal=0.8),
    rack=mat("Escurridor varillas", _lin(190, 190, 195), rough=0.3, metal=1.0),
    rack_edge=mat("Escurridor borde", _lin(150, 150, 150), rough=0.6),
    teal=mat("Turquesa tazas", _lin(106, 176, 191), rough=0.3),
    teal_cm=mat("Turquesa cafetera", _lin(79, 190, 187), rough=0.35),
    mint_top=mat("Menta tapa cubos", _lin(170, 214, 200), rough=0.5),
    mint_cup=mat("Menta vasitos", _lin(167, 191, 189), rough=0.5),
    plate=mat("Platos negros", _lin(40, 40, 52), rough=0.25),
    cube=mat("Melamina negra", _lin(29, 29, 34), rough=0.5),
    bin=mat("Canasto tela negro", _lin(22, 22, 26), rough=0.95),
    oven=mat("Horno negro", _lin(33, 39, 45), rough=0.35, metal=0.3),
    oven_glass=mat("Horno vidrio", _lin(15, 15, 18), rough=0.05),
    hotplate=mat("Anafe placa", _lin(25, 25, 28), rough=0.25),
    glass_cup=mat("Vasos vidrio", _lin(200, 215, 220), rough=0.05, alpha=0.45),
    copper=mat("Taza cobre", _lin(200, 130, 85), rough=0.3, metal=1.0),
    rug=mat("Alfombra persa", _lin(110, 80, 75), tex="cocina_alfombra.jpg", rough=0.95),
    lamina=mat("Lamina botanica", _lin(200, 200, 195), tex="cocina_lamina.jpg", rough=0.8),
    life=mat("Cartel LIFE", _lin(230, 230, 228), tex="cocina_life.jpg", rough=0.8),
    letrero=mat("Letrero letras", _lin(40, 40, 40), tex="cocina_letrero.jpg", rough=0.8),
    frame_dk=mat("Marco cuadro", _lin(70, 55, 40), rough=0.6),
    mandala=mat("Mandala madera", _lin(95, 70, 50), rough=0.7),
    towel=mat("Repasador rayado", _lin(200, 40, 60), rough=0.95),
    blue=mat("Manta azul", _lin(30, 50, 120), rough=0.95),
    red=mat("Rojo caja", _lin(190, 20, 30), rough=0.5),
    soap=mat("Botellas jabon", _lin(225, 225, 215), rough=0.4),
    knife=mat("Cabo cuchillos", _lin(25, 25, 25), rough=0.4),
    block=mat("Taco madera", _lin(220, 190, 150), rough=0.6),
)

# --------------------------------------------------------------- medidas de la cocina
SINK_WIN = max(LEFT_WINS, key=lambda w: w[1] - w[0])     # la ventana grande (sobre la bacha)
CD = 0.60                       # profundidad del bajo mesada (sin la mesada)
CZ = 0.91                       # altura de la mesada terminada
CT = 0.04                       # espesor de la mesada (tabla maciza)
TOE = 0.09                      # zócalo
KY0 = 0.33                      # hueco de escoba entre la pared del frente y el mueble (f0034)
# módulos desde el frente: cajonera de 3 (la que abre el presentador), puerta(s), puerta doble bajo la bacha,
# cajonera trasera de 3. La bacha va bajo la mitad delantera de la ventana grande (canilla junto al marco, f0066).
SINK_Y = SINK_WIN[0] + 0.32
MOD_A = 0.45
YA1 = KY0 + MOD_A
YB0 = SINK_Y - 0.40             # puerta doble bajo la bacha
YB1 = SINK_Y + 0.40
KY1 = YB1 + 0.55
FX = XL + CD                    # plano de los frentes
CY_CTR = XL + CD / 2

# casco (oscuro, se ve en las juntas) + zócalo retirado
box("Bajo mesada", XL, FX - 0.02, KY0, KY1, TOE, CZ - CT, MC["wood_dark"])
box("Zocalo cocina", XL, FX - 0.07, KY0 + 0.02, KY1 - 0.02, 0.0, TOE, MC["wood_dark"])
# mesada maciza con canto visible y pequeño vuelo
box("Mesada", XL, FX + 0.035, KY0 - 0.01, KY1 + 0.01, CZ - CT, CZ, MC["counter"], tile=0.9)

def pull_h(parts, x, yc, zc, length, mi=1):
    """Tirador arco horizontal (en cajones): barra + dos patas."""
    parts += [(x + 0.022, x + 0.032, yc - length / 2, yc + length / 2, zc - 0.005, zc + 0.005, mi),
              (x, x + 0.03, yc - length / 2, yc - length / 2 + 0.01, zc - 0.004, zc + 0.004, mi),
              (x, x + 0.03, yc + length / 2 - 0.01, yc + length / 2, zc - 0.004, zc + 0.004, mi)]

def pull_v(parts, x, yc, zc, length, mi=1):
    """Tirador arco vertical (en puertas)."""
    parts += [(x + 0.022, x + 0.032, yc - 0.005, yc + 0.005, zc - length / 2, zc + length / 2, mi),
              (x, x + 0.03, yc - 0.004, yc + 0.004, zc - length / 2, zc - length / 2 + 0.01, mi),
              (x, x + 0.03, yc - 0.004, yc + 0.004, zc + length / 2 - 0.01, zc + length / 2, mi)]

G = 0.004   # media junta entre frentes
FZ0, FZ1 = TOE + 0.01, CZ - CT - 0.015
# cajonera delantera: cajón chico arriba y dos hondos (f0034, f0080). Interactivos Cajon 1-3 (slide hacia +x).
dz = [(FZ1 - 0.15, FZ1), (FZ0 + (FZ1 - 0.15 - FZ0) / 2, FZ1 - 0.15), (FZ0, FZ0 + (FZ1 - 0.15 - FZ0) / 2)]
for i, (z0, z1) in enumerate(dz):
    pv = (FX, KY0, z0)
    bm = bmesh.new()
    y0, y1 = KY0 + G, YA1 - G
    add_box(bm, FX - 0.02, FX, y0, y1, z0 + G, z1 - G, pivot=pv, mi=0)                      # frente
    add_box(bm, FX - 0.50, FX - 0.02, y0 + 0.03, y1 - 0.03, z0 + 0.02, z0 + 0.03, pivot=pv, mi=0)   # fondo
    add_box(bm, FX - 0.50, FX - 0.02, y0 + 0.02, y0 + 0.03, z0 + 0.02, z1 - 0.04, pivot=pv, mi=0)
    add_box(bm, FX - 0.50, FX - 0.02, y1 - 0.03, y1 - 0.02, z0 + 0.02, z1 - 0.04, pivot=pv, mi=0)
    add_box(bm, FX - 0.50, FX - 0.49, y0 + 0.02, y1 - 0.02, z0 + 0.02, z1 - 0.04, pivot=pv, mi=0)
    pp = []
    pull_h(pp, FX, (y0 + y1) / 2, z1 - 0.06 if i else (z0 + z1) / 2, 0.14)
    for p in pp:
        add_box(bm, *p[:6], pivot=pv, mi=1)
    bm.normal_update()
    caj = make_obj(f"Cajon {i + 1}", bm, [MC["wood"], MC["pull"]], pv, 0.6)
    interactive(caj, "slide", f"Cajón {i + 1} de la cocina", vec=(0.40, 0, 0))

# frentes fijos: puerta doble bajo la bacha + cajonera trasera de 3 cajones iguales
parts = []
if YB0 - YA1 > 0.08:            # puerta(s) entre la cajonera y la bacha
    nd = 2 if YB0 - YA1 > 0.55 else 1
    wd = (YB0 - YA1) / nd
    for k in range(nd):
        parts.append((FX - 0.02, FX, YA1 + k * wd + G, YA1 + (k + 1) * wd - G, FZ0, FZ1, 0))
        pull_v(parts, FX, YA1 + (k + 1) * wd - 0.04 if k == nd - 1 and nd == 1 else YA1 + wd + (0.04 if k else -0.04), FZ1 - 0.13, 0.12)
else:
    YB0 = YA1
ym = (YB0 + YB1) / 2
parts += [(FX - 0.02, FX, YB0 + G, ym - G, FZ0, FZ1, 0), (FX - 0.02, FX, ym + G, YB1 - G, FZ0, FZ1, 0)]
pull_v(parts, FX, ym - 0.04, FZ1 - 0.13, 0.12)
pull_v(parts, FX, ym + 0.04, FZ1 - 0.13, 0.12)
hz = (FZ1 - FZ0) / 3
for k in range(3):
    z0 = FZ0 + k * hz
    parts.append((FX - 0.02, FX, YB1 + G, KY1 - G, z0 + G, z0 + hz - G, 0))
    pull_h(parts, FX, (YB1 + KY1) / 2, z0 + hz - 0.06, 0.18)
multi("Frentes cocina", parts, [MC["wood"], MC["pull"]], tile=0.6)
# panel lateral visible junto a la heladera y del lado del frente
box("Lateral mueble frente", XL, FX, KY0 - 0.005, KY0, TOE, CZ - CT, MC["wood"], tile=0.6)
box("Lateral mueble fondo", XL, FX, KY1, KY1 + 0.005, TOE, CZ - CT, MC["wood"], tile=0.6)

# ------------------------------------------------------------- bacha bajo mesada + escurridor de varillas
SW, SD = 0.54, 0.40          # largo (y) y ancho (x) de la bacha
sx0, sx1 = XL + 0.10, XL + 0.10 + SD
sy0, sy1 = SINK_Y - SW / 2, SINK_Y + SW / 2
multi("Bacha", [(sx0, sx1, sy0, sy1, CZ - 0.22, CZ - 0.20, 1),
                (sx0, sx0 + 0.01, sy0, sy1, CZ - 0.22, CZ + 0.001, 0), (sx1 - 0.01, sx1, sy0, sy1, CZ - 0.22, CZ + 0.001, 0),
                (sx0, sx1, sy0, sy0 + 0.01, CZ - 0.22, CZ + 0.001, 0), (sx0, sx1, sy1 - 0.01, sy1, CZ - 0.22, CZ + 0.001, 0)],
      [MC["sink"], MC["sink_in"]])
box("Bacha hueco", sx0 + 0.01, sx1 - 0.01, sy0 + 0.01, sy1 - 0.01, CZ - 0.20, CZ + 0.0015, MC["sink_in"])
# escurridor enrollable: varillas a lo ancho (x), apoyado sobre la mitad trasera de la bacha y la mesada
RY0, RY1 = SINK_Y - 0.05, SINK_Y + 0.45
nr = 18
rparts = [(sx0 - 0.03, sx1 + 0.03, RY0 + (RY1 - RY0) * k / (nr - 1) - 0.005, RY0 + (RY1 - RY0) * k / (nr - 1) + 0.005,
           CZ + 0.002, CZ + 0.012, 0) for k in range(nr)]
rparts += [(sx0 - 0.04, sx0 - 0.02, RY0 - 0.01, RY1 + 0.01, CZ + 0.001, CZ + 0.010, 1),
           (sx1 + 0.02, sx1 + 0.04, RY0 - 0.01, RY1 + 0.01, CZ + 0.001, CZ + 0.010, 1)]
multi("Escurridor", rparts, [MC["rack"], MC["rack_edge"]])
box("Repasador", sx0 + 0.02, sx0 + 0.20, RY1 + 0.03, RY1 + 0.16, CZ, CZ + 0.04, MC["towel"])
# canilla negra tipo cuello de ganso, contra la pared delante de la bacha (f0066)
CANY = sy0 + 0.06
canilla = multi("Canilla cocina", [(-0.025, 0.025, -0.025, 0.025, 0.0, 0.03),         # base
                                   (-0.013, 0.013, -0.013, 0.013, 0.0, 0.40),         # cuello
                                   (-0.013, 0.20, -0.013, 0.013, 0.37, 0.40),         # caño
                                   (0.17, 0.20, -0.016, 0.016, 0.28, 0.40),           # pico extraíble
                                   (0.0, 0.07, 0.013, 0.023, 0.10, 0.12)],            # palanca
                [M["blackmetal"]], pivot=(0, 0, 0))
canilla.location = (XL + 0.06, CANY + 0.10, CZ)
interactive(canilla, "water", "Canilla de la cocina", group="agua_cocina")
agua_c = cyl("Agua cocina", XL + 0.06 + 0.185, CANY + 0.10, CZ - 0.20, CZ + 0.28, 0.010, M["water"], verts=8)
agua_c["water_of"] = "agua_cocina"
# botellas de jabón junto a la canilla
for j, (dy, h) in enumerate([(0.17, 0.20), (0.24, 0.22), (0.31, 0.16)]):
    cyl(f"Jabon {j}", XL + 0.07, sy0 - dy + 0.30, CZ, CZ + h, 0.03, MC["soap"], verts=10)
# taco de cuchillos al fondo de la mesada (f0066)
kb = YB1 + 0.30
box("Taco cuchillos", XL + 0.05, XL + 0.20, kb, kb + 0.12, CZ, CZ + 0.20, MC["block"])
multi("Cuchillos", [(XL + 0.06 + 0.025 * i, XL + 0.075 + 0.025 * i, kb + 0.02 + 0.02 * (i % 3), kb + 0.04 + 0.02 * (i % 3),
                     CZ + 0.20, CZ + 0.30, 0) for i in range(5)], [MC["knife"]])

# ------------------------------------------------------------- horno eléctrico (adelante, puerta hacia el pasillo)
OY0, OY1 = KY0 + 0.04, KY0 + 0.50
OX0, OX1 = XL + 0.12, XL + 0.46
box("Horno electrico", OX0, OX1, OY0, OY1, CZ + 0.02, CZ + 0.28, MC["oven"])
box("Horno vidrio", OX1, OX1 + 0.005, OY0 + 0.03, OY1 - 0.13, CZ + 0.05, CZ + 0.24, MC["oven_glass"])
for k in range(3):
    cyl(f"Horno perilla {k}", OX1 + 0.01, OY1 - 0.065, CZ + 0.08 + k * 0.065, CZ + 0.10 + k * 0.065, 0.018,
        M["steel"], verts=10, axis="X")
for k in range(4):
    cyl(f"Horno pata {k}", OX0 + 0.03 + (k % 2) * (OX1 - OX0 - 0.06), OY0 + 0.03 + (k // 2) * (OY1 - OY0 - 0.06),
        CZ, CZ + 0.02, 0.012, M["black"], verts=6)
box("Horno manija", OX1 + 0.01, OX1 + 0.025, OY0 + 0.05, OY1 - 0.16, CZ + 0.24, CZ + 0.255, M["steel"])

# ------------------------------------------------------------- estantes flotantes (rincón del frente, sobre el horno)
SH_D, SH_Y1 = 0.26, KY0 + 0.62
sh_z = [1.50, 1.80]
for k, z in enumerate(sh_z):
    box(f"Estante cocina {k}", XL, XL + SH_D, 0.0, SH_Y1, z, z + 0.04, MC["wood"], tile=0.6)
box("Estante cocina repisa", XL, XL + 0.10, 0.0, SH_Y1 + 0.10, 1.25, 1.28, MC["wood"], tile=0.6)   # repisa baja (f0054)
box("Rejilla bajo estante", XL + 0.04, XL + 0.22, 0.30, SH_Y1 - 0.02, sh_z[0] - 0.05, sh_z[0] - 0.035, M["white"])
# estante de arriba: bowls/tazas turquesa, taza de cobre, pila de platos negros acostados
zt = sh_z[1] + 0.04
for j in range(3):
    cone(f"Bowl turquesa {j}", XL + 0.13, 0.12 + j * 0.13, zt, zt + 0.10, 0.045, 0.065, MC["teal"], verts=12)
cyl("Taza cobre", XL + 0.13, 0.52, zt, zt + 0.11, 0.04, MC["copper"], verts=10)
cyl("Platos arriba", XL + 0.13, SH_Y1 - 0.14, zt, zt + 0.05, 0.13, MC["plate"], verts=16)
# estante medio: vasos de vidrio, tazas blancas y bowls negros apilados
zm = sh_z[0] + 0.04
for j in range(5):
    cyl(f"Vaso {j}", XL + 0.09 + (j % 2) * 0.07, 0.06 + j * 0.065, zm, zm + 0.13, 0.032, MC["glass_cup"], verts=8)
for j in range(2):
    cyl(f"Taza blanca {j}", XL + 0.12, 0.42 + j * 0.08, zm, zm + 0.08, 0.035, M["white"], verts=10)
cyl("Bowls negros", XL + 0.13, SH_Y1 - 0.13, zm, zm + 0.12, 0.11, MC["plate"], verts=14)
cyl("Platos medio", XL + 0.13, SH_Y1 - 0.13, zm + 0.12, zm + 0.15, 0.13, MC["plate"], verts=14)

# ------------------------------------------------------------- pared del frente: lámina botánica sobre la puerta
pd0, pd1 = FRONT_DOOR[0], FRONT_DOOR[1]
lx = (pd0 + pd1) / 2 - 0.08
box("Cuadro frente", lx - 0.22, lx + 0.22, 0.0, 0.02, 2.22, 2.76, MC["frame_dk"])
box("Lamina frente", lx - 0.21, lx + 0.21, 0.02, 0.025, 2.23, 2.75, MC["lamina"])
# alfombra persa frente a la puerta (textura recortada del fotograma f0054)
box("Alfombra entrada", pd0 - 0.05, pd1 + 0.05, 0.08, 0.68, 0.0, 0.008, MC["rug"])
for o in [bpy.data.objects["Alfombra entrada"]]:
    # la textura cubre la alfombra entera (UV 0..1 en planta)
    me = o.data
    uvl = me.uv_layers.active.data
    xs = [v.co.x for v in me.vertices]; ys = [v.co.y for v in me.vertices]
    for poly in me.polygons:
        for li in poly.loop_indices:
            v = me.vertices[me.loops[li].vertex_index].co
            uvl[li].uv = ((v.x - min(xs)) / (max(xs) - min(xs)), (v.y - min(ys)) / (max(ys) - min(ys)))

# ------------------------------------------------------------- pared derecha (+x): mueble negro de cubos con anafe
# 2 columnas x 3 filas de melamina negra, tapa con manta menta; anafe doble atrás y cafetera adelante (f0038/f0040).
RW_SMALL = min(RIGHT_WINS, key=lambda w: w[0])          # ventana angosta cerca de la puerta
CBD, CBH, CBW = 0.32, 0.86, 0.72
SY0 = RW_SMALL[1] - 0.05
SY1 = SY0 + CBW
SX1, SX0 = XR - 0.01, XR - 0.01 - CBD
th = 0.018
cp = [(SX0, SX1, SY0, SY1, 0.0, th, 0), (SX0, SX1, SY0, SY1, CBH - th, CBH, 0),
      (SX0, SX1, SY0, SY0 + th, 0, CBH, 0), (SX0, SX1, SY1 - th, SY1, 0, CBH, 0),
      (SX0, SX1, (SY0 + SY1) / 2 - th / 2, (SY0 + SY1) / 2 + th / 2, 0, CBH, 0),
      (SX1 - 0.006, SX1, SY0, SY1, 0, CBH, 0)]
for k in (1, 2):
    z = k * CBH / 3
    cp.append((SX0, SX1, SY0, SY1, z - th / 2, z + th / 2, 0))
multi("Mueble cubos", cp, [MC["cube"]])
cw = (CBW - 3 * th) / 2
ch = (CBH - 4 * th) / 3
def cubby(col, row):
    y0 = SY0 + th + col * (cw + th); z0 = th + row * (ch + th)
    return y0, y0 + cw, z0, z0 + ch
# canastos de tela negros (columna delantera) y cosas en la trasera
for row in range(3):
    y0, y1, z0, z1 = cubby(0, row)
    box(f"Canasto {row}", SX0 + 0.01, SX1 - 0.02, y0 + 0.01, y1 - 0.01, z0, z1 - 0.01, MC["bin"])
    cyl(f"Canasto ojal {row}", SX0 + 0.005, (y0 + y1) / 2, (z0 + z1) / 2 + 0.06, (z0 + z1) / 2 + 0.07, 0.018,
        M["steel"], verts=8, axis="X")
y0, y1, z0, z1 = cubby(1, 2)
box("Caja roja", SX0 + 0.06, SX1 - 0.05, y0 + 0.03, y1 - 0.05, z0, z0 + 0.06, MC["red"])
y0, y1, z0, z1 = cubby(1, 1)
box("Manta azul", SX0 + 0.02, SX1 - 0.03, y0 + 0.01, y1 - 0.01, z0, z0 + 0.17, MC["blue"])
y0, y1, z0, z1 = cubby(1, 0)
box("Canasto bajo", SX0 + 0.01, SX1 - 0.02, y0 + 0.01, y1 - 0.01, z0, z1 - 0.01, MC["bin"])
box("Tapa menta", SX0 - 0.005, SX1, SY0, SY1, CBH, CBH + 0.006, MC["mint_top"])
# anafe eléctrico doble (atrás, y mayor)
ay = SY1 - 0.20
box("Anafe", SX0 + 0.03, SX1 - 0.03, ay - 0.17, ay + 0.17, CBH + 0.006, CBH + 0.07, M["black"])
for k, dy in enumerate((-0.085, 0.085)):
    cyl(f"Hornalla {k}", (SX0 + SX1) / 2, ay + dy, CBH + 0.07, CBH + 0.078, 0.075, MC["hotplate"], verts=20)
    cyl(f"Hornalla aro {k}", (SX0 + SX1) / 2, ay + dy, CBH + 0.069, CBH + 0.074, 0.082, M["steel"], verts=20)
# cafetera turquesa de una taza (adelante) + taza blanca
cy0 = SY0 + 0.03
box("Cafetera", SX0 + 0.12, SX1 - 0.02, cy0, cy0 + 0.17, CBH + 0.006, CBH + 0.31, MC["teal_cm"])
box("Cafetera base", SX0 + 0.02, SX0 + 0.12, cy0, cy0 + 0.17, CBH + 0.006, CBH + 0.03, MC["teal_cm"])
box("Cafetera cabezal", SX0 + 0.04, SX0 + 0.12, cy0, cy0 + 0.17, CBH + 0.22, CBH + 0.31, MC["teal_cm"])
cyl("Taza cafe", SX0 + 0.08, cy0 + 0.085, CBH + 0.03, CBH + 0.12, 0.04, M["white"], verts=10)
cyl("Frasco", SX0 + 0.08, cy0 + 0.25, CBH + 0.006, CBH + 0.14, 0.05, MC["glass_cup"], verts=10)

# riel blanco con 3 vasitos menta (sobre la cafetera), termostato y mandala calado
box("Toallero", XR - 0.05, XR - 0.005, SY0 + 0.02, SY0 + 0.40, 1.33, 1.345, M["white"])
for k in range(3):
    box(f"Vasito colgante {k}", XR - 0.11, XR - 0.02, SY0 + 0.05 + k * 0.11, SY0 + 0.15 + k * 0.11, 1.18, 1.33, MC["mint_cup"])
box("Termostato", XR - 0.025, XR - 0.002, SY0 + 0.50, SY0 + 0.57, 1.70, 1.87, M["white"])

def hexring(name, xw, yc, zc, r, wdt, depth, m_):
    """Aro hexagonal plano sobre la pared x=xw (sobresale hacia -x)."""
    bm = bmesh.new()
    for ri in (r, r * 0.62, r * 0.30):
        pts = [(yc + ri * math.cos(math.radians(30 + 60 * k)), zc + ri * math.sin(math.radians(30 + 60 * k))) for k in range(6)]
        for k in range(6):
            (y_a, z_a), (y_b, z_b) = pts[k], pts[(k + 1) % 6]
            ln = math.hypot(y_b - y_a, z_b - z_a); ang = math.atan2(z_b - z_a, y_b - y_a)
            res = bmesh.ops.create_cube(bm, size=1.0)
            vs = res["verts"]
            bmesh.ops.scale(bm, vec=(depth, ln + wdt, wdt), verts=vs)
            bmesh.ops.rotate(bm, verts=vs, matrix=Matrix.Rotation(ang, 3, "X"))
            bmesh.ops.translate(bm, verts=vs, vec=(xw - depth / 2, (y_a + y_b) / 2, (z_a + z_b) / 2))
    bm.normal_update()
    return make_obj(name, bm, [m_])
hexring("Mandala", XR - 0.002, RW_SMALL[1] + 0.12, 1.90, 0.16, 0.022, 0.015, MC["mandala"])
# repisa de la ventana angosta (con florero)
box("Repisa ventana", XR - 0.14, XR, RW_SMALL[0] - 0.08, RW_SMALL[1] + 0.08, RW_SMALL[2] - 0.08, RW_SMALL[2] - 0.05, M["pine"])
cyl("Florero", XR - 0.07, RW_SMALL[0] + 0.05, RW_SMALL[2] - 0.05, RW_SMALL[2] + 0.18, 0.03, mat("Florero vidrio", _lin(120, 140, 170), alpha=0.6), verts=8)
# cartel "LIFE" apoyado en el alféizar de la ventana grande de la derecha (f0090)
_rw = [w for w in RIGHT_WINS if RW_SMALL[1] < w[0] < BATH_Y - 0.1]   # (las medidas reales dejan una sola ventana en el lado +x del living)
if _rw:
    RW_BIG = _rw[0]
    box("Cartel LIFE", XR - 0.10, XR - 0.09, RW_BIG[0] + 0.12, RW_BIG[0] + 0.40, RW_BIG[2] - 0.05, RW_BIG[2] + 0.30, MC["life"])
else:
    RW_BIG = RW_SMALL
    box("Cartel LIFE", XR - 0.10, XR - 0.09, RW_SMALL[1] + 0.40, RW_SMALL[1] + 0.68, 1.45, 1.80, MC["life"])
# estante alto sobre la entrada (pared derecha, bajo el alero)
box("Estante alto entrada", XR - 0.34, XR, 0.0, SY0 + 0.20, 2.10, 2.13, M["plywood"], tile=1.0)
box("Estante alto frente", XR - 0.36, XR - 0.34, 0.0, SY0 + 0.20, 2.10, 2.22, M["plywood"], tile=1.0)

# letrero de letras (negro) sobre la heladera, contra la pared izquierda (f0094); la heladera es de la zona living
box("Pizarra menu", XL + 0.02, XL + 0.05, KY1 + 0.08, KY1 + 0.40, 1.60, 1.96, MC["letrero"])
