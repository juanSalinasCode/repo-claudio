# Zona: puerta_luces. Se ejecuta en el espacio de nombres compartido de core.py (ver build.py).
# =================================================================== PUERTA DE ENTRADA + LUCES
CUR[0] = "Puerta y luces"
d0, d1 = FRONT_DOOR[0], FRONT_DOOR[1]
multi("Marco puerta", [(d0 - 0.05, d0, -T - 0.02, 0.01, 0, 2.07), (d1, d1 + 0.05, -T - 0.02, 0.01, 0, 2.07),
                       (d0 - 0.05, d1 + 0.05, -T - 0.02, 0.01, 2.02, 2.07)], [M["trim"]])
bm = bmesh.new(); pv = (d1 - 0.01, -0.06, 0.0)
add_box(bm, d0 + 0.01, d1 - 0.01, -0.085, -0.035, 0.01, 2.01, pivot=pv)
bm.normal_update()
for f in bm.faces:
    f.material_index = 0 if f.normal.y < -0.5 else 1
add_box(bm, d0 + 0.06, d0 + 0.09, -0.11, -0.085, 0.95, 1.10, pivot=pv, mi=2)   # manija exterior
add_box(bm, d0 + 0.06, d0 + 0.09, -0.035, -0.01, 0.95, 1.10, pivot=pv, mi=2)   # manija interior
door = make_obj("Puerta entrada", bm, [M["yellow"], M["chalk"], M["steel"]], pv)
interactive(door, "rot", "Puerta de entrada", axis="Z", angle=-100)
# puerta mosquitero blanca (exterior, abierta hacia afuera como en el video)
bm = bmesh.new(); pv = (d0 - 0.02, -T - 0.05, 0.0)
add_box(bm, d0, d1, -T - 0.07, -T - 0.04, 0.02, 2.00, pivot=pv)
bm.normal_update()
mosq = make_obj("Puerta mosquitero", bm, [M["trim"]], pv)
interactive(mosq, "rot", "Puerta mosquitero", axis="Z", angle=-95)
# araña negra con 6 lamparitas + llave de luz
CHY = 2.30
cyl("Araña barra", 0, CHY, 2.75, RIDGE, 0.008, M["blackmetal"], verts=6)
for k in range(6):
    a = k * math.pi / 3
    x, y = 0.30 * math.cos(a), CHY + 0.30 * math.sin(a)
    multi(f"Araña brazo {k}", [(min(0, x) - 0.008, max(0, x) + 0.008, min(CHY, y) - 0.008, max(CHY, y) + 0.008, 2.74, 2.76, 0)], [M["blackmetal"]])
    cyl(f"Araña vela {k}", x, y, 2.76, 2.84, 0.012, M["blackmetal"], verts=6)
    sphere(f"Araña lamparita {k}", x, y, 2.88, 0.035, M["bulb"], seg=8)
for k in range(3):
    sphere(f"Spot cocina {k}", XL + 0.25, 1.30 + k * 0.40, 2.25, 0.04, M["bulb"], seg=8)
box("Riel spots", XL + 0.02, XL + 0.06, 1.20, 2.20, 2.28, 2.31, M["blackmetal"])
llave = box("Llave de luz", 1.00 + 0.05, 1.00 + 0.13, 0.0, 0.015, 1.15, 1.27, M["white"])
interactive(llave, "light", "Llave de luz")
for name, (x, y, z) in {"luz_arana": (0, CHY, 2.70), "luz_cocina": (XL + 0.4, 1.6, 2.2), "luz_bano": (0.6, L - 0.4, 1.9),
                        "luz_altillo": (0, 5.2, 3.1), "luz_frente": (0.5, -0.6, 2.1)}.items():
    e = bpy.data.objects.new(name, None)
    e.location = (x, y, z)
    e["light_point"] = 1
    link(e)
# punto de partida de la cámara
spawn = bpy.data.objects.new("spawn", None); spawn.location = (0.55, -4.5, 0.0); spawn["spawn"] = 1; link(spawn)
loftspot = bpy.data.objects.new("loft_spot", None); loftspot.location = (0.0, 4.48, LOFT_Z + 0.08); loftspot["loft_spot"] = 1; link(loftspot)
downspot = bpy.data.objects.new("down_spot", None); downspot.location = (0.2, 3.4, 0.0); downspot["down_spot"] = 1; link(downspot)

