# Zona: estructura. Se ejecuta en el espacio de nombres compartido de core.py (ver build.py).
# Medidas: audit/medidas.md (COLMAP + escala por puerta 2,03 m / presentador / mesada). Huecos = marco exterior.
# =================================================================== ESTRUCTURA
CUR[0] = "Estructura"
# pared frontal (y=-T..0): puerta (hoja negra 0,82 x 2,03) ; ventana de la cocina a su izquierda (-x)
FRONT_DOOR = (-0.235, 0.615, 0.0, 2.05)
FRONT_WIN = (-0.92, -0.32, 1.20, 2.17)
# pared trasera: dos ventanitas del altillo (casi al nivel del piso del altillo)
BACK_WINS = [(-0.97, -0.40, 2.42, 2.98), (0.30, 0.89, 2.42, 2.98)]
# paredes laterales: (y0, y1, z0, z1)
LEFT_WINS = [(1.51, 2.21, 1.14, 2.14)]                                   # x = XL: ventana sobre la bacha
RIGHT_WINS = [(1.50, 2.21, 1.13, 2.18), (5.10, 5.70, 1.20, 2.12)]        # x = XR: sobre mueble negro/sillón ; baño
TOP = EAVE + 0.22                                                         # remate de paredes bajo la chapa
wall_with_openings("Pared frontal", "y", -T, 0.0, XL - T, XR + T, 0.0, EAVE, [FRONT_DOOR, FRONT_WIN],
                   [M["plywood"], M["siding"]], 0, 1, +1)
box("Hastial frontal", XL - T, XR + T, -T, 0.0, EAVE, TOP, M["siding"])
wall_with_openings("Pared trasera", "y", L, L + T, XL - T, XR + T, 0.0, EAVE, BACK_WINS,
                   [M["plywood"], M["siding"]], 0, 1, -1)
box("Hastial trasero", XL - T, XR + T, L, L + T, EAVE, TOP, M["siding"])
for i, (a, b, c, d) in enumerate(BACK_WINS):
    box(f"Ventana altillo marco {i}", a - 0.05, b + 0.05, L - 0.01, L + 0.005, c - 0.05, d + 0.05, M["trim"])
    box(f"Ventana altillo vidrio {i}", a, b, L + T / 2 - 0.005, L + T / 2 + 0.005, c, d, M["glass"])

wall_with_openings("Pared izquierda", "x", XL - T, XL, 0.0, L, 0.0, EAVE, LEFT_WINS,
                   [M["plywood"], M["siding"]], 0, 1, +1)
wall_with_openings("Pared derecha", "x", XR, XR + T, 0.0, L, 0.0, EAVE, RIGHT_WINS,
                   [M["plywood"], M["siding"]], 0, 1, -1)
# revestimiento blanco del baño (machimbre) sobre paredes laterales y trasera, hasta el cielorraso del baño
box("Baño revest izq", XL, XL + 0.01, BATH_Y, L, 0.0, LOFT_Z, M["white_planks"])
_bw = [w for w in RIGHT_WINS if BATH_Y < (w[0] + w[1]) / 2 < L]
_parts, _y = [], BATH_Y
for (a, b, c, d) in sorted(_bw):
    _parts += [(XR - 0.01, XR, _y, a, 0, LOFT_Z), (XR - 0.01, XR, a, b, 0, c), (XR - 0.01, XR, a, b, d, LOFT_Z)]
    _y = b
_parts.append((XR - 0.01, XR, _y, L, 0, LOFT_Z))
multi("Baño revest der", _parts, [M["white_planks"]])
box("Baño revest fondo", XL, XR, L - 0.01, L, 0.0, LOFT_Z, M["white_planks"])

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
# cielorraso PLANO de multilaminado a z=EAVE (medido 3,12 m; no hay pendiente interior)
box("Cielorraso izq", XL, 0.0, -0.0, L, EAVE, EAVE + 0.03, M["plywood"], tile=1.2)
box("Cielorraso der", 0.0, XR, -0.0, L, EAVE, EAVE + 0.03, M["plywood"], tile=1.2)
# relleno entre el remate de la pared lateral y la chapa
for s_ in (-1, 1):
    a, b = sorted((s_ * W / 2, s_ * (W / 2 + T)))
    box(f"Cenefa {s_}", a, b, -T, L + T, EAVE, TOP, M["siding"])

# tabique del baño con hueco de puerta (hueco entre jambas: 0,64 x 2,10); frente con mural, lado baño blanco
BATH_DOOR = (-0.37, 0.27, 0.0, 2.10)
part = wall_with_openings("Tabique baño", "y", BATH_Y - 0.08, BATH_Y, XL, XR, 0.0, LOFT_Z, [BATH_DOOR],
                          [M["white_planks"], M["mural"]], 0, 1, +1)
# altillo: piso (LOFT_Z..LOFT_Z+0.08) + viga frontal (lleva el riel del granero)
box("Piso altillo", XL, XR, BATH_Y - 0.10, L, LOFT_Z, LOFT_Z + 0.08, M["pine"], tile=1.2)
box("Cielorraso baño", XL, XR, BATH_Y, L, LOFT_Z - 0.01, LOFT_Z, M["white_planks"])
box("Viga altillo", XL, XR, BATH_Y - 0.12, BATH_Y - 0.06, LOFT_Z - 0.12, LOFT_Z + 0.16, M["pine"])
box("Riel granero", -1.0, 0.95, BATH_Y - 0.13, BATH_Y - 0.11, LOFT_Z - 0.06, LOFT_Z - 0.03, M["blackmetal"])
