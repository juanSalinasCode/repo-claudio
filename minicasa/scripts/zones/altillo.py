# Zona: altillo. Se ejecuta en el espacio de nombres compartido de core.py (ver build.py).
# =================================================================== ALTILLO
# Según f0190–f0217: colchón grueso blanco apoyado directo en el piso del altillo, contra la pared XL,
# cabecera hacia las ventanas del fondo; acolchado blanco + edredón tostado arrugado en el centro y
# almohadas blancas al fondo. Desde abajo (f0100–f0132) se ve el borde del colchón y un acolchado blanco
# doblado asomando sobre la cenefa. No hay baranda: el altillo queda abierto (solo la escalera).
CUR[0] = "Altillo"
LF = LOFT_Z + 0.08                                  # cara superior del piso del altillo
_pa = bpy.data.objects.get("Piso altillo")
LY0 = min((pa.location + v.co).y for pa in [_pa] for v in pa.data.vertices) if _pa else BATH_Y - 0.10
M_duvet = mat("Acolchado blanco", (0.93, 0.93, 0.95), rough=0.95)
M_tan = mat("Edredon tostado", (0.80, 0.68, 0.52), rough=0.95)
MW = 1.40                                           # colchón de 2 plazas chico (ancho en x)
BX0, BX1 = XL + 0.04, XL + 0.04 + MW
BY0 = LY0 + 0.02                                    # al ras del borde del altillo (como en f0110)
BY1 = min(L - 0.04, BY0 + 1.95)
box("Colchon", BX0, BX1, BY0, BY1, LF, LF + 0.24, M["mattress"])
# acolchado blanco grueso cubriendo el colchón (un poco más ancho, cae por los lados)
box("Acolchado", BX0 - 0.03, BX1 + 0.03, BY0 - 0.02, BY1 - 0.45, LF + 0.12, LF + 0.34, M_duvet)
# edredón tostado amontonado en el centro (bulto irregular de 3 piezas)
for k, (dx, dy, sx, sy, h) in enumerate(((0.55, 0.55, 0.55, 0.70, 0.16), (0.75, 0.95, 0.45, 0.55, 0.20), (0.62, 0.30, 0.50, 0.30, 0.12))):
    sphere(f"Edredon {k}", BX0 + dx, BY0 + dy, LF + 0.34, 0.5, M_tan, sx=sx, sy=sy, sz=h, seg=12)
box("Manta altillo", BX0 + 0.25, BX1 - 0.05, BY0 + 0.20, BY0 + 1.20, LF + 0.33, LF + 0.37, M_tan)
for k in range(2):
    cx = BX0 + MW * (0.27 + 0.46 * k)
    sphere(f"Almohada {k}", cx, BY1 - 0.25, LF + 0.31, 0.5, M["white"], sx=0.60, sy=0.40, sz=0.16, seg=12)
