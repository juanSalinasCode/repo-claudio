# Skills, plugins, MCPs y herramientas de agente para impresión 3D con Claude (nov. 2026)

Nota de método: la API de GitHub (`gh api`) estaba bloqueada en esta sesión, así que las estrellas y fechas vienen de los README o de directorios de MCP, capturados el 2026-11-23. La mayoría de las páginas de GitHub no mostraban la fecha del último commit, por lo que la actualidad de cada proyecto solo se puede estimar por el número de commits y la versión. buildcad.ai no se pudo abrir (dominio fuera de la red permitida de la sesión).

## 1. Servidores MCP de Blender: ¿alguno funciona sin interfaz (`blender -b`)?

### Takeaway
El estándar de facto, ahujasid/blender-mcp (~35.5k estrellas), necesita la GUI de Blender abierta con su addon escuchando en un socket. Blender tiene ahora un servidor MCP oficial de Blender Lab (Blender 5.1+), que también funciona con addon y socket. Hay varias alternativas pensadas para trabajar sin interfaz (sandraschi, @three-ws/nirholas, uno-blender-mcp, ellmos, dcc-mcp, tspspi, bpy-dev), pero todas son pequeñas y jóvenes. Para un servidor Linux sin interfaz, lo más robusto suele ser que Claude escriba scripts `bpy` y los ejecute con `blender -b --python`, sin MCP.

### Cited Findings
- **ahujasid/blender-mcp** (repo renombrado a `ahujasid/mcp-for-blender`): 35.5k estrellas, 3.3k forks, 276 commits. Su addon abre un socket en `localhost:9876`. Ofrece las herramientas `execute_blender_code`, `look`, `get_scene_info`, `generate_3d`, `search_assets`, `import_asset` y otras. La documentación no menciona ningún modo headless. El socket "has no authentication or encryption". El safe mode viene desactivado por defecto y hay una telemetría anónima mínima, activa salvo que se defina `DISABLE_TELEMETRY=true`. — [GitHub](https://github.com/ahujasid/blender-mcp)
- **Servidor MCP oficial de Blender Lab**: está en blender.org/lab/mcp-server, con el código en projects.blender.org/lab/blender_mcp. Varias guías de terceros indican que requiere Blender 5.1 o posterior, que se distribuye como addon más un paquete `.mcpb` y que escucha en localhost:9876. Según una comparativa, la propia página de Blender Lab advierte que el servidor ejecuta código generado por el LLM sin ninguna salvaguarda. Todo esto procede de fuentes secundarias y no lo verifiqué en la página oficial. — [blender.org](https://www.blender.org/?p=96198); [comparativa strayspark](https://www.strayspark.studio/blog/official-blender-mcp-server-comparison-2026); [claude.com/connectors/blender](https://claude.com/connectors/blender)
- **bpy-dev/blender-mcp**: es una distribución independiente basada en el MCP de Blender Lab que añade "standalone bpy" y ejecución headless o sobre archivos guardados. En modo background las respuestas tienen que ser síncronas. — [GitHub](https://github.com/bpy-dev/blender-mcp)
- **sandraschi/blender-mcp**: usa FastMCP y lanza Blender como subproceso headless por defecto, con un puente en vivo opcional. Expone 41 herramientas "portmanteau" que cubren más de 150 operaciones (mallas por lotes, VSE, Grease Pencil, VRM, splats). Incluye un dashboard en React y una app en Tauri. — [GitHub](https://github.com/sandraschi/blender-mcp)
- **nirholas/blender-mcp (`@three-ws/blender-mcp`)**: lanza `blender -b` en un proceso nuevo por cada llamada, sin addon ni display. Sirve para inspeccionar y convertir entre GLB, glTF, FBX, OBJ, STL, PLY, USD y otros formatos, para generar una preview renderizada que vuelve inline y para ejecutar scripts bpy. Se instala con `npx -y @three-ws/blender-mcp`. — [GitHub](https://github.com/nirholas/blender-mcp)
- **suprombb3131-code/uno-blender-mcp**: servidor en Node que corre Blender `--background` por stdio. Está orientado a escenas de estudio, turntables y scripts bpy. — [GitHub](https://github.com/suprombb3131-code/uno-blender-mcp)
- **ellmos-ai/ellmos-blender-use-mcp**: hace QA de assets sin interfaz (ejecución de scripts en background y reimportación de FBX para verificarla). No usa addon ni puerto TCP. — [GitHub](https://github.com/ellmos-ai/ellmos-blender-use-mcp)
- **dcc-mcp/dcc-mcp-blender**: tiene un bootstrap headless (`blender --background --python ...`) para CI y pipelines, con transporte Streamable HTTP. Sus herramientas tipadas cubren malla, UV, rig, materiales y render. — [GitHub](https://github.com/dcc-mcp/dcc-mcp-blender)
- **tspspi/mcpBlender**: se arranca con `start_blender(background=true)` para trabajar sin interfaz. Las capturas del viewport siguen necesitando GUI. — [GitHub](https://github.com/tspspi/mcpBlender)
- **B7Kompirine/blender-tether**: 0 estrellas y 13 commits. Tiene un modo daemon headless (`background=true`) y una herramienta `view` que renderiza offscreen varias vistas para que el agente compruebe su propio trabajo. Solo está probado en Windows 11 con Blender 5.2.4; "macOS and Linux are untested". No tiene herramientas propias para STL ni booleanos (habría que hacerlo con bpy a través de `run`). — [GitHub](https://github.com/B7Kompirine/blender-tether)
- **minihellboy/claude-blender**: control de Blender desde Claude Code por MCP. No obtuve detalles. — [GitHub](https://github.com/minihellboy/claude-blender)
- Hay limitaciones citadas en la documentación de otros proyectos: Blender tiene que estar abierto, la comunicación va por TCP y no hay undo/redo a nivel de MCP. — [glama ClaudeKit Blender MCP](https://glama.ai/mcp/servers/@olbboy/claudekit-blender-mcp/blob/e9ba0b47fccae95e42a1145d1909df47e1d0c792/GITHUB_README.md)
- El puente opcional a Blender de mcp-3D-printer-server "needs Blender open, because its add-on does not run in background mode". — [GitHub DMontgomery40](https://github.com/DMontgomery40/mcp-3D-printer-server)

### Inferences
- Para un servidor Linux sin GUI, ahujasid/blender-mcp y el MCP oficial de Blender Lab no sirven tal cual. Necesitarían Xvfb más Blender con GUI y el addon cargado, y no he encontrado documentación que confirme que esa combinación funcione.
- La vía más simple y robusta para este usuario: Claude Code escribe un script bpy (importar STL, aplicar modificadores, booleanos, Print3D Toolbox, exportar STL) y lo ejecuta con `blender -b --python script.py -- args`. No necesita MCP y funciona en headless.
- Si se quiere un MCP headless, los candidatos más razonables son nirholas/@three-ws (un proceso por llamada, maneja STL y devuelve previews inline) y sandraschi. Ambos son de un solo autor y de madurez no verificada.

### Gaps
- No pude obtener estrellas ni fechas del último commit para sandraschi, nirholas, uno, ellmos, dcc-mcp, tspspi ni bpy-dev (API de GitHub bloqueada).
- No encontré ningún informe independiente de alguien usando estos MCP headless para editar STL destinados a impresión.

## 2. MCP y skills de slicer (OrcaSlicer, PrusaSlicer, Cura, SpeakCAD, Bambu)

### Takeaway
Ya existe una oferta razonable: el plugin **SpeakCAD Slicer** en el directorio de plugins de Anthropic (que es remoto y devuelve un enlace al slicer web), varios MCP para OrcaSlicer y el multislicer de DMontgomery40. Para una Ender 3 V2 Neo en Linux sin interfaz, lo más sólido es llamar directamente a la CLI de PrusaSlicer u OrcaSlicer con un perfil exportado a `.ini`/`.json`. Los MCP de Orca dependen de una CLI a la que se le documentan fallos.

### Cited Findings
- **SpeakCAD Slicer** (Anthropic Directory, editor de nivel "community", versión 1.0.3, actualizado el 2026-10-19). Está compuesto por la skill `slice-for-your-printer` y el servidor MCP remoto `speakcad-slicer`. Busca el perfil de OrcaSlicer de la impresora (más de 380 impresoras de más de 60 marcas), fija altura de capa, material, relleno y soportes, y devuelve un enlace que abre el slicer online de SpeakCAD con todo seleccionado. Ahí el usuario suelta el archivo y descarga el G-code. — Catálogo de plugins de claude.ai (consultado con la herramienta SearchPlugins el 2026-11-23, sin URL pública)
- **DMontgomery40/mcp-3D-printer-server**: 270 estrellas, 52 forks y 318 commits, versión 1.2.26 o posterior, licencia GPL-2.0. Soporta los slicers PrusaSlicer, Slic3r, OrcaSlicer, CuraEngine, FULU OrcaSlicer-bambulab y Bambu Studio, apuntando al binario con `SLICER_PATH`. Se instala con `npx -y mcp-3d-printer-server` (Node 24) o con una imagen Docker. — [GitHub](https://github.com/DMontgomery40/mcp-3D-printer-server); [docs/SLICING.md](https://github.com/DMontgomery40/mcp-3D-printer-server/blob/main/docs/SLICING.md); [Docker Hub mcp/3d-printer](https://hub.docker.com/r/mcp/3d-printer)
- Advertencias de SLICING.md: la CLI de FULU OrcaSlicer-bambulab v1.0.0 da segfault en cada laminado, y PrusaSlicer ignora la configuración si el perfil es una carpeta en lugar de un único config exportado. Además, el servidor aplica las transformaciones del STL a una copia de la malla "in Orca's order to avoid a CLI crash", lo que apunta a que la CLI de Orca es frágil. — [SLICING.md](https://github.com/DMontgomery40/mcp-3D-printer-server/blob/main/docs/SLICING.md); [codeagent.directory](https://www.codeagent.directory/mcp/320)
- **dmikushin/orca-slicer-mcp**: maneja OrcaSlicer sin interfaz sobre Xvfb mediante DBus. Requiere un parche al código fuente que añade el comando `orca-cmd:export`. — [GitHub](https://github.com/dmikushin/orca-slicer-mcp)
- **BeMuCa/OrcaSlicer-mcp**: usa la CLI oficial de Orca sin parches. Está probado con OrcaSlicer 2.4.2 en Windows, controlado desde WSL2. — [glama](https://glama.ai/mcp/servers/BeMuCa/OrcaSlicer-mcp)
- **ShreddyKrueger75/claude-orcaslicer-mcp**: gestión de presets, análisis de G-code y control de impresora. Tiene un timeout de laminado de 600 s y la CLI no informa del progreso. — [glama](https://glama.ai/mcp/servers/ShreddyKrueger75/claude-orcaslicer-mcp); [mcprepository](https://mcprepository.com/ShreddyKrueger75/claude-orcaslicer-mcp)
- Existe un MCP específico de PrusaSlicer listado, pero no lo verifiqué. — (mención en la búsqueda; sin URL verificada)
- Skills de laminado: **bsafh/print3d-orcaslicer**. Claude escribe un script de Blender, la skill lo ejecuta, revisa la malla, lamina con la CLI de OrcaSlicer y le devuelve al agente lo que hay que corregir. Su impresora objetivo es una Orca Lab X2D. — [GitHub](https://github.com/bsafh/print3d-orcaslicer). Hay también una skill "G-code Slicing" que orquesta la CLI de Orca. — [mcpmarket](https://mcpmarket.com/tools/skills/3d-print-g-code-generator); [skills-hub print3d](https://skills-hub.ai/skills/text-to-cad-print3d)
- **Kiln** (codeofaxel/Kiln) también cubre el laminado (ver sección 3). — [PyPI kiln3d](https://pypi.org/project/kiln3d/)

### Inferences
- SpeakCAD es la opción más cómoda desde claude.ai. Pero el laminado ocurre en su web y el paso final es manual (subir el archivo y descargar el G-code), así que no sirve para un pipeline totalmente automático en un servidor.
- Para la Ender 3 V2 Neo, tanto PrusaSlicer como OrcaSlicer traen perfiles Creality. Lo recomendable es exportar un único perfil validado a mano y fijarlo en la skill, así se evita la trampa de "perfil como carpeta". En Linux sin interfaz, la CLI de PrusaSlicer (`prusa-slicer --export-gcode --load perfil.ini`) parece la menos problemática según la documentación anterior. Esto es inferencia; no está probado aquí.

### Gaps
- No encontré ningún MCP de Cura dedicado y mantenido. CuraEngine solo aparece como backend dentro de DMontgomery40.
- No confirmé que SpeakCAD incluya un perfil concreto de la "Ender-3 V2 Neo", aunque la cifra de más de 380 impresoras lo hace probable.
- Me faltan estrellas y fechas de los MCP de Orca.

## 3. MCP de control de impresora (OctoPrint, Moonraker/Klipper) para una Ender 3 V2 Neo

### Takeaway
Todos los MCP de impresora hablan con APIs de red (OctoPrint, Moonraker, PrusaLink, Bambu…). Una Ender 3 V2 Neo con Marlin de serie no tiene red, así que hace falta un host intermedio, típicamente una Raspberry Pi con OctoPrint por USB. A partir de ahí, mcp-3D-printer-server o Kiln pueden controlarla. Ninguno documenta soporte Marlin por serie salvo Kiln, que menciona "serial connections".

### Cited Findings
- **DMontgomery40/mcp-3D-printer-server**: soporta OctoPrint, Klipper (Moonraker), Duet, Repetier, Bambu Lab, PrusaLink/Prusa Connect y Creality. Bambu es lo más probado en hardware. OctoPrint, Klipper y Prusa están "community-reported". Duet, Repetier y Creality están implementados pero sin reportes de hardware. No menciona Marlin por serie. Advierte de que un comando correcto no verifica que la impresión física haya salido bien. Herramientas STL: medir, escalar, rotar, trasladar, extender la base, centrar, apoyar en plano, editar por secciones y previews SVG. Advierte del uso de memoria con STL de más de ~10 MB. — [GitHub](https://github.com/DMontgomery40/mcp-3D-printer-server)
- El estado que reporta esta herramienta es limitado en OctoPrint y Moonraker: los endpoints `/api/printer` y `/printer/info` no dan el progreso del trabajo. — [mcpservers.org](https://mcpservers.org/servers/DMontgomery40/mcp-3D-printer-server); [mcp.so](https://mcp.so/servers/mcp-3d-printer-server)
- **Kiln (codeofaxel/Kiln)**: MCP más CLI en Python (`pip install kiln3d`, lanzado con `kiln serve`). Cubre diseño, laminado, cola, monitorización y "fulfill". Backends: OctoPrint (marcado como estable), Moonraker, Bambu, Prusa Link, Elegoo y conexiones serie. Licencia AGPL-3.0, unas 35 estrellas (dato posiblemente desactualizado). Las fuentes no coinciden en el número de herramientas (353, 800, 887, 902) ni en la versión (1.1.3 frente a 1.5.0). — [PyPI kiln3d](https://pypi.org/project/kiln3d/); [mcpservers.org](https://mcpservers.org/servers/codeofaxel/kiln); [glama](https://glama.ai/mcp/servers/codeofaxel/kiln); [mcpgee](https://www.mcpgee.com/servers/kiln)
- **mholland97/3d-printer-mcp**: soporta OctoPrint y Klipper/Moonraker, con Bambu "coming soon". Moonraker en local no necesita API key. — [lobehub](https://lobehub.com/mcp/mholland97-3d-printer-mcp)
- **printmcp** (PyPI): MCP compatible con OctoPrint que pide una API key global o una Application Key. — [PyPI](https://pypi.org/project/printmcp/)
- Hay un listado "@octoprint/mcp-server-octoprint" en mcphub que no pude verificar como oficial y cuyas métricas parecen poco fiables. — [mcphub](https://mcphub.pages.dev/servers/octoprint)
- **OctoEverywhere MCP** figura en un catálogo (acceso remoto a OctoPrint/Klipper). No verifiqué sus detalles. — [archestra](https://archestra.ai/mcp-catalog/octoeverywhere__mcp)
- Existe un fork, jbp-kynze/mcp-3D-printer-server, con la misma descripción. — [GitHub](https://github.com/jbp-kynze/mcp-3D-printer-server)

### Inferences
- Arquitectura recomendada para este usuario: Ender 3 V2 Neo → USB → Raspberry Pi con OctoPrint (o, alternativamente, flashear Klipper y usar Moonraker) → MCP mcp-3D-printer-server o Kiln. La opción más sencilla y de menor riesgo es no dar control de impresión al agente: Claude entrega el G-code y el usuario lo pasa por microSD.
- Por seguridad, conviene limitar el agente a subir archivos y consultar el estado, y dejar el "start print" en manos humanas.

### Gaps
- No encontré documentación de que el firmware de serie de la V2 Neo tenga red ni de ningún MCP que hable Marlin por USB directamente, salvo la mención a "serial" de Kiln, que no verifiqué.
- No hay reportes de usuarios concretos con Ender 3 y estos MCP.

## 4. CAD por código (OpenSCAD, CadQuery, build123d), sus MCP y librerías de reparación de malla

### Takeaway
OpenSCAD tiene varios MCP. build123d está ganando terreno como lenguaje preferido de los agentes (agentcad, build123d-mcp), mientras que CadQuery apenas tiene MCP mantenidos. Para modificar STL ya existentes, el patrón de las skills es trimesh + manifold3d en Python headless.

### Cited Findings
- **OpenSCAD MCP**: RobertCoop/openscad-mcp (`claude mcp add openscad --transport stdio -- uvx openscad-mcp`, trae también una skill y un plugin de Claude Code), quellant/openscad-mcp (se ejecuta con uv desde git), `openscad-mcp-server` en PyPI (renderiza con la imagen Docker oficial de OpenSCAD) y format37/openscad-mcp (endpoint alojado para Claude web). — [RobertCoop](https://github.com/robertcoop/openscad-mcp); [quellant](https://github.com/quellant/openscad-mcp); [PyPI](https://pypi.org/project/openscad-mcp-server/); [format37](https://github.com/format37/openscad-mcp)
- **agentcad** (jdilla1277): CLI y MCP de CAD para agentes. Usa build123d por defecto y CadQuery como modo opcional de compatibilidad. — [GitHub](https://github.com/jdilla1277/agentcad)
- Una guía de buildcad.ai cita build123d-mcp como opción local y open source, y dice que no encontró "no maintained CadQuery server worth listing". OpenSCAD exporta STL/3MF pero no STEP. build123d y CadQuery exportan STEP y STL. — [buildcad.ai](https://buildcad.ai/guides/cad-mcp-servers) (a través del snippet de búsqueda; la página no se pudo abrir)
- Un benchmark de forgent3d pone a build123d-mcp con Claude Opus 5.5 en primer lugar (puntuación 0.830), pero se basa en blogs de proveedores con baselines distintas, así que es poco fiable. — [forgent3d](https://www.forgent3d.com/en/blog/ai-cad-languages); [druckworks](https://druckworks.eu/guides/openscad-or-build123d-with-ai)
- Librerías de malla usadas por las skills: **trimesh**, **manifold3d** y **shapely** para trabajar la malla, con build123d/CadQuery para B-rep. La skill m-esm advierte de que comprobar que la malla es watertight "no basta". — [m-esm/3d-print-modeling](https://github.com/m-esm/3d-print-modeling)
- mcp-3D-printer-server trae un "CAD engine" opcional de unos 1.5 GiB. — [GitHub](https://github.com/DMontgomery40/mcp-3D-printer-server)

### Inferences
- Para que Claude modifique STL que le pasa el usuario (escalar, cortar, añadir agujeros, unir), en un servidor sin interfaz, trimesh + manifold3d en Python suele bastar y es más fácil de verificar que Blender. Blender headless queda para operaciones de modelado más artísticas.

### Gaps
- No encontré fuentes específicas sobre pymeshlab ni admesh dentro de skills o MCP de Claude (ni madurez ni uso). Si se citan, tienen que ir sin fuente o investigarse aparte.
- No obtuve estrellas ni fechas de los MCP de OpenSCAD ni de agentcad.

## 5. Agent Skills (SKILL.md) publicadas para impresión 3D

### Takeaway
Hay una docena de skills públicas en GitHub, casi todas muy recientes y con 0 o 1 estrellas. Ninguna está hecha para Ender/Creality; la mayoría apuntan a Bambu. Sirven como plantillas para que el usuario escriba su propia skill con el perfil de la Ender 3 V2 Neo.

### Cited Findings
- **HighStormPVP/blender-3d-printing**: 0 estrellas, 10 commits. Contiene SKILL.md, ocho guías de referencia (imprimibilidad, filamento, Bambu Studio, resina, laminado y exportación…) y seis scripts de Blender (unidades, `printability_check.py` con 3D-Print Toolbox y comprobación de manifold con bmesh, estimación de filamento, exportación). Funciona a través de blender-mcp (`execute_blender_code`), no de `blender -b`. Menciona las CLI de Orca, Prusa y Cura. — [GitHub](https://github.com/HighStormPVP/blender-3d-printing)
- **m-esm/3d-print-modeling**: 1 estrella, 23 commits. Modelado paramétrico FDM en Python (`build.py` con un bloque PARAMETERS), capturas headless con Playwright/Chromium y visores Three.js (vistas iso/front/side/top y cortes de sección). Usa trimesh, manifold3d y build123d/CadQuery. Exporta a Bambu a través del proyecto bambu-3mf-export. — [GitHub](https://github.com/m-esm/3d-print-modeling)
- **TrillyD13/3d-printing-skill**: ciclo completo para Bambu (escalado que respeta encajes e imanes, preparación de la impresión, diseño paramétrico, registro de impresiones). Incluye un empaquetado `.skill` para claude.ai. — [GitHub](https://github.com/TrillyD13/3d-printing-skill)
- **Aneesh72658/3d-print-studio-skill**: convierte una idea, una foto o un STL roto en un modelo listo para imprimir y verificado. Explica cómo subirla a claude.ai. — [GitHub](https://github.com/Aneesh72658/3d-print-studio-skill)
- **chriscantey/skill-3d-printing**: contexto de flujos de trabajo, patrones de OpenSCAD y una plantilla de especificaciones de la impresora. — [GitHub](https://github.com/chriscantey/skill-3d-printing)
- **tamer-afifi/3d-print-design-skill**: trabaja con medidas de calibre, imprime primero pruebas de ajuste y genera modelos CadQuery y 3MF. — [GitHub](https://github.com/tamer-afifi/3d-print-design-skill)
- **flowful-ai/cad-skill** (fork en jpurzner): CadQuery a STL, generador Gridfinity, comprobación del volumen de impresión de la A1. — [GitHub](https://github.com/flowful-ai/cad-skill); [fork](https://github.com/jpurzner/cad-skill)
- **cogco1/architectural-model-3d-printing-skill**: maquetas arquitectónicas a FDM (escala, piezas finas, división en partes, uniones, bases). — [GitHub](https://github.com/cogco1/architectural-model-3d-printing-skill)
- **kalmehdar/claude-3d-printing**: OpenSCAD con exportación por color, comprobaciones de malla, una página "Print Bench" de previsualización, skills y agentes. Puede editar STL existentes. — [GitHub](https://github.com/kalmehdar/claude-3d-printing)
- **bsafh/print3d-orcaslicer**: script de Blender → revisión de malla → laminado con la CLI de Orca, con el comando `/print3d`. — [GitHub](https://github.com/bsafh/print3d-orcaslicer)
- Existe también una skill "3d-printing" en skills.lc (ericmilton711) que no verifiqué. — [skills.lc](https://skills.lc/ericmilton711/claude-skills/ericmilton711-claude-skills-claude-skills-project-management-3d-printing-skill-md)
- Otros plugins del directorio de Anthropic: **3D CAD Converter** (ContentaSoft, solo para Windows PC; convierte STEP, IGES, STL, OBJ, 3MF…). — Catálogo de plugins de claude.ai (SearchPlugins, 2026-11-23)

### Inferences
- Ninguna skill es "llave en mano" para Ender 3 V2 Neo + Linux headless. La combinación más útil para inspirarse: bsafh/print3d-orcaslicer (bucle Blender → Orca CLI), m-esm (verificación visual headless) y HighStormPVP (reglas de imprimibilidad). A eso hay que añadir un perfil fijo de la Ender (volumen 220×220×250 mm, que conviene verificar) dentro de SKILL.md.
- Varios READMEs recomiendan leer el código antes de instalar. Las skills ejecutan scripts, así que hay que revisarlas.

### Gaps
- Las fechas de actualización y la actividad real de cada skill no están verificadas.

## 6. Buenas prácticas y experiencias de la comunidad

### Takeaway
No encontré relatos de primera mano verificables (ni en Reddit ni en blogs) sobre Claude e impresión 3D. Lo que hay son READMEs y guías divulgativas. El patrón que se repite: el agente genera o modifica la geometría con código, la verifica (manifold, dimensiones, render visual), lamina por CLI con un perfil fijo y deja la impresión física bajo control humano.

### Cited Findings
- Patrón de bucle cerrado: el agente escribe un script de Blender, la herramienta lo ejecuta, revisa la malla, lamina con Orca y le dice al agente qué corregir. — [bsafh/print3d-orcaslicer](https://github.com/bsafh/print3d-orcaslicer)
- Verificación visual headless después de cada cambio, porque comprobar que la malla es watertight no basta. — [m-esm/3d-print-modeling](https://github.com/m-esm/3d-print-modeling)
- Exportar a escala real en milímetros y laminar por CLI para automatizar. — [HighStormPVP](https://github.com/HighStormPVP/blender-3d-printing)
- Medir con calibre e imprimir primero pruebas de ajuste. — [tamer-afifi](https://github.com/tamer-afifi/3d-print-design-skill)
- Un comando de impresora con éxito no garantiza que la impresión física salga bien. Un modelo de impresora mal configurado puede estampar la boquilla contra la cama (caso Bambu). — [DMontgomery40](https://github.com/DMontgomery40/mcp-3D-printer-server)
- Riesgos de seguridad: el socket de blender-mcp no tiene autenticación y ejecuta Python arbitrario, así que debe quedarse en localhost o detrás de un túnel SSH. — [ahujasid/blender-mcp](https://github.com/ahujasid/blender-mcp)
- Guías divulgativas: [Awesome Claude – Create 3D with Claude](https://awesomeclaude.ai/how-to/create-3d-with-claude); [3dprinteddecor – How to use Claude for 3D printing](https://3dprinteddecor.com/how-to-use-claude-for-3d-printing/); [AWS builders-flash: Cline + Blender MCP (en japonés)](https://aws.amazon.com/jp/builders-flash/202506/cline-blender-mcp-3d-model); [Meshy – guía de Blender MCP](https://www.meshy.ai/tutorials/blender-mcp-guide)
- MCP de Thingiverse para buscar modelos imprimibles. — [glama MCP_thingiverse](https://glama.ai/mcp/servers/gpaul-mcp/MCP_thingiverse)

### Inferences
- Flujo recomendado para el usuario. (1) Sube el STL al repositorio o servidor. (2) Claude analiza el STL con trimesh (dimensiones, watertight) y hace un render de vistas. (3) Aplica la modificación con trimesh/manifold3d o con un script bpy en `blender -b`. (4) Verifica de nuevo y genera un render. (5) Lamina con la CLI de PrusaSlicer u Orca y un perfil fijo de la Ender 3 V2 Neo. (6) El usuario revisa la vista previa del G-code e imprime desde la microSD o con OctoPrint.

### Gaps
- No hay hilos de Reddit (r/3Dprinting, r/ClaudeAI) ni posts de blog con resultados medidos (tasa de éxito, errores típicos). Las búsquedas no devolvieron ninguno.
