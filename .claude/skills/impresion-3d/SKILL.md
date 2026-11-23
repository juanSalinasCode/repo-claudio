---
name: impresion-3d
description: Preparar y laminar modelos 3D (STL/OBJ/3MF) para la Creality Ender 3 V2 Neo del usuario. Usar cuando el usuario pase un STL, pida modificarlo (escalar, rotar, cortar, agujeros, texto, reparar), orientarlo, o dejarlo listo para imprimir / "ponerlo en Cura" / sacar G-code.
---

# Impresión 3D — Ender 3 V2 Neo

Herramientas en `print3d/` (instalarlas con `bash print3d/setup.sh` si falta `/opt/3d`).

## Impresora (datos fijos)
- Volumen real **220 × 220 × 250 mm** (el perfil de Cura dice 230: corregido en el script).
- Boquilla 0,4 mm, Bowden, filamento 1,75 mm, cama PC hasta 100 °C, CR Touch (malla 4×4).
- Firmware Marlin de Creality: el start G-code hace `G28` + `G29` (no `M420`, falla en fw 1.70).
- Sin red: el usuario imprime desde microSD. Nunca "mandes a imprimir"; entregá archivos.

## Flujo
1. **Analizar**: `/opt/3d/venv/bin/python print3d/prep.py pieza.stl --info --preview vista.png`
   Mirá `dimensiones_mm`, `estanca`, `area_voladizos_cm2`, `entra_en_cama`. Si las medidas
   son minúsculas (<5 mm) probablemente está en cm o m → `--units cm|m`.
   Siempre mirá el PNG (Read) antes de seguir.
2. **Modificar** (si hace falta):
   - Simple: `--scale 1.5`, `--fit 120` (lado mayor), `--rotate 90,0,0`, `--mirror x`,
     `--orient` (pose más estable), `--repair`.
   - A medida: escribir un script bpy y pasarlo con `--script cambios.py` (recibe `obj`).
     Ej. booleano: crear cilindro con `bpy.ops.mesh.primitive_cylinder_add`, modificador
     `BOOLEAN` operación `DIFFERENCE`, `solver='EXACT'`, aplicar y borrar el cortador.
     Unidades: 1 unidad Blender = 1 mm.
3. **Ubicar y exportar**: `prep.py pieza.stl -o pieza_lista.stl [opciones] --preview pieza.png --report pieza.json`
   (siempre apoya en Z=0 y centra; reparar si no es estanca).
4. **Laminar con Cura (CuraEngine 5.14, perfil oficial creality_ender3v2neo + correcciones)**:
   `python3 print3d/cura_slice.py pieza_lista.stl -o pieza.gcode --material PLA --quality standard [-s clave=valor ...]`
   - Materiales: PLA, PETG, ABS, TPU. Calidades: super (0,12), standard (0,2), low (0,28), adaptive, draft.
   - Ajustes útiles: `-s infill_sparse_density=20`, `-s support_enable=True -s support_structure=tree`,
     `-s adhesion_type=brim|skirt|raft|none`, `-s wall_line_count=3`, `-s infill_pattern=gyroid`.
   - Ver todos los valores resueltos: `--dump-settings ajustes.json`. `--stock` = perfil Cura sin correcciones.
   - Soportes: activarlos si `area_voladizos_cm2` es relevante y no se puede reorientar.
5. **Entregar**: STL listo (para abrir en Cura en la PC: Cura lo centra en la cama) + `.gcode`
   (para la microSD) + PNG de vista previa. Informar tiempo, filamento (m y g), temperaturas.

## Perfiles de partida (calibrar con torres)
| | PLA | PETG |
|---|---|---|
| Boquilla | 205 °C | 235 °C |
| Cama | 60 °C | 75 °C |
| Retracción | 5 mm @ 45 mm/s | 5 mm @ 35 mm/s |
| Ventilador | 100 % | 40 % |

## Notas
- CuraEngine solo NO resuelve fórmulas ni perfiles: por eso existe `cura_slice.py` (no llamarlo a pelo).
- Blender 5.3 (bpy del venv) usa `bpy.ops.wm.stl_import/stl_export`; el `blender` de apt (4.0) usa `bpy.ops.export_mesh.stl`.
- Render sin GPU: motor `BLENDER_WORKBENCH` (rápido). EEVEE tarda ~50 s.
- Informe completo de la investigación: `reports/Claude para impresión 3D.md`.
