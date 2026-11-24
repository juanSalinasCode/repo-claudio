# Exterior: 2ª ronda (choques y proporción)

Build: `/opt/3d/minicasa/work/exterior2` · choques: `/opt/3d/minicasa/work/exterior2/colisiones.md`.
Láminas: `audit/exterior/r2_ext_f0001.jpg`, `audit/exterior/r2_ext_f0004.jpg` (cámaras estimadas `cams_ext.json`).
Exterior: 61 objetos, **39 752 triángulos** (antes ~45 000).

## Causa de los choques "grandes"
`collisions.py` mide la penetración con la caja AABB de cada objeto. El revestimiento, la tapajunta, los esquineros,
el zócalo, la cenefa, el borde de durmientes, los arbustos y las rocas eran **un solo objeto cada uno**, armado como
anillo o como nube de piezas. Su AABB envolvía toda la casa, así que el tocar una pared se informaba como 20 cm y
la prueba de "contenido" ubicaba los arbustos o las rocas dentro del freezer, el sillón y otros muebles.
Ahora cada pieza es un objeto propio (`Revestimiento superior 0..4`, `Tapajunta 0..4`, `Esquineros 0..5`,
`Zocalo 0..3`, `Cenefa 0..3`, `Borde durmientes 0..3`, `Roca 0..4`, `Arbusto 0..6`).

## Cambios
- **Revestimiento, tapajunta y esquineros**: van pegados por fuera de las caras exteriores, en XL−T, XR+T, y=−T e
  y=L+T. La tapajunta va debajo del revestimiento (BELT_Z−0.03…BELT_Z), sin solaparse con él. Los esquineros son
  postes de 2.5 cm en las esquinas. Dejé una muesca detrás del `Farol 0` (x 0.80–0.97) para que no se crucen.
- **Zócalo**: pasó de un bloque macizo bajo la casa a un faldón perimetral de 4 cm. Ya no choca con lo que cuelga
  bajo el piso.
- **Techo**: la losa apoya 3 mm sobre `TOP = EAVE+0.22`, el remate de hastiales y cenefas de estructura, y tiene
  2.5 cm de espesor como mínimo. ROOF_TOP = 3.383 y la caída hacia el fondo es de 1.5 cm. La cenefa exterior queda
  por fuera del revestimiento.
- **Ripio**: el margen bajó de 0.45 a 0.30 m. El galpón, el poste y el medidor quedan fuera del borde de durmientes,
  y el soporte de las condensadoras ya estaba fuera. Los esquineros del galpón ya no se meten en él.
- **Vegetación y rocas**: un chequeo `_free()` corta el build si una pieza invade la casa + 0.3 m, el deck, los
  escalones, la cama de ripio, el galpón, el poste, las condensadoras o la parrilla. Separé Roca 1 y Roca 2.

## Proporción (f0001/f0004)
La fachada mide 2.40 m de ancho sin alero y 2.66 m con alero. La altura del deck al borde de la cenefa es 3.42 m.
Eso da 1.43 sin alero y 1.29 con alero. Medí la foto en píxeles y da 1.29 con alero. Contra la puerta: altura de la
casa / alto de la puerta = 1.56 en la foto y 1.56 en el render; ancho / ancho de la puerta = 2.8 en la foto y 2.9
en el render. **La proporción coincide.** La cámara estimada sigue algo alta y por eso el render se ve más chato;
las razones de arriba no dependen de eso.

## Pendiente (otros agentes)
- **Baño**: `Riel granero` y `Soporte riel 0` llegan a x = −1.21. Atraviesan la pared izquierda y asoman 1 cm por
  fuera, contra `Revestimiento superior 3` y `Tapajunta 3`. Con `x ≥ XL` alcanza.
- **Estructura**: si se quiere la fachada exactamente en 1.37 sin alero, hay que bajar `TOP` a ≈ EAVE+0.10.
