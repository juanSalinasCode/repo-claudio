# Zona: escalera. Se ejecuta en el espacio de nombres compartido de core.py (ver build.py).
# =================================================================== ESCALERA ESCONDIDA
CUR[0] = "Escalera"
# panel con ranuras en la pared derecha (sobre el sillón)
box("Panel escalera", XR - 0.03, XR - 0.005, 2.95, BATH_Y - 0.08, 0.90, LOFT_Z, M["pine"])
STEPS = 6
for i in range(STEPS):
    y = 3.02 + i * 0.22
    z = 0.95 + i * 0.20   # bisagra de cada escalón
    bm = bmesh.new(); pv = (XR - 0.035, y, z)
    # plegado: vertical (sobresale hacia arriba), al desplegar gira -90° en Y => horizontal hacia -x
    add_box(bm, XR - 0.065, XR - 0.035, y, y + 0.38, z, z + 0.26, pivot=pv)
    bm.normal_update()
    st = make_obj(f"Escalon oculto {i + 1}", bm, [M["pine"]], pv)
    interactive(st, "rot", "Escalera escondida", group="escalera", axis="Y", angle=-90)
# acceso al altillo (zona clickeable invisible sobre el último escalón)
acc = box("Subir al altillo", XR - 0.45, XR - 0.05, 4.05, BATH_Y - 0.10, 1.95, 2.40, M["glass"])
interactive(acc, "loft", "Subir / bajar del altillo", group="altillo", extra={"needs": "escalera"})
acc.hide_render = True

