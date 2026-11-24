# Zona: bano. Se ejecuta en el espacio de nombres compartido de core.py (ver build.py).
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

