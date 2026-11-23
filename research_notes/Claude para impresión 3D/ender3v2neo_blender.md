# Ender 3 V2 Neo (specs + perfiles de slicer) y Blender headless para preparar STL (nov. 2026)

> Nota de método: el entorno de investigación tenía red restringida. **docs.blender.org y lash-l.github.io no resolvieron** (hay que permitirlos en los ajustes de red de la sesión para citarlos directamente). Las fuentes web se obtuvieron por búsqueda; el perfil de Cura se descargó de GitHub (raw). Varias afirmaciones de Blender se **verificaron ejecutando Blender 4.0.2 en modo `-b` en este mismo contenedor** (`/usr/bin/blender`, Ubuntu); se citan como "verificado localmente".

## A1. Especificaciones de la Ender 3 V2 Neo

### Takeaway
220 × 220 × 250 mm, boquilla 0,4 mm, extrusor Bowden todo-metal, CR Touch (malla de 16 puntos = 4×4), cama magnética PC sobre acero, boquilla máx. 260 °C (algunas fuentes dicen 250 °C), cama máx. 100 °C, velocidad máx. ≤120 mm/s (típica 50 mm/s).

### Cited Findings
- Volumen de impresión 220 × 220 × 250 mm; boquilla 0,4 mm; FDM de un extrusor; Bowden y cama PC de acero magnética — [Farnell datasheet](https://www.farnell.com/datasheets/3990939.pdf); [B&H](https://www.bhphotovideo.com/c/product/1732071-REG/creality_ender_3_v2_neo_3d.html); [All3DP specs](https://all3dp.com/1/creality-ender-3-v2-neo-review-3d-printer-specs/)
- Temperatura máx. de boquilla 260 °C — [Farnell datasheet](https://www.farnell.com/datasheets/3990939.pdf); [MatterHackers](https://www.matterhackers.com/store/l/creality3d-ender-3-v2-neo-3d-printer-kit/sk/M212JC95); contradicho por [Clever Creations](https://clevercreations.org/creality-ender-3-v2-neo-review-specs/) (250 °C) y por reseñas citadas en [AppleInsider](https://appleinsider.com/articles/23/01/11/ender-3-v2-neo-review-3d-printing-with-the-beginner-in-mind) (250 °C).
- Cama caliente máx. 100 °C — [Farnell datasheet](https://www.farnell.com/datasheets/3990939.pdf)
- Extrusor Bowden todo-metal; CR Touch de serie con comprobación de 16 puntos — [3DSourced](https://www.3dsourced.com/3d-printers/ender-3-neo-vs-v2-neo-max/); [Geekbuying](https://www.geekbuying.com/item/Creality-Ender-3-V2-Neo-3D-Printer-518343.html)
- Velocidad de impresión ≤120 mm/s (máximo, no típico); 3DSourced probó de 40 a 120 mm/s — [Geekbuying](https://www.geekbuying.com/item/Creality-Ender-3-V2-Neo-3D-Printer-518343.html); [3DSourced](https://www.3dsourced.com/3d-printers/ender-3-neo-vs-v2-neo-max/)
- El firmware de serie puede sustituirse; se citan como alternativas populares Marlin, Klipper, Jyers, TH3D — [Creality3DOfficial](https://www.creality3dofficial.com/products/ender-3v2-neo-3d-printer). Firmware comunitario activo: mriscoc "Ender3V2S1" (Marlin profesional) con variantes para la Neo — [mriscoc/Ender3V2S1 discussion #413](https://github.com/mriscoc/Ender3V2S1/discussions/413); [guías de calibración](https://github.com/mriscoc/Ender3V2S1/wiki/Calibration-Guides)
- Manual de usuario oficial (PDF) con menú "Prepare > Preheat PLA" — [Manual (manuals.plus)](https://manuals.plus/m/d743561ebcdbac7b194e36400f8cabf58f2a2621e4a01985c396ffb79972dec0); [PDF en Amazon](https://m.media-amazon.com/images/I/B19LW6u-ldL.pdf)

### Inferences
- Para un agente: usar 220×220 como área segura (no 230×230 del perfil de Cura, ver A3) y altura útil ~245 mm para margen. Tratar 250 °C como límite práctico (PTFE del Bowden: por encima de ~240 °C el tubo PTFE se degrada; esto es conocimiento general, no verificado con fuente aquí).
- El firmware de serie es Marlin modificado por Creality (pantalla DWIN 4,3"); no se encontró número de versión oficial.

### Gaps
- No se encontró la página de specs en creality.com ni el número de versión del firmware de serie (búsquedas no devolvieron creality.com). No se pudo leer la tabla de materiales del manual.

## A2. Start/End G-code y malla CR Touch (¿G29 o M420 S1?)

### Takeaway
Con firmware de serie, lo que la comunidad reporta que funciona es `G28` + `G29` (sondeo en cada impresión, ~1–2 min); `M420 S1` solo recarga una malla guardada y en el firmware Creality 1.70 se reporta con fallo. El perfil de Cura oficial **no incluye ni G29 ni M420** — hay que añadirlo.

### Cited Findings
- G29 sondea y crea malla nueva; `M420 S1 Z0` restaura la malla guardada (sin fade) — [Creality forum, tag ender-3-v2-neo](https://forum.creality.com/tag/ender-3-v2-neo) / resumen en búsqueda; ver también [Ultimaker community, G29 not working](https://community.ultimaker.com/topic/43277-g29-bed-leveling-not-working/)
- Usuario con firmware de serie en V2 Neo: "G28 luego G29 funcionó; G29 reactiva el ABL automáticamente, no hace falta M420" — [Ultimaker community](https://community.ultimaker.com/topic/44724-i-feel-like-i-am-about-to-lose-my-mind-over-the-ender-3-v2/)
- "Si usas el firmware 1.70 de Creality, M420 está bugueado; hay que usar G29" — [Ultimaker community](https://community.ultimaker.com/topic/33907-47-is-now-auto-bed-leveling-on-every-print/)
- En el hilo del firmware mriscoc se debate si en la Neo es mejor G29 o M420 con malla guardada (sin respuesta definitiva) — [mriscoc discussion #413](https://github.com/mriscoc/Ender3V2S1/discussions/413)
- Start G-code bundled en Cura (`creality_ender3v2neo.def.json`), literal: `G92 E0 / G28 / G1 Z2.0 F3000 / G1 X10.1 Y20 Z0.28 F5000.0 / G1 X10.1 Y200.0 Z0.28 F1500.0 E15 / G1 X10.4 Y200.0 Z0.28 F5000.0 / G1 X10.4 Y20 Z0.28 F1500.0 E30 / G92 E0 / G1 Z2.0 F3000` — sin G29/M420 — [Cura GitHub](https://github.com/Ultimaker/Cura/blob/main/resources/definitions/creality_ender3v2neo.def.json)
- End G-code heredado de `creality_base`: `G91 / G1 E-2 F2700 / G1 E-2 Z0.2 F2400 / G1 X5 Y5 F3000 / G1 Z10 / G90 / G1 X0 Y{machine_depth} / M106 S0 / M104 S0 / M140 S0 / M84 X Y E` — [Cura creality_base.def.json](https://github.com/Ultimaker/Cura/blob/main/resources/definitions/creality_base.def.json)
- En OrcaSlicer hay que añadir explícitamente el comando de nivelado en el start G-code; usuarios reportan que el perfil Orca de la "Ender 3 NEO v2" debería esperar a la temperatura de cama antes de sondear y que puede requerir reajuste de Z-offset — [Creality forum: Auto mesh with Orca](https://forum.creality.com/t/auto-mesh-calibration-with-orca/45768); [r/OrcaSlicer (mirror)](https://pol1.lr.ggtyler.dev/r/OrcaSlicer/comments/1k1ikvv/auto_leveling_routine); [Duet forum](https://forum.duet3d.com/post/352010)
- Orca soporta malla adaptativa (limitada a min/max de la cama) — [OrcaSlicer wiki adaptive bed mesh](https://www.github.com/SoftFever/OrcaSlicer/wiki/adaptive-bed-mesh)

### Inferences
- Start G-code recomendado (sintetizado de lo anterior; Cura usa `{material_bed_temperature_layer_0}` y `{material_print_temperature_layer_0}`; en Orca/Prusa `[bed_temperature_initial_layer_single]`, `[nozzle_temperature_initial_layer]`):
  ```gcode
  M140 S{material_bed_temperature_layer_0}   ; cama
  M104 S150                                  ; boquilla tibia (no gotea al sondear)
  M190 S{material_bed_temperature_layer_0}   ; esperar cama (sondear con cama dilatada)
  G28                                        ; home (desactiva la malla)
  G29                                        ; malla 4x4 con CR Touch (o M420 S1 Z10 si hay malla guardada y firmware != 1.70)
  M109 S{material_print_temperature_layer_0} ; esperar boquilla
  G92 E0
  G1 Z2.0 F3000
  G1 X10.1 Y20 Z0.28 F5000.0
  G1 X10.1 Y200.0 Z0.28 F1500.0 E15
  G1 X10.4 Y200.0 Z0.28 F5000.0
  G1 X10.4 Y20 Z0.28 F1500.0 E30
  G92 E0
  G1 Z2.0 F3000
  ```
- End G-code: el de `creality_base` es adecuado; añadir `M84` al final si se quiere liberar también Z.
- Z-offset: ajustar en pantalla (Prepare > Z-offset / "Probe Z offset") con papel; guardar con `M500`. Valor típico negativo (≈ −1 a −2 mm en muchas unidades) — dato anecdótico, no verificado con fuente.

### Gaps
- No se pudo confirmar qué start G-code trae Creality Print para la V2 Neo, ni si el firmware de serie más reciente guarda la malla tras G29 de forma fiable (sin acceso a creality.com / wiki).

## A3. Perfiles PLA/PETG y perfiles bundled en slicers (con errores conocidos)

### Takeaway
Valores de perfil Cura bundled: retracción 4 mm @ 25 mm/s, 50 mm/s impresión, 20 mm/s primera capa, aceleración 500, jerk 8, skirt. Comunidad (Bowden): PLA ~200–210 °C / 60 °C, retracción 5 mm @ 45–60 mm/s; PETG ~230–240 °C / 70–80 °C, retracción 4–6 mm @ 25–40 mm/s, ventilador 30–50 %. Error conocido: Cura declara cama 230×230 (la física es 220×220).

### Cited Findings
- Cura `creality_ender3v2neo`: `machine_width`=230, `machine_depth`=230, `machine_height`=250, `gantry_height`=25, `retraction_amount`=4, `retraction_speed`=25, polígono cabezal X −26..32 / Y −32..34 — [Cura GitHub](https://github.com/Ultimaker/Cura/blob/main/resources/definitions/creality_ender3v2neo.def.json)
- Cura `creality_base` (heredado): `speed_print`=50, `speed_layer_0`=20, `speed_travel`=150 (si speed_print<60), `acceleration_print`=500, `jerk_print`=8, `adhesion_type`='skirt', `z_seam_type`='back', `retraction_min_travel`=1.5, `retraction_count_max`=100, `wall_thickness`=line_width×2, combing 'noskin' — [Cura creality_base.def.json](https://github.com/Ultimaker/Cura/blob/main/resources/definitions/creality_base.def.json)
- Guía Bowden Ender 3 V2/Pro: empezar en 5 mm y ajustar ±1 mm hasta eliminar stringing — [All3DP retraction](https://all3dp.com/2/ender-3-retraction-settings-all-you-need-to-know/); [Wevolver](https://www.wevolver.com/article/ender-3-retraction-settings)
- Una guía da para V2 Neo en Cura: PLA 5 mm @ 60 mm/s; ABS 5 mm @ 55 mm/s; PETG 4 mm @ 60 mm/s (fuente de calidad dudosa) — [Wevolver](https://www.wevolver.com/article/the-best-ender-3-retraction-settings)
- Perfil PLA Ender 3 (V2/Pro) de All3DP: 200 °C boquilla / 60 °C cama — [All3DP Cura profile](https://all3dp.com/2/ender-3-cura-settings-best-ender-3-cura-profile/)
- PETG en Ender 3: Creality recomienda cama 50–60 °C en su blog (valor bajo; la comunidad usa más); PETG retracción 4 mm @ 25 mm/s en un perfil Cura; subir travel en pasos de 10 mm/s desde ~90 mm/s contra stringing — [Creality blog PETG](https://www.creality.com/uk/blog/how-to-get-perfect-petg-prints-on-ender-3-correct-settings-first); [All3DP PETG Ender 3](https://all3dp.com/2/ender-3-petg-settings-profile/); [All3DP Cura PETG](https://all3dp.com/2/cura-petg-settings-profile/)
- Prueba de 3DWithUs con ajustes de la V2 Neo — [3DWithUs](https://3dwithus.com/creality-ender-3-v2-neo-review-3d-printer-testing-settings)
- Perfil Orca de la V2 Neo: no espera a la cama antes de sondear; Z-offset puede necesitar ajuste — [r/OrcaSlicer (mirror)](https://pol1.lr.ggtyler.dev/r/OrcaSlicer/comments/1k1ikvv/auto_leveling_routine)
- Un usuario reporta que añadir la E3V2 en Orca produce end G-code erróneo — [Google Groups](https://groups.google.com/g/3d-printing-tips--tricks/c/7Yc_cWmHm9U)
- Calibración (flow, e-steps, PID, retracción, temp tower) para Ender 3 V2/S1 — [mriscoc Calibration Guides](https://github.com/mriscoc/Ender3V2S1/wiki/Calibration-Guides)

### Inferences
- Tabla de partida recomendada para un agente (síntesis; calibrar con temp tower y torre de retracción):

  | Parámetro | PLA | PETG |
  |---|---|---|
  | Boquilla | 200–210 °C (1ª capa +5) | 230–240 °C (1ª capa 235–245) |
  | Cama | 60 °C | 70–80 °C (PETG pega fuerte al PEI/PC: usar pegamento de barra como desmoldeante) |
  | Retracción (Bowden) | 5 mm @ 45 mm/s (rango 4–6 @ 25–60) | 4–6 mm @ 30–40 mm/s, sin coasting excesivo |
  | Velocidad | 50–60 mm/s (perímetros ext. 25–30) | 40–50 mm/s |
  | 1ª capa | 0,24–0,28 mm @ 20 mm/s, ventilador 0 | igual, ventilador 0 |
  | Ventilador | 100 % desde capa 2–3 | 30–50 % |
  | Viaje | 150 mm/s | 150 mm/s, Z-hop 0,2–0,4 opcional |
  | Aceleración / jerk | 500 / 8 (Cura) | 500 / 8 |

- Corrección del perfil Cura: poner `machine_width`/`machine_depth` a 220 si se colocan piezas cerca del borde; la malla CR Touch no cubre los bordes (el sensor está desplazado del nozzle) — inferencia general.

### Gaps
- No se obtuvieron valores oficiales de Creality Print para la V2 Neo (temperaturas, retracción) ni del perfil bundled de PrusaSlicer; tampoco lista concreta de bugs del perfil de Creality Print. Teaching Tech no fue consultable.

## B1. Importar/exportar STL en Blender 4.x/5.x, unidades y transformaciones

### Takeaway
Usar `bpy.ops.wm.stl_import` (desde 4.0, C++) y `bpy.ops.wm.stl_export` (desde 4.1). En 4.0 (Ubuntu apt) **no existe `wm.stl_export`**: hay que usar `bpy.ops.export_mesh.stl` (add-on Python). El add-on Python pasó a "legacy" en 4.1 y está como extensión "STL format - Legacy" para 4.2+. Blender trabaja en metros por defecto pero STL no tiene unidades: con `global_scale=1` y `use_scene_unit=False`, 1 unidad de Blender = 1 mm en el slicer.

### Cited Findings
- En Blender 4.0.2 existen `wm.stl_import` (params: `filepath`, `global_scale`=1.0, `use_scene_unit`=False, `use_facet_normal`=False, `forward_axis`='Y', `up_axis`='Z', `use_mesh_validate`=False), `import_mesh.stl` y `export_mesh.stl` (`use_selection`=False, `global_scale`=1.0, `use_scene_unit`=False, `ascii`=False, `use_mesh_modifiers`=True, `batch_mode`='OFF', `axis_forward`='Y', `axis_up`='Z'); **`wm.stl_export` no existe en 4.0** — verificado localmente (Blender 4.0.2, `get_rna_type()`)
- Manual 4.0: el importador add-on está obsoleto y se sustituye por el importador integrado; para exportar en 4.0 hay que usar el add-on STL — [Manual 4.0 STL](https://docs.blender.org/manual/en/4.0/files/import_export/stl.html); [Manual 4.0 mesh_stl](https://docs.blender.org/manual/en/4.0/addons/import_export/mesh_stl.html)
- 4.1: nuevo exportador C++ 3–10× más rápido; se recomienda migrar a `bpy.ops.wm.stl_export` / `bpy.ops.wm.stl_import`; add-on Python marcado legacy — [Release notes 4.1 I/O](https://developer.blender.org/docs/release_notes/4.1/pipeline_assets_io/)
- 4.2 LTS: importadores OBJ/PLY/STL con "Validate Meshes" activado por defecto — [Release notes 4.2 I/O](https://developer.blender.org/docs/release_notes/4.2/pipeline_assets_io/)
- Add-on legacy disponible como extensión "STL format - Legacy" (4.2+) — [extensions.blender.org](https://extensions.blender.org/add-ons/stl-format-legacy/); tarea de eliminación — [blender-addons #104634](https://projects.blender.org/blender/blender-addons/issues/104634)
- Opciones del manual 4.2 (facet normals, validate mesh, scene units, forward/up, apply modifiers) — [Manual 4.2 STL](https://docs.blender.org/manual/en/4.2/files/import_export/stl.html)
- Escena por defecto: `unit_settings.system`='METRIC', `scale_length`=1.0, `length_unit`='METERS' — verificado localmente (4.0.2)

### Inferences
- Patrón portable:
  ```python
  import bpy
  def stl_import(p):
      bpy.ops.wm.stl_import(filepath=p)            # 4.0+
  def stl_export(p):
      if hasattr(bpy.ops.wm, "stl_export") and "stl_export" in dir(bpy.ops.wm):
          bpy.ops.wm.stl_export(filepath=p, export_selected_objects=True, apply_modifiers=True)  # 4.1+ (nombres a verificar con get_rna_type())
      else:
          bpy.ops.export_mesh.stl(filepath=p, use_selection=True, use_mesh_modifiers=True)      # 4.0
  ```
  (Los nombres de parámetros de `wm.stl_export` — `export_selected_objects`, `apply_modifiers`, `ascii_format`, `global_scale`, `use_scene_unit` — siguen el patrón del exportador OBJ C++; no se pudieron confirmar con docs.blender.org bloqueado. Comprobar con `bpy.ops.wm.stl_export.get_rna_type().properties.keys()`.)
- Unidades: para ver mm en la UI, `scene.unit_settings.scale_length=0.001` y `length_unit='MILLIMETERS'`; mantener `use_scene_unit=False` en import/export para que 1 BU = 1 mm.
- Aplicar transformaciones antes de exportar/medir: `bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)`.

### Gaps
- Firma exacta de `wm.stl_export` en 4.2/4.5/5.x no verificada (docs bloqueados; Blender local es 4.0.2). No confirmado si 5.x eliminó por completo `export_mesh.stl`.

## B2. 3D-Print Toolbox (bundled en 4.0–4.1, extensión en 4.2+)

### Takeaway
En 4.0 viene bundled como `object_print3d_utils` con 17 operadores `bpy.ops.mesh.print3d_*`. En 4.2+ es la extensión `print3d_toolbox` (extensions.blender.org, v1.1.x). Defaults críticos: `thickness_min`=0.001 (¡en unidades de escena; si 1 BU = 1 mm, ajustarlo a ~0.8–1.2!), `angle_overhang`=45°.

### Cited Findings
- Operadores disponibles en 4.0.2 tras `addon_enable(module='object_print3d_utils')`: `print3d_check_all`, `_check_solid`, `_check_intersect`, `_check_degenerate`, `_check_distort`, `_check_thick`, `_check_sharp`, `_check_overhang`, `_clean_non_manifold`, `_clean_distorted`, `_info_volume`, `_info_area`, `_scale_to_volume`, `_scale_to_bounds`, `_align_to_xy`, `_export`, `_select_report` — verificado localmente
- Defaults `scene.print_3d` en 4.0.2: `thickness_min`=0.001, `angle_overhang`=0.785 rad (45°), `angle_sharp`=2.79 rad (160°), `angle_distort`=45°, `threshold_zero`=0.0001, `use_apply_scale`=False, `export_format`='STL' — verificado localmente
- Manual 4.1: checks de no-manifold, geometría degenerada, etc.; ubicación en la barra lateral del Viewport — [Manual 4.1 3D Print Toolbox](https://docs.blender.org/manual/en/4.1/addons/mesh/3d_print_toolbox.html)
- Extensión en 4.2+: [extensions.blender.org/add-ons/print3d-toolbox](https://extensions.blender.org/add-ons/print3d-toolbox); código GPL-3 — [projects.blender.org/extensions/print3d_toolbox](https://projects.blender.org/extensions/print3d_toolbox); versiones 1.1.1 → 1.1.4 en reseñas — [reviews](https://extensions.blender.org/add-ons/print3d-toolbox/reviews/?score=5)
- Problema reportado al activarlo en 4.2.2 (issue #9, cerrado sin respuesta) — [issue #9](https://projects.blender.org/extensions/print3d_toolbox/issues/9)
- Desde 4.2 los add-ons bundled pasan a la plataforma de extensiones — [devtalk: Changes to Add-on bundling 4.2](https://devtalk.blender.org/t/changes-to-add-on-and-themes-bundling-4-2-onwards/34593)

### Inferences
- En 4.2+ headless, instalar la extensión: `blender -b --command extension install-file -r user_default print3d_toolbox-<ver>.zip` o `blender --command extension sync && blender --command extension install print3d_toolbox` y habilitar como módulo `bl_ext.<repo>.print3d_toolbox` (sintaxis basada en conocimiento previo, no verificada aquí). Los nombres de operadores pueden haber cambiado en la extensión; mejor implementar los checks críticos en bmesh/trimesh (ver B3), que no dependen del add-on.
- `print3d_check_all` devolvió `{'FINISHED'}` en un cubo con agujero booleano; los resultados se leen en el informe del add-on (no hay valor de retorno estructurado) — verificado localmente; para agentes conviene calcular las métricas directamente.

### Gaps
- Lista exacta de operadores y nombre de módulo de la extensión en 4.2/4.5/5.x no verificados (docs bloqueados).

## B3. Modificaciones por script (escala, booleanos, solidify, split, chamfer, merge, normales, decimate, Z=0/centrado)

### Takeaway
Todo se hace con modificadores + `modifier_apply` o con `bmesh.ops`, sin UI. Se verificó un pipeline completo en Blender 4.0.2 headless: cubo 20 mm − agujero Ø6 (Boolean EXACT) + chaflán 1 mm (Bevel) + merge 0,001 + recalc normals → 0 aristas no-manifold, volumen 7302,55 mm³, apoyado en Z=0 y centrado.

### Cited Findings
- Pipeline verificado localmente (Blender 4.0.2, `blender -b --factory-startup --python pipe.py`): `modifiers.new(type='BOOLEAN')` con `operation='DIFFERENCE'`, `solver='EXACT'`; `modifiers.new(type='BEVEL')` con `width=1.0, segments=1, limit_method='ANGLE'`; `bmesh.ops.remove_doubles(dist=0.001)`; `bmesh.ops.recalc_face_normals`; conteo `not e.is_manifold`=0; `bm.calc_volume(signed=True)`=7302,55; `export_mesh.stl(use_selection=True)` generó STL binario de 15 284 bytes — verificado localmente

### Inferences
- Recetas (API estable 4.x–5.x; nombres de modificadores son tipos RNA):
  ```python
  import bpy, bmesh
  from mathutils import Vector
  ob = bpy.context.active_object
  # Escala a mm objetivo (p.ej. lado mayor = 100 mm)
  f = 100.0 / max(ob.dimensions); ob.scale *= f
  bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
  # Booleano (agujero / corte / texto en relieve: texto -> convertir a malla con bpy.ops.object.convert(target='MESH'))
  m = ob.modifiers.new("b", 'BOOLEAN'); m.object = cutter; m.operation = 'DIFFERENCE'  # 'UNION' para emboss
  m.solver = 'EXACT'; bpy.ops.object.modifier_apply(modifier=m.name)
  # Hueco / pared: Solidify (thickness negativa = hacia dentro)
  s = ob.modifiers.new("s", 'SOLIDIFY'); s.thickness = 2.0; s.offset = -1; s.use_even_offset = True
  # Chaflán
  b = ob.modifiers.new("c", 'BEVEL'); b.width = 0.8; b.segments = 1; b.limit_method = 'ANGLE'
  # Decimate
  d = ob.modifiers.new("d", 'DECIMATE'); d.ratio = 0.5
  # Split en piezas sueltas
  bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.separate(type='LOOSE'); bpy.ops.object.mode_set(mode='OBJECT')
  # Corte plano (bisect) para partir piezas grandes > 220 mm:
  bm = bmesh.new(); bm.from_mesh(ob.data)
  bmesh.ops.bisect_plane(bm, geom=bm.verts[:]+bm.edges[:]+bm.faces[:], plane_co=(0,0,100), plane_no=(0,0,1), clear_outer=True)
  # (rellenar el corte con bmesh.ops.edgeloop_fill / holes_fill)
  # Merge by distance + normales
  bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.001); bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
  bm.to_mesh(ob.data); bm.free()
  # Apoyar en Z=0 y centrar en XY (en el origen; el slicer recentra)
  ws = [ob.matrix_world @ v.co for v in ob.data.vertices]
  mn = Vector(map(min, zip(*ws))); mx = Vector(map(max, zip(*ws)))
  ob.location += Vector((-(mn.x+mx.x)/2, -(mn.y+mx.y)/2, -mn.z))
  ```
- Comprobar que el bounding box cabe en 220×220×250 antes de exportar; si no, bisect o escalar.
- Grosor mínimo de pared para boquilla 0,4: ≥0,8 mm (2 líneas); detalles ≥0,4 mm; texto en relieve ≥0,6 mm de alto (reglas generales de FDM, sin fuente específica aquí).

### Gaps
- No se verificó Solidify/Decimate/bisect en este entorno (solo Boolean/Bevel/merge/normales/colocación).

## B4. Alternativas/complementos: trimesh, pymeshlab, manifold3d, Tweaker-3

### Takeaway
Disponibles en PyPI (nov. 2026): trimesh 5.2.2, pymeshlab 2025.7.post1, manifold3d 3.5.5. Tweaker-3 (Schranz, Salzburg Research) auto-orienta STL/3MF por CLI (`tweaker3 -i pieza.stl -x` modo extendido, `-min sur` minimiza superficie de soportes).

### Cited Findings
- Versiones en PyPI: trimesh 5.2.2, pymeshlab 2025.7.post1, manifold3d 3.5.5, bpy 5.3.0 (también 5.2.x, 5.1.x) — verificado localmente con `pip index versions` (2026-11-23)
- Tweaker-3: busca orientación óptima de STL/3MF; `python Tweaker.py -i demo_object.stl -vb` o instalado `tweaker3 -i demo_object.stl`; modo extendido recomendado para más fiabilidad; `-min sur` optimiza superficie de soporte; disponible como plugin de Cura y OctoPrint; el repo STL-tweaker antiguo está deprecado — [Tweaker-3 (mirror GitHub)](https://githubrp.bychv-a.workers.dev/ChristophSchranz/Tweaker-3); [Salzburg Research](https://www.salzburgresearch.at/?p=17279)
- stlbench usa Tweaker-3 en una pipeline orientar→escalar→distribuir — [PyPI stlbench](https://pypi.org/project/stlbench/)

### Inferences
- Roles recomendados: **trimesh** para análisis rápido (`mesh.is_watertight`, `is_winding_consistent`, `volume`, `bounds`, `split()`, `fill_holes()`, `fix_normals()`); **pymeshlab** para reparación seria (filtros `meshing_remove_duplicate_vertices`, `meshing_repair_non_manifold_edges`, `meshing_close_holes`); **manifold3d** para booleanos garantizados-manifold y rápidos (mismo motor que el solver "Manifold" de Blender 4.5+ — conocimiento previo, no verificado aquí). Nombres de API de memoria; verificar.
- Flujo agente sugerido: import → trimesh check → (pymeshlab repair si no watertight) → Tweaker-3 orientación → Blender para modificaciones → trimesh check final → slicer CLI.

### Gaps
- No se obtuvieron docs oficiales de trimesh/pymeshlab/manifold3d (no consultados por límite de llamadas); versión actual de Tweaker-3 no confirmada (kandi listaba 3.9.1).

## B5. Diferencias de versiones de Blender y módulo pip `bpy`

### Takeaway
Ubuntu apt (24.04) da Blender 4.0.2: tiene `wm.stl_import` pero exporta solo con `export_mesh.stl`, y Print3D Toolbox bundled. 4.1 añade `wm.stl_export` C++. 4.2 LTS mueve add-ons a extensiones. 5.1 sube a Python 3.13. `pip install bpy` solo funciona con la versión exacta de Python de esa release (5.x → 3.13; 4.5 LTS → 3.11).

### Cited Findings
- Blender del sistema en este contenedor: 4.0.2 (`/usr/bin/blender`) — verificado localmente
- 4.1: exportador STL C++ y migración a `wm.stl_*` — [Release notes 4.1](https://developer.blender.org/docs/release_notes/4.1/pipeline_assets_io/)
- 4.2: add-ons bundled → extensiones — [devtalk](https://devtalk.blender.org/t/changes-to-add-on-and-themes-bundling-4-2-onwards/34593); [Blender 4.2 LTS](https://www.blender.org/?p=92674)
- 4.5 LTS notas de I/O — [Release notes 4.5](https://developer.blender.org/docs/release_notes/4.5/pipeline_assets_io/)
- 5.1: Python actualizado a 3.13 — [Release notes 5.1 Python API](https://developer.blender.org/docs/release_notes/5.1/python_api/)
- Cada release de `bpy` en PyPI soporta una sola versión de Python; versiones fuera de la ventana LTS se retiran de PyPI y quedan en download.blender.org/pypi/bpy/ — [PyPI bpy](https://pypi.org/p/bpy); [PyPI bpy 4.5.13](https://pypi.org/project/bpy/4.5.13/); 4.5 LTS en Python 3.11, 5.x en 3.13 — [pyvista-blender install](https://kmarchais.github.io/pyvista-blender/getting-started/installation/)
- Problemas históricos de instalación de bpy por versión de Python — [issue #120801](https://projects.blender.org/blender/blender/issues/120801); [issue #119156](https://projects.blender.org/blender/blender/issues/119156)
- Python del contenedor 3.13.18 y PyPI ofrece bpy 5.3.0 → compatible — verificado localmente

### Inferences
- Opción robusta para el agente: `pip install bpy==5.3.0` en venv Python 3.13 (API `wm.stl_export` disponible, sin depender del apt 4.0). Alternativa: descargar tarball oficial 4.5 LTS. Con 4.0 apt, usar el patrón con fallback a `export_mesh.stl`.
- Con módulo `bpy` no hay `--factory-startup`; usar `bpy.ops.wm.read_factory_settings(use_empty=True)` al inicio.

### Gaps
- No se verificaron los cambios de API de 5.0 (p. ej. si se eliminó `export_mesh.stl` del todo) ni el tamaño de la wheel de bpy 5.3.
