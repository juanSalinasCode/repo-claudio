# Cocina — auditoría

Archivo: `scripts/zones/cocina.py`. Build: `/opt/3d/minicasa/work/cocina` (OK, 296 objetos, 30 interactivos; la zona tiene unos 3,2k triángulos).
Láminas finales en `audit/cocina/` (`cocina2`, `cocina4`, `entrada3`, `heladera2`). Hice 3 ciclos: uno con cámaras estimadas a ojo y dos con `audit/cameras.json`.

## Qué cambié
- **Bajo mesada como en el video** (f0026/f0034/f0066/f0080). Desde el frente: cajonera de 3 (`Cajon 1-3`, interactivos slide; uno chico arriba y dos hondos), puerta(s) intermedias, puerta doble bajo la bacha y cajonera trasera de 3 cajones iguales. Los frentes de cerezo van sobre un casco oscuro que se ve en las juntas, con tiradores de arco de níquel (horizontales en los cajones y verticales en las puertas) y zócalo retirado.
- **Mesada maciza de maple claro** de 4 cm con vuelo. Bacha bajo mesada, escurridor enrollable de 18 varillas a lo ancho, repasador rojo, jabones y taco de cuchillos al fondo.
- **Canilla negra tipo cuello de ganso** junto al marco delantero de la ventana. Sigue siendo el interactivo `water` del grupo `agua_cocina`, y el agua cae dentro de la bacha.
- Horno eléctrico negro con vidrio, perillas y manija. 2 estantes flotantes más una repisa baja en el rincón del frente, con bowls turquesa, taza de cobre, platos y bowls negros, vasos de vidrio, tazas blancas y una rejilla blanca.
- **Pared derecha.** Mueble de cubos de 2×3 en melamina negra, con canastos de tela, manta azul, caja roja y tapa menta. Encima, anafe doble atrás y cafetera turquesa adelante con su taza. También van el riel blanco con 3 vasitos menta, el termostato, el mandala hexagonal calado (geometría), la repisa de la ventana angosta con florero y el cartel "LIFE" en el alféizar de la ventana grande. Agregué el estante alto de multilaminado sobre la entrada. **Saqué el "espejo"**: en el video es la ventana grande.
- **Pared del frente:** lámina botánica con paspartú verde sobre la puerta, y alfombra persa en la entrada. Saqué la "alfombra cocina", que no existe en el video.
- Letrero de letras negro sobre la heladera (va en `Pizarra menu`).

## Medidas y anclajes
Todo depende de las constantes. La bacha está en `SINK_Y = ventana más grande de LEFT_WINS[0] + 0.32`; la mesada empieza en `KY0 = 0.33` (hueco de escoba, f0034) y termina en `KY1 = SINK_Y + 0.95`; la profundidad es 0.60 y la altura 0.91. El mueble de cubos empieza 5 cm antes de que termine la ventana angosta de `RIGHT_WINS`. La lámina queda centrada sobre `FRONT_DOOR`. Living ya usa `KY1` para pegar la heladera a la mesada.

## Colores (medianas de píxeles en sRGB, pasados a lineal)
| Elemento | sRGB (0–255) | Fotograma |
|---|---|---|
| Frente cerezo | 140,66,28 | f0034, f0066 |
| Mesada maple | 228,204,164 | f0034, f0066 |
| Bowls turquesa | 106,176,191 | f0054 |
| Cafetera | 79,190,187 | f0040 |
| Platos negros | 40,40,52 | f0054 |
| Melamina negra del cubo | 29,29,34 | f0040 |
| Vasitos menta | 167,191,189 | f0040 |
| Heladera menta | ~167,213,211 (lateral) / 153,173,169 (frente en sombra) | f0094, f0100 |

## Texturas nuevas en `tex/`
- `cocina_alfombra.jpg`: rectificada con homografía desde f0054 y espejada, porque la pierna tapa la mitad derecha.
- `cocina_lamina.jpg`: desde f0054.
- `cocina_life.jpg`: desde f0090.
- `cocina_letrero.jpg`: desde f0094.
- `cocina_mueble.jpg` y `cocina_mesada.jpg`: veta procedural tileable con los colores muestreados. El recorte directo de la puerta era casi un color liso con reflejos y dejaba costuras.

## Qué sigue sin coincidir
- **Ventanas.** Cuando hice la auditoría, `LEFT_WINS`/`RIGHT_WINS` todavía eran los valores viejos.
  - La bacha y la canilla coinciden en posición *relativa* a la ventana grande, pero esa ventana todavía está ~0,5 m más al frente de lo que muestran las cámaras `cocina2`/`cocina4`.
  - En `entrada3` el mueble de cubos y la ventana grande derecha aparecen junto a la cámara (y≈0,6–1,3). En el modelo quedan más atrás porque la ventana angosta está en 1,15–1,45.
  - Cuando Medidas actualice las ventanas, la cocina las sigue sola.
- `LEFT_WINS[0]` (0,25–0,75), en la pared izquierda, no existe en el video: ahí están los estantes, sobre multilaminado liso. Lo que se ve a la izquierda de los estantes es `FRONT_WIN`. Se lo dejo a Medidas y Estructura.
- Los frentes salen más oscuros que en la foto en Workbench, porque la iluminación de la foto es más cálida y brillante.
- La vajilla es simplificada: bowls cónicos y pilas de platos como cilindros.
