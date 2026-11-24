# Zona: living. Se ejecuta en el espacio de nombres compartido de core.py (ver build.py).
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

