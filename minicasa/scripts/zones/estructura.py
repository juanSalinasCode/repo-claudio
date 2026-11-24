# Zona: estructura. Se ejecuta en el espacio de nombres compartido de core.py (ver build.py).
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

