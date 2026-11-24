# Zona: escalera. Se ejecuta en el espacio de nombres compartido de core.py (ver build.py).
# =================================================================== ESCALERA ESCONDIDA
# Como en el video (f0103-f0109 plegada, f0180-f0203 desplegada): sobre el sillón, en la pared derecha, hay un panel
# de pino en diagonal con 8 pedadas plegadas hacia ABAJO (rectángulos verticales en diente de sierra, con una ranura
# oscura arriba de cada uno) y un larguero exterior en diagonal debajo de ellas. Al desplegar, cada pedada gira 90°
# sobre su bisagra (canto de la pared, arriba) y queda horizontal; el larguero sube y sale de la pared
# (paralelogramo) y queda como zanca/baranda exterior de una escalera tipo "molinero" que llega al altillo.
CUR[0] = "Escalera"
M_stair = mat("Pino escalera", (0.51, 0.32, 0.17), rough=0.6)
M_slot = mat("Ranura oscura", (0.03, 0.02, 0.015), rough=0.9)

# Presupuesto (cocina.py): arranca bajo el final de la ventana +x (pie del larguero ~1.96-2.04), 2 pedadas delante
# del sillón (SOFA_Y0) y las demás por encima del respaldo; llega al altillo en STAIR_Y1 (junto al tabique).
STEPS = 8
ST_TOP = LOFT_Z + 0.08                  # piso terminado del altillo
ST_Z0 = 0.32                            # primera pedada (más alta, para que plegada no atraviese el piso)
ST_RISE = (ST_TOP - ST_Z0) / STEPS      # 0.26
ST_D = 0.28                             # profundidad de la pedada (sale de la pared hacia -x)
ST_TH = 0.035                           # espesor de la pedada
ST_Y1 = STAIR_Y1                        # borde del altillo (llegada)
ST_RUN = 0.21
ST_TW = ST_RUN - 0.02                   # largo de cada pedada (en y); plegadas quedan separadas por la ranura
ST_X = XR - 0.012                       # plano de las bisagras (sobre el panel de pino)
ST_Y = [ST_Y1 - (STEPS - i) * ST_RUN - 0.05 for i in range(STEPS)]   # inicio (y) de cada pedada
ST_Z = [ST_Z0 + ST_RISE * i for i in range(STEPS)]                  # nivel superior de cada pedada
assert ST_Y[1] + ST_TW <= SOFA_Y0 and ST_Z[2] - ST_TH > 0.76       # 2 pedadas delante del sillón, resto sobre el respaldo


def _band(name, x0, x1, pts_yz, m_):
    """Polígono en el plano YZ extruido en x (de x0 a x1)."""
    bm = bmesh.new()
    a = [bm.verts.new((x0, y, z)) for y, z in pts_yz]
    b = [bm.verts.new((x1, y, z)) for y, z in pts_yz]
    bm.faces.new(a); bm.faces.new(b[::-1])
    n = len(pts_yz)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new([a[i], a[j], b[j], b[i]])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.normal_update()
    return bm


# línea de bisagras: z = ST_Z[i] en y = ST_Y[i] + ST_TW / 2
_slope = ST_RISE / ST_RUN
_y0c = ST_Y[0] + ST_TW / 2
def _hinge_z(y):
    return ST_Z[0] + (y - _y0c) * _slope
def _y_at(z, off):
    return _y0c + (z - off - ST_Z[0]) / _slope

# panel de pino fijo en la pared (fondo claro donde cuelgan las pedadas plegadas)
_up, _dn = 0.12, ST_D + 0.30
zt = ST_TOP + 0.10
pts = [(_y_at(0.0, _up), 0.0), (_y_at(0.0, -_dn), 0.0), (ST_Y1 - 0.03, _hinge_z(ST_Y1 - 0.03) - _dn), (ST_Y1 - 0.03, _hinge_z(ST_Y1 - 0.03) + _up)]
bm = _band("Panel escalera", XR - 0.012, XR - 0.002, pts, M_stair)
make_obj("Panel escalera", bm, [M_stair])

for i in range(STEPS):
    y, zt_ = ST_Y[i], ST_Z[i]
    pv = (ST_X, y + ST_TW / 2, zt_ - ST_TH)
    bm = bmesh.new()
    # plegada: cuelga hacia abajo desde la bisagra, apoyada contra el panel
    add_box(bm, ST_X - ST_TH, ST_X, y, y + ST_TW, zt_ - ST_TH - ST_D, zt_ - ST_TH, pivot=pv)
    bm.normal_update()
    st = make_obj(f"Escalon oculto {i + 1}", bm, [M_stair], pv)
    # giro +90° en Y: la pedada pasa de colgar (-z) a horizontal hacia el pasillo (-x)
    interactive(st, "rot", "Escalera escondida", group="escalera", axis="Y", angle=90)
    # ranura oscura sobre cada pedada plegada (la "ranura" que se ve en la pared)
    box(f"Ranura escalon {i + 1}", XR - 0.017, XR - 0.012, y, y + ST_TW, zt_ - ST_TH, zt_ - ST_TH + 0.012, M_slot)

# larguero exterior: desplegado queda a ST_D de la pared, bajo los cantos exteriores de las pedadas;
# plegado (estado inicial) está contra el panel y ST_D más abajo -> slide (+ST_D hacia la pared, -ST_D en z) invertido.
# Plegado queda contra las pedadas plegadas, a la misma altura (solo desliza en x): no atraviesa el piso.
_lt, _lb = 0.02 - ST_TH, -0.11          # bordes superior/inferior del larguero respecto de la línea de bisagras
ze = ST_TOP - 0.10                      # remata bajo el canto del altillo
pts = [(_y_at(0.0, _lt), 0.0), (_y_at(0.0, _lb), 0.0), (_y_at(ze, _lb), ze), (_y_at(ze, _lt), ze)]
_ycut = STAIR_Y1 - 0.02                 # no pasa del tabique (y <= 3.85)
pts = [(min(y, _ycut), z) for y, z in pts]
xo = ST_X - ST_TH - 0.036
bm = _band("Larguero escalera", xo, xo + 0.035, pts, M_stair)
lpv = (xo, (pts[0][0] + pts[2][0]) / 2, 0.0)
bmesh.ops.translate(bm, verts=bm.verts, vec=Vector((0, -lpv[1], 0)))
lar = make_obj("Larguero escalera", bm, [M_stair], (0, lpv[1], 0))
lar.location = (0, lpv[1], 0)
interactive(lar, "slide", "Escalera escondida", group="escalera", vec=(-(ST_D - ST_TH - 0.001), 0, 0))

# acceso al altillo (zona clickeable invisible sobre el último escalón)
acc = box("Subir al altillo", XR - ST_D - 0.05, XR - 0.05, ST_Y[-2], ST_Y1, ST_Z[-2], ST_TOP + 0.35, M["glass"])
interactive(acc, "loft", "Subir / bajar del altillo", group="altillo", extra={"needs": "escalera"})
acc.hide_render = True
