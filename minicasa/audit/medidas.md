# Medidas y cámaras (agente de Medidas)

Sistema: metros, Z arriba, cara interior de la pared frontal en y=0, cara interior de la trasera en y=L,
interior x ∈ [XL, XR] (cocina/bacha en −x, mueble negro/sillón/escalera en +x), piso interior z=0.

## Método

1. **COLMAP** (SIFT CPU, OPENCV, 217 fotogramas). Corrida original: 4 modelos. Agregué ~3800 pares
   no secuenciales (`matches_importer`) y re-mapeé con umbrales más bajos (`abs_pose_min_num_inliers 20`, etc.):
   - modelo A (`sparse2/1`): f0011–f0020 + f0092–f0217 = **136 imágenes** (entrada, living, granero, baño, escalera, altillo).
   - modelo B (`sparse2/2`): f0022–f0091 = **70 imágenes** (cocina mirando al frente).
   - Total **206/217 registradas**. Sin registrar: exterior f0001–f0010 y f0021. Error de reproyección 0,74–0,84 px.
   - Focal ≈ 597 px (fov_h = 62,1–62,2°), distorsión despreciable (k1 ≈ −0,005), punto principal centrado.
   A y B no comparten imágenes (miran en sentidos opuestos); los uní con las paredes y una ventana común.
2. **Vertical y orientación**: puntos de fuga sobre bordes de todas las imágenes (búsqueda en la esfera, ±1,5°),
   refinado con los planos de las paredes largas (RANSAC por región). Paredes verticales a <1°, cielorraso
   horizontal a <1° (normal (−0,018, 0,003, 0,9999)).
3. **Origen**: x = centro entre paredes largas; z = piso (cluster superior de puntos del piso; el piso brillante
   da reflejos más abajo); y = plano de la pared frontal (modelo B). El modelo A se posicionó en y con el borde
   trasero de la ventana +x (y=2,20 en ambos modelos, verificado en f0091/f0092/f0180/f0191; ±4 cm).
4. **Escala** (B; A = B × 2,425, razón de anchos y altos medidos en ambos, coinciden al 0,3 %):
   - hoja de la puerta de entrada pintada de negro: 17,0 u de alto y 6,75 u de ancho, razón 2,52 → puerta
     estándar 80"×32" (2,03 × 0,81 m) → 0,1194 m/u;
   - presentador (1,70 m): 1,65 m en f0024 (paso largo) y 1,67 m en f0171 (mirando hacia arriba) → 0,121–0,122;
   - verificación independiente: la mesada queda a **0,88–0,90 m** (estándar 0,90–0,91) ✓.
   - Adoptado 0,1205 m/u (A: 0,2922). **Incertidumbre de escala ±3 %** (p. ej. ±6 cm en W, ±9 cm en altura).
5. **Huecos**: rayo del píxel (marcado a mano en recortes con grilla) ∩ plano de la pared, en 2–4 fotogramas
   por elemento. Dispersión típica 1–4 cm.
6. **Verificación**: `scripts/audit.py` con las 26 cámaras: puerta, ventanas, cielorraso/paredes, hueco del baño
   y ventanas del altillo coinciden con las fotos con error típico **≈3–8 px a 720 px** (sin offset sistemático).
   Láminas en `audit/medidas/`.

Archivos de trabajo: `/opt/3d/minicasa/work/medidas/` (modelos TXT `t2_1`, `t2_2`, `align.json`, scripts en `py/`).

## Medidas de la cáscara (→ `scripts/core.py`)

| constante | valor | cómo | ± |
|---|---|---|---|
| W (ancho int.) | **2,00** | paredes a −1,01 / +0,99 | 0,06 |
| L (largo int.) | **5,79** | pared trasera (baño/altillo) | 0,08 |
| EAVE = altura de pared = cielorraso | **3,12** | cielorraso **plano** (no hay cumbrera interior) | 0,09 |
| RIDGE | 3,12 | = EAVE (techo exterior casi plano, tipo "shed"; la fachada frontal termina en una cenefa recta) | – |
| BATH_Y (cara lado baño del tabique) | **3,94** | cara living del tabique 3,86 (mural), cara baño 3,94 | 0,04 |
| LOFT_Z (cielorraso baño / bajo piso altillo) | **2,32** | riel granero ≈2,30; piso altillo terminado ≈2,40 (coincide con el borde inferior de las ventanas traseras) | 0,05 |
| T | **0,20** | interior medido 2,00 (3 referencias independientes); la fachada en f0001 mide ≈2,4 m → paredes gruesas (pedido de exterior) | 0,05 |
| GROUND | −0,50 | 2 escalones del deck (f0001) | 0,1 |

Cielorraso: medido **plano** (normal a <1° de la vertical en el modelo A, 1300 puntos; en la cocina (modelo B) 2,98–3,11 con pocos puntos). La inclinación que se ve en las tomas de la cocina es perspectiva del gran angular; las láminas cocina1–5 calzan con cielorraso plano. Tabique lado baño: panel blanco liso; piso del altillo madera oscura (#736A60).

Altillo: altura libre ≈ 0,72 m (3,12 − 2,40). Colchón ~0,2 m sobre el piso (puntos a 2,55–2,62).

## Aberturas (todas = marco exterior; x en pared frontal/trasera, y en paredes laterales)

| elemento | pared | rango horizontal | z | notas |
|---|---|---|---|---|
| Puerta de entrada | frente y=0 | x −0,235…0,615 (hoja negra −0,22…0,60) | 0…2,05 | algo a la derecha (+x) del centro, como en f0001 |
| Ventana frente (cocina) | frente | x −0,92…−0,32 | 1,20…2,17 | borde inferior menos preciso (±5 cm) |
| Ventana sobre la bacha | izq x=XL | y 1,51…2,21 | 1,14…2,14 | **única** ventana del lado cocina; enfrente de la ventana +x |
| Ventana sobre mueble negro (delante del pie de la escalera) | der x=XR | y 1,50…2,21 | 1,13…2,18 | f0091/f0092/f0180/f0191 |
| Ventana baño der | der x=XR | y 5,25…5,70 | 1,20…2,12 | borde trasero medido (f0144); ancho 0,45 según agente de baño |
| Ventana baño izq (sobre inodoro) | izq x=XL | y 4,10…4,57 | 1,21…2,00 | borde trasero y≈4,57 y alféizar 1,21 medidos en f0137; delantero tapado por la jamba |
| Ventanas altillo (2) | fondo y=L | x −0,97…−0,40 y 0,30…0,89 | 2,42…2,98 | f0207/f0209/f0213, consistentes ±1 cm |
| Hueco baño (entre jambas) | tabique | x −0,37…0,27 | 0…2,10 | f0016/f0131/f0171; la hoja granero es más ancha y cuelga del lado living |

## Muebles (aprox., para las zonas)

- Mesada: altura **0,88–0,90**; va desde casi la pared frontal (hueco escoba) hasta y ≈ 2,2 (más allá de la ventana de la bacha).
- Heladera: entre y ≈ 2,2 y 2,8 (cara frontal en x ≈ −0,36 ± 0,05); **queda ~1,0 m** entre la heladera y la cara del
  tabique (3,86), donde cuelgan mesa plegable y sillas (f0111–f0122). Con L/BATH_Y nuevos el hueco ya no es 1,4 m.
- Sillón: lado +x bajo la escalera, asiento ≈0,45–0,60 (cluster de puntos); y ≈2,3–3,8.
- Escalera escondida: sobre la pared +x desde y ≈2,2 (detrás de la ventana) hasta el altillo (y ≈3,9, z 2,40).
- Baño: plato de ducha en esquina −x/fondo, vanitorio + espejo sobre pared +x, estante de madera en la pared del fondo,
  inodoro del lado −x cerca del tabique. No medí cotas finas de ducha/vanitorio/inodoro (ver láminas bano1–4).
- No medí: mueble negro (cubos), dimensiones del sillón, ducha, vanitorio e inodoro en detalle.

## Dudoso / pendiente

- Exterior sin cámaras (f0001–f0010 no registran); el agente de exterior debe ajustar a mano. Ojo: `BELT_Z = EAVE`
  en exterior.py ahora queda a 3,12 m; en la foto la junta horizontal está a ≈2,25 m sobre el umbral.
- `puerta_luces.py` cuelga la araña de `RIDGE` (= 3,12, cielorraso): ahora queda bien al ras.
- `cocina.py` toma `RW_BIG` como la 2ª ventana derecha = ahora la del baño; revisar lo que ancle a ella.
- Escala ±3 %; ventana del baño y borde inferior de la ventana del frente, ±5 cm.
