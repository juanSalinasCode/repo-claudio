# Zona exterior + puerta/luces

Archivos: `scripts/zones/exterior.py`, `scripts/zones/puerta_luces.py`. Las texturas nuevas son `tex/exterior_*.jpg`; las genera `/opt/3d/minicasa/work/exterior/make_tex.py` a partir de recortes de los fotogramas.
Láminas finales en `audit/exterior/`: `ext_f0001`, `ext_f0004`, `entrada2` (f0013) y `entrada3` (f0014).
Build de trabajo: `/opt/3d/minicasa/work/exterior/minicasa.{blend,glb}`. Triángulos: exterior ≈ 41 k, puerta/luces ≈ 1.7 k.

## Qué se ve en el video y cómo quedó
- **Fachada.** Es un prisma recto de techo casi plano. **No hay hastial triangular visible**: el borde superior es horizontal y lo remata una cenefa negra de unos 0.24 m con alero de 0.12–0.16 m. Lo modelé como `Techo` (losa siempre por encima de `max(EAVE, RIDGE) + 0.05`) más `Cenefa` perimetral, con `ROOF_TOP = max(RIDGE, EAVE) + 0.25`.
- **Revestimiento.** Es board-and-batten vertical gris carbón, con listones cada ~0.24 m. La textura `exterior_siding.jpg` es un recorte de f0005 y reemplaza la imagen de `M["siding"]`. A ~0.22 m sobre el contramarco de la puerta hay una **junta horizontal** (`BELT_Z = ROOF_TOP − 1.05`). La modelé como revestimiento superior que sobresale 2 cm más una tapajunta negra, en el frente y en los laterales. En el fondo no hay revestimiento superior, para no tapar las ventanas del altillo.
- **Puerta de entrada.** Es amarilla por fuera (#c19e18 en sombra) y negra tipo pizarrón por dentro. La **bisagra está a la izquierda** vista desde afuera (x = d0) y la puerta abre hacia adentro (f0007, f0010 y f0012). Antes el modelo la tenía a la derecha. El interactivo `Puerta entrada` tiene el pivote en d0 y `angle = +95`.
- **Puerta mosquitero.** Es blanca, con bisagra a la izquierda, y abre hacia afuera (`angle = −105`). Tiene vidrio superior, travesaño, vidrio inferior y zócalo ciego, en proporciones medidas en f0004.
- **Luces de la fachada.** Encima de la puerta, sobre la junta, hay una luz solar con sensor (`Farol 1`). A la derecha de la puerta hay un farol caja negro con vidrio esmerilado encendido (`Farol 0`).
- **Felpudo.** Es de coco, de 0.80 × 0.54 m, con la textura recortada de f0010.
- **Deck y escalones.** El deck es gris envejecido, del ancho de la casa y de 1.20 m de profundidad. Le siguen 2 escalones de 0.27 m de huella, con 3 contrahuellas iguales hasta el terreno. Todo está sobre una cama de ripio con borde de durmientes que llega a ~2 m delante de la fachada y sobresale 0.45 m a los lados. Hay además una senda de losetas a la derecha.
- **Entorno visible.** A la izquierda, una plancha/parrilla negra con carro y, detrás, 2 condensadoras grises sobre un soporte blanco. A la derecha, un poste de servicio con medidor, un galpón de madera clara con esquineros blancos, una roca grande en primer plano y rocas al fondo a la derecha.
- **Bosque.** Son 88 árboles con troncos altos y finos (13–24 m, radio de 0.09 a 0.28 m) y copas altas hechas de 4–6 manchas irregulares. Las texturas de follaje y pasto salen de f0001. Todo está en 2 mallas (`Bosque troncos` y `Bosque copas`) para que el visor web siga siendo liviano. El claro delante de la casa queda libre.
- **Araña** (f0013–f0016). Tiene florón, cable, columna central y 6 brazos que salen de abajo, van casi horizontales (r = 0.27 m) y suben a portavelas con lamparita globo. Las cámaras `entrada2` y `entrada3` la ubican en **x ≈ 0, y ≈ 2.9**, con los brazos a 2.22 m. Antes estaba en y = 2.3. Si `estructura` define `CEIL_Z`, el cable lo usa; si no, toma `RIDGE`.
- **Spots.** Son un riel con 3 spots negros sobre la ventana más ancha de `LEFT_WINS` (f0022).
- **Llave de luz.** Está del lado del picaporte (d1).
- **Interactivos y empties.** Conservan sus nombres. `luz_arana`, `luz_cocina` y `luz_frente` siguen ahora a la araña, al riel y al farol; `spawn` sigue al eje de la puerta.

## Inferido (no se ve en el video)
Laterales y fondo exteriores, caída del techo hacia el fondo (0.04 m), arbustos, la mayor parte del bosque y la parte trasera del galpón.

## Ciclos de auditoría
1. Con una cámara estimada a ojo para f0001: corregí la parrilla, las condensadoras, el galpón, la profundidad del deck y escalones y la densidad de las copas.
2. Con `cameras.json` (HFOV de 62°): recalculé la profundidad del deck, los escalones y el ripio. Moví la araña a y = 2.9 y ahora coincide con los bordes en `entrada2` y `entrada3`.
3. Con las medidas nuevas de Medidas (cielorraso plano en EAVE = 3.12): la losa del techo atravesaba el cielorraso. Ahora queda por encima, y la junta horizontal se ancló a `ROOF_TOP`.

No hay cámaras exteriores en `cameras.json`. Para f0001/f0004 usé una cámara estimada por fugas (`work/exterior/cams_ext.json`), así que esas láminas son orientativas. `entrada1` (f0012) no sirve con la puerta cerrada.

## Para el agente de Medidas (estructura.py)
- **Proporción de la fachada en f0001/f0004.** El alto, del deck al borde superior de la cenefa, es ≈ 1.37 × el ancho exterior. El contramarco de la puerta, de unos 0.99 m, ocupa 0.38 del ancho. Con una puerta de 0.82–0.85 m, el ancho exterior da **≈ 2.5–2.6 m**, y el modelo actual (W = 2.00 + 2T) tiene 2.24 m. Ahora la fachada sale demasiado alta y angosta (1.64 en vez de 1.37). ¿W ≈ 2.25 o paredes más gruesas?
- **Posiciones de puerta y ventana.** Medidas como fracción del ancho exterior, coinciden con `FRONT_DOOR`/`FRONT_WIN` actuales (puerta 0.39–0.78, ventana 0.13–0.37). La parte superior de la ventana del frente está a la misma altura que la de la puerta.
- **`Hastial frontal`/`trasero`.** Ya son rectángulos y está bien. Por encima de EAVE los laterales los cierra mi revestimiento superior.
