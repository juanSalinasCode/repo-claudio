# Zona: exterior. Se ejecuta en el espacio de nombres compartido de core.py (ver build.py).
# Referencia: fotogramas f0001–f0010 (fachada frontal, deck, entorno). Ver audit/exterior.md.
# Todo se expresa relativo a las constantes de core.py (XL, XR, W, L, T, EAVE, RIDGE, GROUND).
# Esta zona corre ANTES que estructura.py: no puede usar FRONT_DOOR/FRONT_WIN (la puerta, el felpudo y los
# faroles están en puerta_luces.py).
# =================================================================== EXTERIOR
import random
CUR[0] = "Exterior"

X0, X1 = XL - T, XR + T                 # caras exteriores de las paredes laterales
Y0, Y1 = -T, L + T                      # caras exteriores de frente y fondo
# Techo: visto de frente es un PRISMA RECTO de techo casi plano (no se ve hastial triangular). Fachada medida
# en f0001/f0004: alto (deck→borde superior de la cenefa) ≈ 1.37 × ancho exterior (2.40 → ≈3.29 m).
# La chapa APOYA sobre el remate de estructura.py (hastiales/cenefas hasta TOP = EAVE + 0.22, definido allí
# después de esta zona): losa de ≥2.5 cm encima, sin cruzar. Con ese TOP la proporción da ≈1.43.
STRUCT_TOP = EAVE + 0.22                # = TOP de estructura.py (no definido todavía cuando corre esta zona)
ROOF_FALL = 0.015                       # caída hacia el fondo (inferido: no se ve)
ROOF_TOP = STRUCT_TOP + 0.003 + 0.025 + ROOF_FALL   # borde superior de la cenefa en el frente
FASCIA_H = 0.24                         # cenefa negra
ROOF_OV = 0.13                          # alero (frente y lados ≈ 0.12–0.16 m en f0004)
CLAD = 0.02                             # el revestimiento superior sobresale 2 cm: arma la "junta" horizontal
BELT_Z = 2.05 + 0.22                  # junta/botaguas horizontal (f0004/f0007: 0.22 m sobre el contramarco de la puerta)
EXT_DECK_Z = -0.04                      # superficie del deck (un poco más baja que el umbral)
EXT_DECK_D = 1.20                       # profundidad del deck (fuga en f0001 con HFOV 62° de cameras.json → cámara a ~7.7 m)
STEP_D = 0.27                           # huella de los 2 escalones (f0001: 0.28 / 0.22 m)
GRAVEL_M = 0.30                         # franja de ripio alrededor (más allá de las paredes)
GRAVEL_FRONT = Y0 - EXT_DECK_D - 2 * STEP_D - 0.25     # ≈ 2.0 m delante de la fachada

# --- materiales propios (colores lineales muestreados de los fotogramas)
_sid = M["siding"]                       # revestimiento board-and-batten gris carbón real (recorte de f0005)
for _n in _sid.node_tree.nodes:
    if _n.type == "TEX_IMAGE":
        _n.image = bpy.data.images.load(os.path.join(TEX, "exterior_siding.jpg"), check_existing=True)
_sid.diffuse_color = (0.085, 0.082, 0.088, 1)
EM = dict(
    fascia=mat("Cenefa negra", (0.02, 0.022, 0.024), rough=0.6),
    membrane=mat("Techo membrana", (0.05, 0.05, 0.055), rough=0.8),
    deck=mat("Deck gris", tex="exterior_deck.jpg", rough=0.85),
    grass=mat("Pasto real", tex="exterior_pasto.jpg", rough=1.0),
    gravel=mat("Ripio", tex="exterior_ripio.jpg", rough=1.0),
    timber=mat("Durmiente", (0.24, 0.17, 0.11), rough=0.9),
    paver=mat("Losetas", (0.30, 0.29, 0.27), rough=0.9),
    bark=mat("Corteza gris", tex="exterior_corteza.jpg", rough=1.0),
    leaf=mat("Follaje real", tex="exterior_follaje.jpg", rough=1.0),
    leaf2=mat("Follaje real 2", tex="exterior_follaje2.jpg", rough=1.0),
    shrub=mat("Arbusto", (0.035, 0.09, 0.03), rough=1.0),
    rock=mat("Roca", (0.55, 0.50, 0.38), rough=0.9),
    grill=mat("Parrilla negra", (0.012, 0.014, 0.013), rough=0.5, metal=0.3),
    ac=mat("Condensadora gris", (0.50, 0.51, 0.52), rough=0.5),
    shed=mat("Galpon madera", (0.42, 0.30, 0.17), rough=0.8),
    zocalo=mat("Zocalo oscuro", (0.03, 0.03, 0.032), rough=0.8),
)

def hull(name, pts, mats, mi_fn=None, tile=1.0):
    """Sólido convexo de una lista de puntos (para el techo inclinado)."""
    bm = bmesh.new()
    for p in pts:
        bm.verts.new(p)
    bmesh.ops.convex_hull(bm, input=bm.verts)
    bm.normal_update()
    if mi_fn:
        for f in bm.faces:
            f.material_index = mi_fn(f.normal)
    return make_obj(name, bm, mats, (0, 0, 0), tile)

def boxes(name, parts, m_, tile=1.0):
    """Una caja = un objeto (los anillos en un solo objeto daban AABB enormes que 'contenían' la casa)."""
    for i, p in enumerate(parts):
        box(f"{name} {i}", *p, m_, tile=tile)

# --------------------------------------------------------------- terreno, ripio, deck, escalones
box("Terreno", -40, 40, -40, 40, GROUND - 0.1, GROUND, EM["grass"], tile=5.0)
box("Ripio", X0 - GRAVEL_M, X1 + GRAVEL_M, GRAVEL_FRONT, Y1 + GRAVEL_M, GROUND, GROUND + 0.025, EM["gravel"], tile=0.6)
gx0, gx1, gy0, gy1, tw = X0 - GRAVEL_M - 0.1, X1 + GRAVEL_M + 0.1, GRAVEL_FRONT - 0.1, Y1 + GRAVEL_M + 0.1, 0.10
boxes("Borde durmientes", [(gx0, gx1, gy0, gy0 + tw, GROUND, GROUND + 0.10), (gx0, gx1, gy1 - tw, gy1, GROUND, GROUND + 0.10),
                           (gx0, gx0 + tw, gy0 + tw, gy1 - tw, GROUND, GROUND + 0.10),
                           (gx1 - tw, gx1, gy0 + tw, gy1 - tw, GROUND, GROUND + 0.10)], EM["timber"])
# zócalo: faldón perimetral de 4 cm bajo las paredes (hueco por dentro: no invade lo que cuelga bajo el piso)
ZT, zz = 0.04, (GROUND + 0.002, -0.003)
boxes("Zocalo", [(X0, X1, Y0, Y0 + ZT, *zz), (X0, X1, Y1 - ZT, Y1, *zz),
                 (X0, X0 + ZT, Y0 + ZT, Y1 - ZT, *zz), (X1 - ZT, X1, Y0 + ZT, Y1 - ZT, *zz)], EM["zocalo"])
box("Deck", X0, X1, Y0 - EXT_DECK_D, Y0, GROUND + 0.02, EXT_DECK_Z, EM["deck"], tile=1.0)
_rh = (EXT_DECK_Z - GROUND) / 3          # 3 contrahuellas iguales (deck + 2 escalones), f0001
for k in (1, 2):
    box(f"Escalon {k}", X0 - 0.02, X1 + 0.02, Y0 - EXT_DECK_D - k * STEP_D, Y0 - EXT_DECK_D - (k - 1) * STEP_D,
        GROUND + 0.02, EXT_DECK_Z - k * _rh, EM["deck"], tile=1.0)
# senda de losetas hacia la derecha (f0001, abajo a la derecha), fuera del borde de durmientes
multi("Losetas senda", [(gx1 + 0.15 + i * 0.68, gx1 + 0.75 + i * 0.68, GRAVEL_FRONT + 0.15 - 0.08 * i,
                         GRAVEL_FRONT + 0.75 - 0.08 * i, GROUND, GROUND + 0.03) for i in range(5)], [EM["paver"]])

# --------------------------------------------------------------- revestimiento superior + techo
# Todo POR FUERA de las caras exteriores de las paredes (X0, X1, Y0, Y1 con T=0.20). Sobre BELT_Z el
# revestimiento sobresale CLAD y la tapajunta negra (debajo, BELT_Z−0.03..BELT_Z) marca la junta horizontal.
# Muesca en la tapajunta/revestimiento detrás del farol de puerta_luces (x≈0.80–0.97, placa hasta ≈2.30).
zc1 = ROOF_TOP - FASCIA_H + 0.02
FAROL_X = (0.80, 0.97)
_zf = BELT_Z + 0.035
boxes("Revestimiento superior", [
    (X0 - CLAD, FAROL_X[0], Y0 - CLAD, Y0, BELT_Z, zc1),                 # frente (izq. del farol)
    (FAROL_X[1], X1 + CLAD, Y0 - CLAD, Y0, BELT_Z, zc1),                 # frente (der. del farol)
    (FAROL_X[0], FAROL_X[1], Y0 - CLAD, Y0, _zf, zc1),                   # frente (sobre el farol)
    (X0 - CLAD, X0, Y0, Y1, BELT_Z, zc1),                                # izquierda
    (X1, X1 + CLAD, Y0, Y1, BELT_Z, zc1)], M["siding"])                  # derecha
bz, bo = (BELT_Z - 0.03, BELT_Z), CLAD + 0.012
boxes("Tapajunta", [(X0 - bo, FAROL_X[0], Y0 - bo, Y0, *bz), (FAROL_X[1], X1 + bo, Y0 - bo, Y0, *bz),
                    (X0 - bo, X1 + bo, Y1, Y1 + 0.012, *bz),
                    (X0 - bo, X0, Y0, Y1, *bz), (X1, X1 + bo, Y0, Y1, *bz)], EM["fascia"])
# esquineros: tablas verticales de 2.5 cm en las 4 esquinas, pegadas por fuera (frente: hasta la tapajunta;
# fondo: hasta el revestimiento superior, que no cubre el fondo para no tapar las ventanas del altillo)
EQ = 0.025
boxes("Esquineros", [(X0 - EQ, X0, Y0 - EQ, Y0, 0.0, bz[0]), (X1, X1 + EQ, Y0 - EQ, Y0, 0.0, bz[0]),
                     (X0 - EQ, X0, Y1, Y1 + EQ, 0.0, bz[0]), (X1, X1 + EQ, Y1, Y1 + EQ, 0.0, bz[0]),
                     (X0 - CLAD, X0, Y1, Y1 + EQ, bz[1], ROOF_TOP - FASCIA_H), (X1, X1 + CLAD, Y1, Y1 + EQ, bz[1], ROOF_TOP - FASCIA_H)], M["siding"])
rx0, rx1, ry0, ry1 = X0 - ROOF_OV, X1 + ROOF_OV, Y0 - ROOF_OV, Y1 + ROOF_OV
zt0, zt1 = ROOF_TOP, ROOF_TOP - ROOF_FALL
zb = STRUCT_TOP + 0.003                  # la chapa apoya sobre hastiales/cenefas de estructura (3 mm de luz)
hull("Techo", [(rx0, ry0, zt0), (rx1, ry0, zt0), (rx0, ry1, zt1), (rx1, ry1, zt1),
               (rx0, ry0, zb), (rx1, ry0, zb), (rx0, ry1, zb), (rx1, ry1, zb)],
     [EM["fascia"], EM["membrane"]], mi_fn=lambda n: 1 if n.z > 0.5 else 0)
fz0 = ROOF_TOP - FASCIA_H                  # cenefa negra perimetral (por fuera del revestimiento)
boxes("Cenefa", [(rx0, rx1, ry0, Y0 - CLAD, fz0, zb), (rx0, rx1, Y1, ry1, fz0, zb),
                 (rx0, X0 - CLAD, Y0 - CLAD, Y1, fz0, zb), (X1 + CLAD, rx1, Y0 - CLAD, Y1, fz0, zb)], EM["fascia"])

# --------------------------------------------------------------- parrilla (plancha negra con carro, f0003)
gxc, gyc, gz = X0 - 1.25, Y0 + 0.10, GROUND
gparts = []
for dx in (-0.30, 0.30):
    for dy in (-0.22, 0.22):
        gparts.append((gxc + dx - 0.02, gxc + dx + 0.02, gyc + dy - 0.02, gyc + dy + 0.02, gz, gz + 0.80))
gparts += [(gxc - 0.32, gxc + 0.32, gyc - 0.24, gyc + 0.24, gz + 0.22, gz + 0.25),      # estante inferior
           (gxc - 0.36, gxc + 0.36, gyc - 0.26, gyc + 0.26, gz + 0.78, gz + 0.90),      # plancha
           (gxc - 0.35, gxc + 0.35, gyc - 0.20, gyc + 0.26, gz + 0.90, gz + 1.12),      # tapa
           (gxc - 0.62, gxc - 0.36, gyc - 0.22, gyc + 0.22, gz + 0.84, gz + 0.87),      # estante lateral
           (gxc + 0.36, gxc + 0.58, gyc - 0.22, gyc + 0.22, gz + 0.84, gz + 0.87)]
multi("Parrilla", gparts, [EM["grill"]])
# condensadoras del aire (2 unidades grises sobre soporte, detrás de la parrilla, f0003)
for i, yc in enumerate((Y0 + 0.95, Y0 + 1.75)):
    box(f"Condensadora {i}", X0 - 0.85, X0 - 0.52, yc - 0.37, yc + 0.37, GROUND + 0.32, GROUND + 0.88, EM["ac"])
    cyl(f"Condensadora rejilla {i}", X0 - 0.855, yc + 0.08, GROUND + 0.60, GROUND + 0.61, 0.17, M["black"], verts=12, axis="X")
multi("Soporte condensadoras", [(X0 - 0.86, X0 - 0.50, Y0 + 0.52, Y0 + 2.18, GROUND + 0.29, GROUND + 0.32)] +
      [(x - 0.015, x + 0.015, y - 0.015, y + 0.015, GROUND, GROUND + 0.29)
       for x in (X0 - 0.84, X0 - 0.52) for y in (Y0 + 0.55, Y0 + 2.15)], [M["white"]])
multi("Caneria aire", [(X0 - 0.52, X0 - CLAD, Y0 + 0.90, Y0 + 0.96, GROUND + 0.60, GROUND + 0.66)], [M["white"]])

# --------------------------------------------------------------- lado derecho: poste de servicio y galpón (f0003)
PX = gx1 + 0.12                          # poste fuera del borde de durmientes
multi("Poste servicio", [(PX + 0.06, PX + 0.16, Y0 + 2.2, Y0 + 2.3, GROUND, GROUND + 1.9),
                         (PX + 0.01, PX + 0.06, Y0 + 2.12, Y0 + 2.38, GROUND + 1.05, GROUND + 1.55)], [EM["timber"]])
box("Medidor", PX - 0.05, PX + 0.01, Y0 + 2.15, Y0 + 2.35, GROUND + 1.10, GROUND + 1.45, M["gray"])
sx0, sx1, sy0, sy1, sh = gx1 + 0.12, gx1 + 1.02, Y0 + 3.9, Y0 + 5.0, 1.65
box("Galpon", sx0, sx1, sy0, sy1, GROUND, GROUND + sh, EM["shed"])
multi("Galpon esquineros", [(x - 0.04, x + 0.04, sy0 - 0.03, sy0, GROUND, GROUND + sh) for x in (sx0, sx1)] +
      [(sx0 - 0.04, sx1 + 0.04, sy0 - 0.03, sy0, GROUND + sh - 0.08, GROUND + sh)], [M["white"]])
box("Galpon techo", sx0 - 0.1, sx1 + 0.1, sy0 - 0.1, sy1 + 0.1, GROUND + sh, GROUND + sh + 0.08, EM["fascia"])

# --------------------------------------------------------------- rocas y arbustos
def blob(bm, x, y, z, r, sx=1, sy=1, sz=1, mi=0, sub=2, jit=0.0):
    res = bmesh.ops.create_icosphere(bm, subdivisions=sub, radius=r)
    for v in res["verts"]:
        if jit:
            v.co *= 1 + random.uniform(-jit, jit)
        v.co.x, v.co.y, v.co.z = v.co.x * sx + x, v.co.y * sy + y, v.co.z * sz + z
    fs = {f for v in res["verts"] for f in v.link_faces}
    for f in fs:
        f.material_index = mi

# Cada roca/arbusto es un objeto propio y TODO queda fuera de la huella de la casa + 0.3 m, del deck/escalones,
# del borde de durmientes, del galpón, del poste y de las condensadoras (se verifica abajo).
_keepout = [(X0 - 0.3, X1 + 0.3, Y0 - EXT_DECK_D - 2 * STEP_D - 0.3, Y1 + 0.3),        # casa + deck + escalones
            (gx0 - 0.05, gx1 + 0.05, gy0 - 0.05, gy1 + 0.05),                           # cama de ripio con borde
            (sx0 - 0.1, sx1 + 0.1, sy0 - 0.1, sy1 + 0.1), (PX - 0.1, PX + 0.3, Y0 + 2.0, Y0 + 2.5),
            (X0 - 0.95, X0 - 0.4, Y0 + 0.4, Y0 + 2.3), (gxc - 0.7, gxc + 0.7, gyc - 0.35, gyc + 0.35)]

def _free(x, y, rx, ry):
    for (a0, a1, b0, b1) in _keepout:
        if x + rx > a0 and x - rx < a1 and y + ry > b0 and y - ry < b1:
            raise ValueError(f"vegetación/roca en ({x:.2f},{y:.2f}) invade la zona {a0:.2f}..{a1:.2f} × {b0:.2f}..{b1:.2f}")

random.seed(11)
for i, (x, y, r, sz) in enumerate([(2.7, -5.3, 0.62, 0.95), (6.0, 9.0, 0.9, 0.55), (7.9, 9.9, 0.6, 0.5),
                                   (-6.5, 11.0, 0.5, 0.6), (5.2, 8.2, 0.35, 0.6)]):
    _free(x, y, r * 1.1 * 1.13, r * 0.9 * 1.13)
    bm = bmesh.new()
    blob(bm, x, y, GROUND + r * sz * 0.55, r, 1.1, 0.9, sz, jit=0.12)
    bm.normal_update()
    make_obj(f"Roca {i}", bm, [EM["rock"]], (0, 0, 0), 1.0)
for i, (x, y, r) in enumerate([(gx1 + 0.68, Y0 - 0.9, 0.45), (gx1 + 0.72, Y0 + 1.0, 0.40), (gx0 - 0.7, Y1 + 0.9, 0.5),
                               (gx1 + 0.75, Y1 + 1.1, 0.55), (-5.5, 1.5, 0.7), (5.0, -0.5, 0.6), (-4.0, 6.0, 0.8)]):
    _free(x, y, r * 1.21, r * 1.21)
    bm = bmesh.new()
    blob(bm, x, y, GROUND + r * 0.8, r, 1, 1, 1.3, jit=0.2, sub=2)
    bm.normal_update()
    make_obj(f"Arbusto {i}", bm, [EM["shrub"]], (0, 0, 0), 1.0)

# --------------------------------------------------------------- bosque (troncos altos y finos, copas altas)
# Bosque caducifolio claro: troncos rectos grises de 15–25 m, copas que empiezan a ~2/3 de la altura,
# hecho de 3–5 manchas irregulares por árbol. Todo en 2 mallas (troncos / copas) para el visor web.
random.seed(4)
trunks, crowns = bmesh.new(), bmesh.new()

def tree(x, y, h, r):
    c = bmesh.ops.create_cone(trunks, cap_ends=False, segments=6, radius1=r, radius2=r * 0.3, depth=h * 0.92)
    bmesh.ops.translate(trunks, verts=c["verts"], vec=(x, y, GROUND + h * 0.46))
    lean = (random.uniform(-0.03, 0.03), random.uniform(-0.03, 0.03))
    for v in c["verts"]:
        t = v.co.z - GROUND
        v.co.x += lean[0] * t; v.co.y += lean[1] * t
    for k in range(random.randint(4, 6)):
        t = random.uniform(0.45, 1.0)
        a, d = random.uniform(0, 6.28), random.uniform(0.4, 2.2)
        rr = random.uniform(1.0, 1.9) * (0.7 + 0.3 * h / 20)
        blob(crowns, x + lean[0] * h * t + d * math.cos(a), y + lean[1] * h * t + d * math.sin(a), GROUND + h * t, rr,
             random.uniform(0.8, 1.3), random.uniform(0.8, 1.3), random.uniform(0.55, 0.85), mi=random.randint(0, 1), jit=0.25)

# árboles ubicados según f0001 (tronco grande a la derecha detrás de la casa, varios finos a la izquierda)
for (x, y, h, r) in [(5.0, 7.2, 24, 0.28), (-4.6, 9.0, 18, 0.16), (-6.2, 6.5, 17, 0.13), (-3.6, 12.5, 19, 0.15),
                     (3.0, 13.5, 21, 0.2), (7.5, 4.0, 20, 0.17), (-8.0, 2.0, 18, 0.15), (9.5, 11.0, 22, 0.22)]:
    tree(x, y, h, r)
n = 0
while n < 80:
    x, y = random.uniform(-32, 32), random.uniform(-30, 36)
    if (-6.5 < x < 6.5 and -16 < y < 5) or (-4 < x < 4 and y < L + 4):
        continue                                      # claro delante de la casa (de donde se filma)
    tree(x, y, random.uniform(13, 24), random.uniform(0.09, 0.24))
    n += 1
# renovales bajos (sotobosque)
for k in range(25):
    x, y = random.uniform(-20, 20), random.uniform(-10, 25)
    if -6 < x < 6 and y < 8:
        continue
    blob(crowns, x, y, GROUND + random.uniform(0.6, 1.4), random.uniform(0.7, 1.3), 1, 1, 0.8, mi=1, jit=0.3)
trunks.normal_update(); crowns.normal_update()
make_obj("Bosque troncos", trunks, [EM["bark"]], (0, 0, 0), 1.0)
make_obj("Bosque copas", crowns, [EM["leaf"], EM["leaf2"]], (0, 0, 0), 1.8)
