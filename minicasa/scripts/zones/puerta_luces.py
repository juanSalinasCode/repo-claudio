# Zona: puerta_luces. Se ejecuta en el espacio de nombres compartido de core.py (ver build.py).
# Referencia: f0001–f0012 (puerta, mosquitero, faroles, felpudo), f0013–f0016 (araña), f0022 (spots), f0023–f0030
# (cara interior negra tipo pizarrón). Ver audit/exterior.md.
# =================================================================== PUERTA DE ENTRADA + LUCES
CUR[0] = "Puerta y luces"
d0, d1, dz0, dz1 = FRONT_DOOR
dcx = (d0 + d1) / 2
CAS = 0.07                                   # contramarco blanco exterior
_deck_z = globals().get("EXT_DECK_Z", -0.04)
_belt_z = globals().get("BELT_Z", EAVE)
_clad = globals().get("CLAD", 0.0)
PL = dict(
    yellow=mat("Puerta amarilla real", (0.80, 0.56, 0.015), rough=0.45),       # f0007 #c19e18 en sombra
    coir=mat("Felpudo coco", tex="exterior_felpudo.jpg", rough=1.0),
    frost=mat("Vidrio esmerilado farol", (1.0, 0.9, 0.7), emit=(1.0, 0.82, 0.55), emit_strength=3.0),
    sensor=mat("Luz solar sensor", (0.62, 0.62, 0.60), rough=0.5),
)

# --- contramarco blanco exterior + revestimiento del vano + umbral
multi("Marco puerta", [
    (d0 - CAS, d0, -T - 0.025, -T + 0.001, dz0, dz1 + CAS), (d1, d1 + CAS, -T - 0.025, -T + 0.001, dz0, dz1 + CAS),
    (d0 - CAS, d1 + CAS, -T - 0.025, -T + 0.001, dz1, dz1 + CAS),
    (d0, d0 + 0.015, -T, 0.0, dz0, dz1), (d1 - 0.015, d1, -T, 0.0, dz0, dz1), (d0, d1, -T, 0.0, dz1 - 0.015, dz1),
    (d0 - 0.05, d0, 0.0, 0.012, dz0, dz1 + 0.05), (d1, d1 + 0.05, 0.0, 0.012, dz0, dz1 + 0.05),   # marco interior
    (d0 - 0.05, d1 + 0.05, 0.0, 0.012, dz1, dz1 + 0.05)], [M["trim"]])
box("Umbral", d0 - 0.02, d1 + 0.02, -T - 0.04, 0.0, -0.012, 0.012, M["gray"])

# --- puerta de entrada: amarilla afuera, negra (pizarrón) adentro; bisagra a la IZQUIERDA visto desde afuera
#     (x = d0) y abre hacia adentro (f0007, f0010, f0012).
bm = bmesh.new(); pv = (d0 + 0.012, -0.02, 0.0)
add_box(bm, d0 + 0.015, d1 - 0.015, -0.065, -0.02, 0.012, dz1 - 0.005, pivot=pv)
bm.normal_update()
for f in bm.faces:
    f.material_index = 1 if f.normal.y > 0.5 else 0
hx = d1 - 0.08
add_box(bm, hx - 0.025, hx + 0.025, -0.09, -0.065, 0.95, 1.00, pivot=pv, mi=2)     # pomo exterior
add_box(bm, hx - 0.02, hx + 0.02, -0.08, -0.065, 1.10, 1.14, pivot=pv, mi=2)       # cerradura
add_box(bm, hx - 0.10, hx + 0.02, -0.02, 0.0, 0.96, 0.99, pivot=pv, mi=3)          # manija interior negra
door = make_obj("Puerta entrada", bm, [PL["yellow"], M["chalk"], M["steel"], M["blackmetal"]], pv)
interactive(door, "rot", "Puerta de entrada", axis="Z", angle=95)

# --- puerta mosquitero blanca (storm door): bisagra izquierda, abre hacia afuera; dos vidrios + zócalo ciego
#     (f0001/f0004: vidrio superior 1.39–2.11 m, travesaño, vidrio inferior 0.59–1.33 m, zócalo hasta 0.59 m).
sx0, sx1, sz1 = d0 - 0.035, d1 + 0.035, dz1 + 0.035
hgt = sz1 / 2.11 if sz1 > 0 else 1.0
gz = [0.59 * hgt * 0.96, 1.33 * hgt * 0.96, 1.39 * hgt * 0.96, sz1 - 0.10]
ST = 0.085
yo0, yo1 = -T - 0.065, -T - 0.035
bm = bmesh.new(); pv = (sx0, (yo0 + yo1) / 2, 0.0)
for p in [(sx0, sx0 + ST, 0.01, sz1), (sx1 - ST, sx1, 0.01, sz1), (sx0 + ST, sx1 - ST, sz1 - 0.10, sz1),
          (sx0 + ST, sx1 - ST, gz[1], gz[2]), (sx0 + ST, sx1 - ST, 0.01, gz[0])]:
    add_box(bm, p[0], p[1], yo0, yo1, p[2], p[3], pivot=pv, mi=0)
for (za, zb) in [(gz[0], gz[1]), (gz[2], gz[3])]:
    add_box(bm, sx0 + ST, sx1 - ST, yo0 + 0.012, yo1 - 0.012, za, zb, pivot=pv, mi=1)
add_box(bm, sx1 - 0.075, sx1 - 0.055, yo0 - 0.04, yo0, 1.00, 1.16, pivot=pv, mi=2)   # tirador
bm.normal_update()
mosq = make_obj("Puerta mosquitero", bm, [M["trim"], M["glass"], M["blackmetal"]], pv)
interactive(mosq, "rot", "Puerta mosquitero", axis="Z", angle=-105)

# --- felpudo de coco delante de la puerta (f0007)
box("Felpudo", dcx - 0.40, dcx + 0.40, -T - 0.60, -T - 0.06, _deck_z, _deck_z + 0.015, PL["coir"], tile=0.8)

# --- faroles: farol caja negro con vidrio esmerilado a la derecha de la puerta + luz solar con sensor
#     centrada sobre la puerta, apoyada en la tapajunta horizontal (f0004, f0005, f0007).
fx, fz, fy = d1 + CAS + 0.20, dz1 + CAS + 0.02, -T
_lw2, _lh = 0.075, 0.12                         # farol ≈ 0.15 × 0.24 m (f0007)
_fr = [(fx - 0.05, fx + 0.05, fy - 0.015, fy, fz - _lh - 0.04, fz + _lh + 0.02),                    # placa
       (fx - _lw2 - 0.01, fx + _lw2 + 0.01, fy - 0.15, fy - 0.015, fz + _lh, fz + _lh + 0.035),       # sombrerete
       (fx - _lw2, fx + _lw2, fy - 0.14, fy - 0.015, fz - _lh - 0.02, fz - _lh)]                       # base
for (xa, xb) in [(fx - _lw2, fx - _lw2 + 0.012), (fx + _lw2 - 0.012, fx + _lw2), (fx - 0.005, fx + 0.005)]:
    _fr.append((xa, xb, fy - 0.14, fy - 0.128, fz - _lh, fz + _lh))          # parantes frontales + central
_fr.append((fx - _lw2, fx + _lw2, fy - 0.14, fy - 0.128, fz - 0.005, fz + 0.005))   # travesaño
for xs in (fx - _lw2, fx + _lw2 - 0.012):
    _fr.append((xs, xs + 0.012, fy - 0.14, fy - 0.015, fz - _lh, fz + _lh))  # cantos laterales
multi("Farol 0", _fr, [M["blackmetal"]])
box("Farol vidrio 0", fx - _lw2 + 0.008, fx + _lw2 - 0.008, fy - 0.132, fy - 0.02, fz - _lh, fz + _lh, PL["frost"])
multi("Farol 1", [(dcx - 0.08, dcx + 0.08, -T - _clad - 0.07, -T - _clad, _belt_z + 0.03, _belt_z + 0.15),
                  (dcx - 0.085, dcx + 0.085, -T - _clad - 0.09, -T - _clad - 0.005, _belt_z + 0.15, _belt_z + 0.165)],
      [PL["sensor"]])
box("Farol 1 sensor", dcx - 0.06, dcx + 0.06, -T - _clad - 0.075, -T - _clad - 0.01, _belt_z + 0.01, _belt_z + 0.03, M["black"])

# --- araña negra (f0013–f0016): florón, cable largo, columna central y 6 brazos que salen de abajo,
#     van hacia afuera casi horizontales y suben en vertical hasta un portavela con lamparita globo.
CHY = 2.90                       # cámaras entrada2/entrada3 (f0013/f0014): brazos a y≈2.9, x≈0
CH_ARM_Z = 2.22                  # nivel de los brazos
CH_R = 0.27                      # radio de los brazos
CH_TOP = CH_ARM_Z + 0.42         # tope de la columna central
CH_CEIL = globals().get("CEIL_Z", RIDGE)   # cielorraso sobre la araña (las cámaras sugieren ≈3.3 m)

def rod(bm, p0, p1, r, seg=6, mi=0):
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    res = bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r, depth=d.length)
    rot = d.to_track_quat("Z", "Y").to_matrix()
    bmesh.ops.rotate(bm, verts=res["verts"], matrix=rot)
    bmesh.ops.translate(bm, verts=res["verts"], vec=(p0 + p1) / 2)
    for v in res["verts"]:
        for f in v.link_faces:
            f.material_index = mi

bm = bmesh.new()
rod(bm, (0, CHY, CH_CEIL - 0.035), (0, CHY, CH_CEIL + 0.005), 0.06, seg=12)        # florón
rod(bm, (0, CHY, CH_TOP), (0, CHY, CH_CEIL - 0.03), 0.005, seg=4)                # cable
rod(bm, (0, CHY, CH_ARM_Z - 0.02), (0, CHY, CH_TOP), 0.012, seg=8)             # columna
rod(bm, (0, CHY, CH_ARM_Z + 0.08), (0, CHY, CH_ARM_Z + 0.16), 0.022, seg=8)    # anillo
rod(bm, (0, CHY, CH_TOP - 0.04), (0, CHY, CH_TOP), 0.02, seg=8)                # remate
tips = []
for k in range(6):
    a = math.radians(30 + 60 * k)
    ca, sa = math.cos(a), math.sin(a)
    p_hub = (0.015 * ca, CHY + 0.015 * sa, CH_ARM_Z + 0.06)
    p_el = (0.09 * ca, CHY + 0.09 * sa, CH_ARM_Z)
    p_out = (CH_R * ca, CHY + CH_R * sa, CH_ARM_Z)
    p_up = (CH_R * ca, CHY + CH_R * sa, CH_ARM_Z + 0.24)
    rod(bm, p_hub, p_el, 0.006); rod(bm, p_el, p_out, 0.006); rod(bm, p_out, p_up, 0.006)
    rod(bm, (p_up[0], p_up[1], p_up[2] - 0.01), (p_up[0], p_up[1], p_up[2] + 0.05), 0.014, seg=8)   # portavela
    tips.append((p_up[0], p_up[1], p_up[2] + 0.085))
bm.normal_update()
make_obj("Araña", bm, [M["blackmetal"]], (0, 0, 0), 1.0)
bm = bmesh.new()
for (x, y, z) in tips:
    r_ = bmesh.ops.create_uvsphere(bm, u_segments=8, v_segments=6, radius=0.032)
    bmesh.ops.translate(bm, verts=r_["verts"], vec=(x, y, z))
bm.normal_update()
make_obj("Araña lamparitas", bm, [M["bulb"]], (0, 0, 0), 1.0)

# --- riel con 3 spots negros sobre la ventana grande de la cocina (f0022)
_lw = globals().get("LEFT_WINS", [(1.20, 2.25, 1.05, 2.05)])
_kw = max(_lw, key=lambda w: w[1] - w[0])
ry_c, rz = (_kw[0] + _kw[1]) / 2, min(_kw[3] + 0.22, EAVE - 0.06)
box("Riel spots", XL + 0.005, XL + 0.035, ry_c - 0.40, ry_c + 0.40, rz - 0.015, rz + 0.015, M["blackmetal"])
for k in range(3):
    yk = ry_c - 0.28 + k * 0.28
    multi(f"Spot cocina cuerpo {k}", [(XL + 0.035, XL + 0.07, yk - 0.01, yk + 0.01, rz - 0.01, rz + 0.01),
                                       (XL + 0.05, XL + 0.11, yk - 0.03, yk + 0.03, rz - 0.10, rz - 0.01)], [M["blackmetal"]])
    box(f"Spot cocina {k}", XL + 0.055, XL + 0.105, yk - 0.025, yk + 0.025, rz - 0.105, rz - 0.10, M["bulb"])

# --- llave de luz: del lado del picaporte (d1), adentro
llave = box("Llave de luz", d1 + 0.10, d1 + 0.18, 0.0, 0.015, 1.15, 1.27, M["white"])
interactive(llave, "light", "Llave de luz")

for name, (x, y, z) in {"luz_arana": (0, CHY, CH_ARM_Z + 0.20), "luz_cocina": (XL + 0.4, ry_c, rz - 0.2),
                        "luz_bano": (0.6, L - 0.4, 1.9), "luz_altillo": (0, 5.2, 3.1),
                        "luz_frente": (fx, -T - 0.4, fz)}.items():
    e = bpy.data.objects.new(name, None)
    e.location = (x, y, z)
    e["light_point"] = 1
    link(e)
# punto de partida de la cámara (frente a la escalera del deck)
spawn = bpy.data.objects.new("spawn", None); spawn.location = (dcx, -4.5, 0.0); spawn["spawn"] = 1; link(spawn)
loftspot = bpy.data.objects.new("loft_spot", None); loftspot.location = (0.0, 4.48, LOFT_Z + 0.08); loftspot["loft_spot"] = 1; link(loftspot)
downspot = bpy.data.objects.new("down_spot", None); downspot.location = (0.2, 3.4, 0.0); downspot["down_spot"] = 1; link(downspot)
