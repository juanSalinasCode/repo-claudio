# Zona: exterior. Se ejecuta en el espacio de nombres compartido de core.py (ver build.py).
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

