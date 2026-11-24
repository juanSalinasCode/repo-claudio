# Zona: altillo. Se ejecuta en el espacio de nombres compartido de core.py (ver build.py).
# =================================================================== ALTILLO
CUR[0] = "Altillo"
box("Colchon", XL + 0.15, XR - 0.15, BATH_Y + 0.15, L - 0.10, LOFT_Z + 0.08, LOFT_Z + 0.30, M["mattress"])
box("Edredon", XL + 0.15, XR - 0.15, BATH_Y + 0.15, L - 0.60, LOFT_Z + 0.30, LOFT_Z + 0.36, M["mattress"])
box("Manta altillo", XL + 0.25, 0.40, BATH_Y + 0.25, L - 0.65, LOFT_Z + 0.36, LOFT_Z + 0.40, M["blanket"])
for k in range(2):
    box(f"Almohada {k}", XL + 0.30 + k * 1.0, XL + 0.95 + k * 1.0, L - 0.55, L - 0.15, LOFT_Z + 0.30, LOFT_Z + 0.42, M["white"])
box("Baranda altillo", XL, XR - 0.50, BATH_Y - 0.10, BATH_Y - 0.06, LOFT_Z + 0.08, LOFT_Z + 0.25, M["pine"])

