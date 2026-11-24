# Guía para agentes: Mini Casa fiel al video

Objetivo: que el modelo Blender sea **lo más parecido posible al video** `/opt/3d/minicasa/video.mp4`
(54 s, 720×1280 vertical; tour de una tiny house). El usuario dijo que la versión actual "no se parece".
Prioridad: proporciones y ubicación correctas > forma de cada mueble > colores/texturas > detalles chicos.
Ignorar al presentador (persona) y el desorden.

## Archivos y quién toca qué
- `scripts/core.py` — helpers (box, multi, cyl, sphere, prism, wall_with_openings, interactive…), materiales `M[...]`
  y constantes (W, L, T, EAVE, RIDGE, GROUND, BATH_Y, LOFT_Z, XL, XR). **Solo el agente de Medidas cambia las
  constantes.** Cualquiera puede *agregar* materiales nuevos con `mat("Nombre", color, tex=...)` dentro de su zona.
- `scripts/zones/<zona>.py` — cada zona es dueña de su archivo. Se ejecutan en este orden en un espacio de nombres
  compartido: exterior, estructura, cocina, living, escalera, bano, altillo, puerta_luces. Una zona puede leer
  constantes definidas por zonas anteriores (p. ej. `FRONT_DOOR`, `BATH_DOOR`, `TY`), no las borres ni renombres.
- `scripts/build.py --out DIR` — construye todo y exporta `DIR/minicasa.blend` + `DIR/minicasa.glb`.
  **Usá siempre tu propia carpeta `--out`** (p. ej. `/opt/3d/minicasa/work/<zona>`), nunca `out/` (la usa el integrador).
  `--no-glb` para iterar más rápido.
- `scripts/audit.py --blend DIR/minicasa.blend --cams audit/cameras.json --out DIR/audit [--only nombre1,nombre2]`
  — renderiza desde las cámaras del video y arma láminas `[fotograma | render | bordes del render sobre la foto]`.
  Mirá las láminas con Read. Iterá hasta que coincidan.
- Texturas: `tex/` (generadas por `scripts/textures.py`). Podés **recortar texturas reales de los fotogramas**
  (mural de triángulos, láminas/cuadros, alfombras, mármol, multilaminado) con PIL y guardarlas en `tex/` con el
  prefijo de tu zona (p. ej. `tex/cocina_salpicadero.jpg`). Para rectificar un cuadrilátero en perspectiva usá
  una homografía (ver `/opt/3d/openhouse/archviz/phototex.py` como referencia, licencia MIT).

## Convenciones (no cambiar)
- Metros, Z arriba. Frente de la casa (puerta de entrada) en y=0, fondo en y=L. Interior x ∈ [XL, XR].
  Mirando desde la puerta hacia el fondo: cocina/mesada a la **izquierda (−x)**, mueble negro y sillón a la
  **derecha (+x)**. Piso interior z=0.
- Objetos interactivos: el **origen del objeto es la bisagra/pivote** y se marcan con `interactive(ob, tipo, etiqueta,
  group=..., axis="X|Y|Z", angle=grados, vec=(dx,dy,dz))` en coordenadas Blender (la función convierte a three.js).
  Tipos: `rot`, `slide`, `vis` (+ `extra={"vis_state": "open"|"closed"}`), `water` (+ objetos con `["water_of"]=grupo`),
  `light`, `loft`. **Mantené todos los interactivos existentes** (nombres y grupos), podés mejorar su forma/posición.
  Lista actual: Puerta entrada, Puerta mosquitero, Cajon 1-3, Canilla cocina (agua_cocina), Heladera puerta, Freezer,
  Mesa plegable + Silla plegada/abierta 1-2 + Mensula mesa (grupo "mesa"), Escalon oculto 1-6 (grupo "escalera"),
  Subir al altillo (loft), Puerta granero, Inodoro tapa, Mampara ducha, Grifo ducha (agua_ducha), Canilla baño
  (agua_bano), Llave de luz. Empties: luz_*, spawn, loft_spot, down_spot.
- El visor web es three.js sin sombras: modelá con cajas/cilindros/prismas (low-poly está bien, ~50k triángulos total
  máximo por zona). Nada de modificadores sin aplicar.

## Recursos de referencia
- Fotogramas a 4 fps, resolución completa: `/opt/3d/minicasa/colmap/images/f0001.jpg … f0217.jpg`
  (frame N ≈ segundo (N−1)/4). Tramos aproximados:
  exterior f0001–f0010 · entrada/pasillo f0010–f0022 · cocina f0022–f0090 · heladera f0088–f0100 ·
  sillón/sillas/mesa/puerta granero f0100–f0125 · baño f0125–f0165 · escalera escondida y altillo f0165–f0217.
- Cámaras resueltas (si existen): `audit/cameras.json` y `audit/medidas.md` (las escribe el agente de Medidas).
- Toolkit de referencia: `/opt/3d/openhouse` (docs/workflow.md, docs/realism.md, tools/overlay.py).
- Python: `/opt/3d/venv/bin/python` (bpy 5.3, numpy, PIL, trimesh, scipy).

## Entrega de cada agente
1. Tu archivo de zona mejorado (y texturas nuevas en `tex/`).
2. `audit/<zona>.md`: qué cambiaste, medidas usadas, qué sigue sin coincidir y por qué.
3. 2–4 láminas de auditoría finales en `audit/<zona>/`.
No hagas commits de git; el integrador junta todo.
