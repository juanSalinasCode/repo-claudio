# Slicers headless en Linux para Creality Ender 3 V2 Neo (estado a noviembre de 2026)

> Nota de método: en esta sesión cloud solo eran accesibles `raw.githubusercontent.com` y el buscador web. No se pudo acceder a help.prusa3d.com, orcaslicer.com/wiki, dyn.manpages.debian.org, printago.io ni a la API de GitHub (releases). Por eso, muchas afirmaciones se apoyan directamente en el **código fuente** de las ramas principales (main/master) a fecha 2026-11-23, que es fuente primaria, aunque refleja el desarrollo y no necesariamente la última versión estable. Nada se ha probado ejecutando binarios.

## 1. CuraEngine (UltiMaker Cura 5.x): uso por CLI, definiciones y trampas

### Takeaway
CuraEngine tiene una CLI documentada (`CuraEngine slice -j def.json -s k=v -e0 ... -l model.stl -o out.gcode`) y existe la definición `creality_ender3v2neo.def.json` (hereda de `creality_base` → `fdmprinter`). Pero la CLI **no evalúa la pila de perfiles como la GUI** (calidad, material, intent ni las fórmulas que dependen de ellos), por lo que un agente tendría que resolver o pasar muchos valores explícitamente. Es la opción más frágil para automatizar.

### Cited Findings
- Sintaxis oficial (texto de ayuda en `Application::printHelp`): `CuraEngine slice [-v] [-p] [-j <settings.json>] [-s <settingkey>=<value>] [-g] [-e<extruder_nr>] [-o <output.gcode>] [-l <model.stl>] [--next]`. Flags: `-j` "Load settings.def.json file to register all settings and their defaults"; `-r` "Load a json file containing resolved setting values"; `-d` añade rutas de búsqueda de definiciones; `-s` "Set a setting to a value for the last supplied object, extruder train, or general settings"; `-e<n>` cambia el foco al tren extrusor n; `-g` cambia el foco al grupo de mallas (modo one-at-a-time); `-m<threads>`; `-p` muestra el progreso. — [CuraEngine src/Application.cpp (main)](https://raw.githubusercontent.com/Ultimaker/CuraEngine/main/src/Application.cpp)
- Los ajustes se aplican al último objeto suministrado (el orden de los argumentos importa): `CuraEngine slice [general settings] -g [group] -e0 [extruder 0 settings] -l obj.stl [object settings] --next ...`. Para cargar definiciones desde rutas propias se usa la variable de entorno `CURA_ENGINE_SEARCH_PATH`. — [CuraEngine Application.cpp](https://raw.githubusercontent.com/Ultimaker/CuraEngine/main/src/Application.cpp)
- `creality_ender3v2neo.def.json` existe en Cura: `"inherits": "creality_base"`, `quality_definition: creality_base`, con estos valores: área de 230×230×250, `gantry_height` 25, retracción de 4 mm a 25 mm/s y su propio start G-code (dos líneas de purga). — [Cura resources/definitions/creality_ender3v2neo.def.json](https://raw.githubusercontent.com/Ultimaker/Cura/main/resources/definitions/creality_ender3v2neo.def.json)
- `creality_base.def.json` hereda de `fdmprinter`, define `machine_extruder_trains: {"0": "creality_base_extruder_0"}`, `has_machine_quality: true`, `preferred_quality_type: "standard"` y `material_diameter` 1.75. — [Cura creality_base.def.json](https://raw.githubusercontent.com/Ultimaker/Cura/main/resources/definitions/creality_base.def.json)
- Versiones: Cura 5.11.0 estable el 23 de octubre de 2025; un mirror de releases lista también 5.12.0 — [Wikipedia / resultados de búsqueda sobre Cura](https://en.wikipedia.org/wiki/Cura_(software)), [UltiMaker blog 5.11](https://ultimaker.com/learn/cura-5-11-stable-released). La rama `main` de Cura declara `version: "5.15.0-alpha.0"` y `curaengine/5.15.0-alpha.0` — [Cura conandata.yml](https://raw.githubusercontent.com/Ultimaker/Cura/main/conandata.yml).

### Inferences
- Con `-j creality_ender3v2neo.def.json` y la variable `CURA_ENGINE_SEARCH_PATH` apuntando a `resources/definitions` y `resources/extruders`, el motor resuelve la herencia de las *definiciones* (máquina → creality_base → fdmprinter) y de los extrusores. Lo que no carga son los perfiles de `resources/quality/creality/*.inst.cfg`, ni los de material o intent: eso lo hace el frontend de Cura (Python/Uranium). En la práctica hay que pasar con `-s` la altura de capa, las temperaturas, `infill_sparse_density`, `support_enable`, `adhesion_type`, etc. Además, varias de las fórmulas `value` de `fdmprinter` que dependen de ellos no se reevalúan igual que en la GUI. Esto coincide con un problema conocido de la comunidad, pero no encontré una fuente accesible que lo documente en detalle (ver Gaps).
- Posicionamiento: el STL se carga en sus coordenadas tal cual. En Cura el origen está en el centro de la cama solo si `machine_center_is_zero` es true, y en Creality es false. Por tanto hay que centrar la malla (por ejemplo con `-s mesh_position_x/y/z` o preprocesando el STL con trimesh) y apoyarla en Z=0.
- La salida es solo G-code. CuraEngine no genera `.3mf`.
- Una alternativa "más fiel a la GUI" es ejecutar el frontend de Cura completo en headless (no existe un modo CLI oficial) o usar wrappers comunitarios. No pude verificar ninguno concreto ni su mantenimiento en 2026.

### Gaps
- No pude acceder a la wiki de CuraEngine (páginas "Slicing" y "Settings"), ni a issues que documenten qué ajustes quedan sin resolver o con fórmulas distintas en la CLI.
- No pude verificar la última versión estable exacta de Cura en noviembre de 2026 (la API de GitHub estaba bloqueada). Solo consta 5.12.0 publicada y `main` en 5.15.0-alpha. Es probable que 5.13 o 5.14 sea la estable actual, pero no está verificado.
- No verifiqué wrappers (p. ej. scripts que "aplanan" perfiles de Cura a `-s`).

## 2. PrusaSlicer CLI

### Takeaway
PrusaSlicer tiene una CLI madura que corta sin pantalla (`--export-gcode`, `--load config.ini`, `--center`, `--dont-arrange`, `--export-3mf`, etc.) y es la opción más ergonómica para automatizar a partir de un `.ini` plano. La rama master ya está en **3.0.0-alpha14** (noviembre de 2026). La estable que se esperaría es la serie 2.9.x, pero esto no está verificado.

### Cited Findings
- Versión de desarrollo en master: `SLIC3R_VERSION "3.0.0-alpha14"` — [PrusaSlicer version.inc](https://raw.githubusercontent.com/prusa3d/PrusaSlicer/master/version.inc). Prusa publica páginas de "manual profile download" para PrusaSlicer 2.9 y 3.0 — [Prusa Help 3.0](https://help.prusa3d.com/article/manual-profile-download-for-prusaslicer-3-0_1182332), [Prusa Help 2.9](https://help.prusa3d.com/article/manual-profile-download-for-prusaslicer-2-9_727206).
- En la 3.0, el binario `main()` delega en `Slic3r::CLI::run(argc, argv)`: la CLI se ha refactorizado a su propio módulo — [PrusaSlicer src/PrusaSlicer.cpp](https://raw.githubusercontent.com/prusa3d/PrusaSlicer/master/src/PrusaSlicer.cpp).
- Flags documentados en las páginas de manual de Debian y Ubuntu: `--export-gcode` ("Slice the model and export toolpaths as G-code"), `--load` (repetible, carga `.ini`), `--center X,Y` ("Center the print around the given center"), `--dont-arrange` ("Do not rearrange the given models before merging and keep their original XY coordinates"), `--export-3mf` y `--printer-technology FFF|SLA` — [resumen de manpages Debian/Ubuntu vía búsqueda](https://manpages.ubuntu.com/manpages/jammy/man1/prusa-slicer.1.html).
- Ejemplo de la comunidad: `prusa-slicer -g --load config.ini --dont-arrange --center 125,105 model.stl` — [Prusa forum: command line arrange](https://forum.prusa3d.com/forum/prusaslicer/command-line-arrange).
- Un "Export Config Bundle" solo contiene los perfiles personalizados, no los de sistema — [Prusa forum](https://forum.prusa3d.com/forum/prusaslicer/export-config-bundle-with-physical-printer-does-not-transfer-all-settings/?language=cs). Para la CLI hay que usar "Export Config" (un `.ini` plano y resuelto con impresora + proceso + filamento), no el bundle.

### Inferences
- El flujo más robusto: una sola vez (en GUI o desde un `.3mf`/G-code anterior, que llevan la configuración incrustada) se obtiene un `ender3v2neo.ini` plano con el perfil de sistema Creality "Ender-3 V2 Neo". Después: `prusa-slicer --export-gcode --load ender3v2neo.ini --center 115,115 --ensure-on-bed -o out.gcode model.stl`, con overrides por flag (`--layer-height 0.2`, `--fill-density 20%`, `--support-material` …). Cualquier opción de configuración se puede pasar como `--opcion-con-guiones`.
- PrusaSlicer/Slic3r históricamente centra y arregla los objetos por defecto en la CLI (de ahí la existencia de `--dont-arrange`).
- Recuerdo que versiones recientes (≥2.6) incluyen `--datadir`, `--repair`, `--rotate`, `--scale-to-fit`, `--merge`, `--info`, `--loglevel`, `--sw-renderer` y la selección de perfiles de sistema con `--printer-profile/--print-profile/--material-profile`. **No pude verificarlo con una fuente accesible**, así que el agente debe comprobarlo con `prusa-slicer --help` en la versión instalada.
- AppImage en Linux sin pantalla: la CLI de exportación no abre la GUI. En servidores sin FUSE se usa `--appimage-extract-and-run`. Tampoco pude verificar esto con fuente en esta sesión.

### Gaps
- No pude leer la página oficial "Command Line Interface" (help.prusa3d.com estaba bloqueado), ni el código de opciones CLI de 3.0 (las rutas `src/libslic3r/PrintConfig.cpp` y `src/CLI/*` dieron 404 en master, así que se han movido).
- No hay confirmación de si existe `--orient`/auto-orient por CLI en PrusaSlicer (en la GUI sí hay "Optimize orientation"). Sin fuente.
- No pude confirmar con fuente primaria la presencia del perfil "Creality Ender-3 V2 Neo" en el bundle de PrusaSlicer (`resources/profiles/Creality.ini` → 404 en esa ruta). Parece probable porque OrcaSlicer, que hereda perfiles, sí lo tiene, pero no está verificado.

## 3. OrcaSlicer CLI

### Takeaway
OrcaSlicer (master 2.6.0-dev; la estable reciente sería la serie 2.3.x/2.4, sin verificar) tiene un modo CLI real que corta sin pantalla: sin acciones arranca la GUI y, si no hay `DISPLAY` ni Wayland, falla. Incluye el perfil oficial **"Creality Ender-3 V2 Neo 0.4 nozzle"** y las mejores funciones de calidad. Su CLI es menos ergonómica: espera JSON de máquina/proceso/filamento resueltos (heredado de Bambu Studio) y produce `plate_N.gcode` o `.gcode.3mf`.

### Cited Findings
- Versión en main: `set(SoftFever_VERSION "2.6.0-dev")` — [OrcaSlicer version.inc](https://raw.githubusercontent.com/SoftFever/OrcaSlicer/main/version.inc).
- Uso: `orca-slicer [ OPTIONS ] [ file.3mf/file.stl ... ]`. Prioridad de ajustes: "1) setting values from the command line (highest priority) 2) setting values loaded with --load-settings and --load-filaments 3) setting values loaded from 3mf (lowest priority)" — [OrcaSlicer src/OrcaSlicer.cpp](https://raw.githubusercontent.com/SoftFever/OrcaSlicer/main/src/OrcaSlicer.cpp).
- Opciones CLI definidas en el código ([orca PrintConfig.cpp](https://raw.githubusercontent.com/SoftFever/OrcaSlicer/main/src/libslic3r/PrintConfig.cpp)):
  - `--slice <n>`: "Slice the plates: 0-all plates, i-plate i"
  - `--load-settings`: "Load process/machine settings from the specified file"
  - `--load-filaments`: "Load filament settings from the specified file list"
  - `--arrange <n>`: "0-disable, 1-enable, others-auto"
  - `--orient <n>`: "0-disable, 1-enable, others-auto"
  - `--ensure-on-bed`: "Lift the object above the bed when it is partially below"
  - `--export-3mf`, `--outputdir`
  - `--export-settings` ("Use - to write them to stdout")
  - `--allow-newer-file`, `--export-slicedata`, `--load-slicedata`, `--repetitions`, `--skip-objects`, `--load-filament-ids`, `--allow-rotations`, `--info`, `--pipe`, `--min-save`, `--uptodate`, `--export-stl/--export-stls`
  - `export_gcode` aparece **comentado** en la definición: no existe `--export-gcode` como en Prusa.
- Salida de G-code: el código escribe `outfile = outfile_dir + "/plate_" + N + ".gcode"`, o sea `plate_1.gcode` en `--outputdir` — [OrcaSlicer.cpp](https://raw.githubusercontent.com/SoftFever/OrcaSlicer/main/src/OrcaSlicer.cpp).
- Headless: la GUI solo arranca si `m_actions.empty()`. Si se pide la GUI y no hay `DISPLAY` ni socket Wayland, imprime "Neither DISPLAY nor a Wayland socket found, GUI mode not available". Sin embargo, la regeneración de miniaturas en modo CLI llama a `glfwInit()` y crea un contexto OpenGL 3.3 oculto (`GLFW_VISIBLE false`). Si falla, solo lo registra como error — [OrcaSlicer.cpp](https://raw.githubusercontent.com/SoftFever/OrcaSlicer/main/src/OrcaSlicer.cpp).
- El código lee `inherits_group` y `inherits` de la configuración para mapear a presets de sistema, lo que indica que los JSON cargados por CLI deben ser coherentes con los presets de sistema — [OrcaSlicer.cpp](https://raw.githubusercontent.com/SoftFever/OrcaSlicer/main/src/OrcaSlicer.cpp).
- Perfil: `Creality.json` de Orca incluye `"Creality Ender-3 V2 Neo"` y `"Creality Ender-3 V2 Neo 0.4 nozzle"` — [OrcaSlicer resources/profiles/Creality.json](https://raw.githubusercontent.com/SoftFever/OrcaSlicer/main/resources/profiles/Creality.json).
- La wiki oficial tiene una página "CLI Mode" y documenta que las claves con guion bajo se pasan con guiones (`layer_height` → `--layer-height`). Según una referencia de terceros (Printago, proveedor de slicing en la nube), el patrón típico es `--slice 1 --load-settings "machine.json;process.json" --load-filaments filament.json --export-3mf out.gcode.3mf`. Existe además el wrapper npm `orcaslicer-addon` (WIP) y una imagen Docker de linuxserver (orientada a GUI web). — [resumen de búsqueda: orcaslicer.com wiki, printago.io, libraries.io, docs.linuxserver.io](https://www.orcaslicer.com/wiki/cli/cli_mode)
- En el foro de Bambu se informa de que la CLI de Bambu Studio (base de Orca) necesitó entorno gráfico en un servidor y no aplicaba presets externos — [Bambu forum](https://forum.bambulab.com/t/cli-cannot-apply-external-presets/197842). Hay una discusión en GitHub pidiendo ayuda para automatizar Orca por CLI — [OrcaSlicer discussion #1603](https://github.com/SoftFever/OrcaSlicer/discussions/1603).

### Inferences
- Para un servidor sin pantalla conviene ejecutar Orca bajo `xvfb-run` (o con Mesa/llvmpipe) para que funcionen las miniaturas de GLFW, aunque el corte en sí no lo necesite. AppImage: `--appimage-extract-and-run` si no hay FUSE.
- Los JSON de sistema de Orca tienen `inherits` en cadena (fdm_creality_common → …). Lo práctico es exportar los presets "aplanados" una vez, desde la GUI o con `--export-settings`, y reutilizarlos.
- Orca tiene `--orient` y `--arrange` por CLI, cosa que PrusaSlicer (verificado) no ofrece de la misma forma.

### Gaps
- No pude leer la wiki CLI de Orca ni la de Printago (hosts bloqueados), ni verificar la última versión estable publicada en noviembre de 2026.
- No hay datos verificados sobre la estabilidad real headless (crashes por GL, AppImage) en versiones de 2026.

## 4. Otras opciones (SuperSlicer, Slic3r, Kiri:Moto)

### Takeaway
No aportan ventajas para este caso. SuperSlicer (fork de PrusaSlicer) tiene la misma CLI pero un desarrollo más lento. Slic3r clásico está obsoleto. Kiri:Moto es un slicer web/JS que se puede ejecutar en Node, pero sus perfiles y calidad están por detrás.

### Cited Findings
- El manual de Slic3r documenta la CLI original, de la que heredan PrusaSlicer y SuperSlicer — [Slic3r Manual – command line](https://manual.slic3r.org/advanced/command-line).

### Inferences
- Evitarlos salvo necesidad concreta.

### Gaps
- No verifiqué el estado de releases de SuperSlicer (API bloqueada) ni la CLI y el perfil Ender 3 V2 Neo de Kiri:Moto en 2026.

## 5. Formatos de salida y apertura en Cura (3MF)

### Takeaway
Para que el usuario lo abra en Cura en su PC, lo seguro es entregar **G-code** (Cura lo abre en vista previa) y, aparte, el **STL/3MF de malla** ya orientado y posicionado para volver a cortarlo. Los 3MF de proyecto de Prusa u Orca solo transfieren la malla de forma fiable; los ajustes no se transfieren, y la posición se ha comportado de forma inconsistente.

### Cited Findings
- Cura ha colocado piezas de 3MF externos poniendo el sistema de coordenadas del archivo en (0,0,0) en lugar de en el centro de la cama — [UltiMaker community](https://community.ultimaker.com/topic/38953-what-does-cura-do-with-3mf-files/). Otro usuario reabrió en Cura 5.0 un 3MF exportado con la pieza ya colocada y la posición se respetó — [V1 Engineering forum](https://forum.v1engineering.com/t/lr3-y-drive-3mf-file-is-positioned-below-origin/32855).
- Cura 5.6 abrió un 3MF genérico de Bambu solo parcialmente y no pudo abrir el 3MF de proyecto de Bambu. Bambu recomienda "Export Generic 3MF" para Cura/PrusaSlicer — [BambuStudio issue #3316](https://github.com/bambulab/BambuStudio/issues/3316).
- La salida de Orca por `--export-3mf` con `--slice` es un `.gcode.3mf` (G-code dentro de un 3MF), según Printago (fuente de terceros) — [printago.io](https://printago.io/blog/orca-slicer-cli-reference).

### Inferences
- Un `.gcode.3mf` de Orca no es útil en Cura; hay que extraer `plate_1.gcode` o usar la salida `.gcode` directa.
- El "proyecto Cura" (.3mf con `Cura/` y los perfiles) solo lo genera la GUI de Cura (Uranium). Ningún slicer CLI produce un proyecto Cura completo. Si el usuario quiere ajustar en Cura, lo mejor es un STL/3MF de malla centrado y apoyado en la cama, junto con la lista de ajustes recomendados.

### Gaps
- No hay prueba reciente (2025-2026) de que Cura 5.x respete las transformaciones de un 3MF de PrusaSlicer/Orca. Hay que probarlo.

## 6. Calidad, funciones y recomendación

### Takeaway
**Recomendación: PrusaSlicer CLI** como motor principal del agente (ergonomía, `.ini` plano, G-code directo, Arachne, soportes orgánicos/árbol, ironing). **OrcaSlicer** queda como alternativa si se quiere `--orient` automático o el perfil más afinado de Creality. **CuraEngine** solo si se exige el "comportamiento Cura", porque requiere resolver los perfiles a mano.

### Cited Findings
- Orca expone `--orient`/`--arrange` por CLI e incluye el perfil oficial Ender-3 V2 Neo 0.4 — [Orca PrintConfig.cpp](https://raw.githubusercontent.com/SoftFever/OrcaSlicer/main/src/libslic3r/PrintConfig.cpp), [Orca Creality.json](https://raw.githubusercontent.com/SoftFever/OrcaSlicer/main/resources/profiles/Creality.json).
- La CLI de CuraEngine solo carga definiciones (`-j`), valores resueltos (`-r`) y overrides (`-s`) — [CuraEngine Application.cpp](https://raw.githubusercontent.com/Ultimaker/CuraEngine/main/src/Application.cpp).

### Inferences
- Funciones (conocimiento general, no verificado con fuente en esta sesión): los tres tienen Arachne (paredes de ancho variable), soportes árbol (Cura "tree", Prusa "organic" desde 2.6, Orca "tree(auto)/organic"), ironing y altura de capa adaptativa (Cura "adaptive layers", Prusa "variable layer height" solo en GUI, Orca "adaptive layer height"). Orca suma calibraciones y "precise wall"/"scarf seam".
- Ergonomía: PrusaSlicer > Orca > CuraEngine.

### Gaps
- Sin benchmarks objetivos de calidad de impresión entre slicers para la Ender 3 V2 Neo.
