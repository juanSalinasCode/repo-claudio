# Living + escalera: auditoría

Archivos: `scripts/zones/living.py`, `scripts/zones/escalera.py`, texturas `tex/living_almohadon.jpg` (almohadón con elefante rectificado de f0106) y `tex/living_logo.jpg` (logo "Classic" rectificado de f0100).
Build: `/opt/3d/minicasa/work/living` (blend y glb). Láminas: `audit/living/`.

## Qué cambió
- **Heladera retro** (f0094–f0100): carcasa con cantos superiores redondeados, puerta superior con canto curvo, burletes, manijas cromadas horizontales del lado de la mesada, barra cromada y logo, zócalo negro y un papelito en el lateral. Color muestreado: sRGB (168,207,204), lineal (0.40,0.62,0.60). Va **pegada al final de la mesada** (`FY0 = KY1 + 0.02`). La auditoría con las cámaras heladera1 y heladera2 lo confirmó; en el primer ciclo estaba anclada al tabique y quedaba demasiado lejos.
- **Freezer**: en el video es una **puerta inferior abisagrada** (misma bisagra del lado del tabique, con cajones transparentes adentro), no un cajón. Pasó de `slide` a `rot` (Z, 100°). Se conservan el nombre y el grupo.
- **Mesa y sillas** (f0112–f0124): las sillas bistro de listones (acacia, sRGB ≈ (95,62,40)) se guardan plegadas y de pie, y la mesa plegada queda contra el tabique, en el hueco entre la heladera y el tabique. Al abrir, `Mesa plegable` (ahora `combo`: gira 90° en X y se traslada) queda armada en el pasillo frente al sillón. `Mensula mesa` son las patas en X, y las `Silla abierta 1-2` aparecen a cada lado.
- **Sillón** tipo loveseat turquesa, sRGB (40,74,87): mide 1.50 × 0.78, con rollos curvos en el respaldo y los apoyabrazos, patas cónicas de madera abiertas, 1 almohadón blanco y 2 con la textura real del elefante, y una manta de piel en el extremo del fondo.
- **Split**: pared izquierda, arriba, encima de la mesada y la heladera (`EAVE - 0.06`), con frente redondeado y rejilla.
- **Tablero eléctrico**: está en el mural, a la izquierda de la puerta granero (`BATH_DOOR[0] - 0.33 … -0.10`), con display azul.
- **Escalera escondida** (f0103–f0109 plegada, f0180–f0203 desplegada): un panel de pino en diagonal sobre el sillón, con **8 pedadas** que cuelgan hacia abajo plegadas (los rectángulos en diente de sierra con una ranura oscura arriba). Cada `Escalon oculto i` gira +90° en Y alrededor de su bisagra en la pared y queda horizontal, con una profundidad de 0.40. Se agregó `Larguero escalera` (slide del grupo "escalera"): plegado queda bajo las pedadas y al desplegar sube y sale hasta ser la zanca exterior que apoya en el piso. Altura por escalón = `(LOFT_Z+0.08)/9`. El avance se calcula para que las 3 pedadas bajas queden delante del sillón (`SOY0`). `Subir al altillo` (loft, needs escalera) está sobre las dos últimas.

Todo es relativo a XL, XR, BATH_Y, LOFT_Z, EAVE, KY1 y BATH_DOOR. `TY` sigue definido.

## Qué sigue sin coincidir
1. **Ventana `RIGHT_WINS[1]` (y 3.05–3.95)**: en el modelo está sobre el sillón, pero en el video esa pared la ocupa la escalera. La ventana real está **delante** del pie de la escalera (f0180, f0192). Esto le toca a Medidas/estructura: correrla hacia el frente, aproximadamente a y ≈ 1.9–2.6.
2. Con las constantes actuales queda ~1.4 m entre la heladera y el tabique, y en el video son ~0.5 m. Una de dos: `BATH_Y` es grande o la cocina es corta. Las sillas están ancladas al tabique, así que se acomodan solas cuando corrijan las medidas.
3. En la cámara living2 el sillón del video se ve algo más grande y más cerca; puede que sea más profundo.
4. Plegadas, las pedadas más bajas quedan en parte bajo el piso. No se ve porque están detrás del sillón.
5. La escalera del video es algo más empinada; el avance queda limitado por la longitud del sillón.
6. En Workbench la heladera se ve más oscura que en el video por la iluminación; el color base es el muestreado.

Triángulos: Living ≈ 2.1k y Escalera ≈ 0.25k.
