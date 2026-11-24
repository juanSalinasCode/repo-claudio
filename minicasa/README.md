# Mini Casa 3D

Modelo de la mini casa del video "¡NO vas a creer lo que OCULTA esta mini CASA!", reconstruido en Blender y recorrible en el navegador.

- `scripts/textures.py` — genera las texturas (multilaminado, piso, mural de triángulos, mármol, revestimiento…).
- `scripts/build.py` — construye toda la casa con bpy (Blender 5.3) y exporta `out/minicasa.blend` y `out/minicasa.glb`.
- `scripts/render_views.py` — renders de control.
- `web/index.html` + `web/minicasa.json` — visor three.js: caminar, abrir puertas, cajones, heladera/freezer, canillas,
  ducha, mesa y sillas plegables, escalera escondida y subir al altillo.

Regenerar: `python scripts/textures.py tex && /opt/3d/venv/bin/python scripts/build.py`
(después convertir el .glb a `web/minicasa.json`, ver el commit).

Medidas supuestas (no hay medidas reales): interior 2,40 × 6,00 m, paredes 2,45 m, cumbrera 3,60 m,
baño de 1,60 m de fondo con altillo a 2,10 m. Exterior lateral/trasero inventado (no se ve en el video).
