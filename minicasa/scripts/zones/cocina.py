# Zona: cocina. Se ejecuta en el espacio de nombres compartido de core.py (ver build.py).
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

