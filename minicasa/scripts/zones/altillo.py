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
_vg = _bb("Viga altillo", (0, 0, BATH_Y - 0.12, BATH_Y - 0.06, 0, LOFT_Z + 0.16))
BY0 = max(LY0 + 0.02, _vg[3] + 0.005) if _vg[5] > LF else LY0 + 0.02   # detrás de la cenefa (sobresale del piso)
BY1 = L - 0.04
MH = 0.20                                           # colchón ≈0,20 (puntos a 2,55–2,62); techo a EAVE
# Capas apiladas sin cruzarse (cada una apoya sobre la anterior con 2–3 mm de luz):
#   colchón LF..LF+MH → acolchado (manta fina que cae por los costados) → edredón tostado / almohadas.
box("Colchon", BX0, BX1, BY0, BY1, LF, LF + MH, M["mattress"])
ZA = LF + MH + 0.002                                # cara inferior del acolchado
AT = 0.05                                           # espesor del acolchado
AY1 = BY1 - 0.52                                    # deja libre la cabecera para las almohadas
multi("Acolchado", [(BX0 - 0.03, BX1 + 0.03, BY0 - 0.03, AY1, ZA, ZA + AT, 0),            # sobre el colchón
                    (BX0 - 0.03, BX0 - 0.003, BY0 - 0.03, AY1, LF + 0.155, ZA, 0),      # cae a la izquierda
                    (BX1 + 0.003, BX1 + 0.03, BY0 - 0.03, AY1, LF + 0.155, ZA, 0),      # cae a la derecha
                    (BX0 - 0.003, BX1 + 0.003, BY0 - 0.03, BY0 - 0.003, max(LF + 0.155, _vg[5] + 0.003), ZA, 0)],   # pies (sobre la cenefa)
      [M_duvet])
ZT = ZA + AT + 0.003                                # base del edredón y de la manta
# edredón tostado amontonado: tres bultos suaves (elipsoides) con huellas que no se pisan
for k, (cx, cy, sx, sy, h) in enumerate(((0.45, 0.60, 0.55, 0.62, 0.16), (0.95, 0.80, 0.42, 0.50, 0.20), (0.62, 1.17, 0.48, 0.24, 0.12))):
    sphere(f"Edredon {k}", BX0 + cx, BY0 + cy, ZT + h / 2, 0.5, M_tan, sx=sx, sy=sy, sz=h, seg=12)
box("Manta altillo", BX0 + 0.05, BX1 - 0.05, BY0 + 0.02, BY0 + 0.26, ZT, ZT + 0.04, M_tan)   # doblada a los pies
for k in range(2):
    cx = BX0 + MW * (0.27 + 0.46 * k)
    sphere(f"Almohada {k}", cx, BY1 - 0.25, LF + MH + 0.003 + 0.08, 0.5, M["white"], sx=0.60, sy=0.40, sz=0.16, seg=12)
