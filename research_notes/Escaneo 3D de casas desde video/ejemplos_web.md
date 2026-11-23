# Ejemplos web de casas en 3D, tecnología para embeber escenas y contexto de mercado (noviembre 2026)

Nota metodológica: algunos dominios no se pudieron abrir desde esta sesión por restricciones de red (radiancefields.com, worldlabs.ai, blog.playcanvas.com, developer.playcanvas.com). Para esos sitios, los datos vienen de fragmentos del buscador y deberían verificarse abriendo la página.

## 1. Ejemplos publicados: casas o propiedades convertidas en escena 3D en una web (y si alguno se hizo con Claude o Claude Code)

### Takeaway
Hay ejemplos de producción claros: Zillow SkyTour (exteriores desde dron con Gaussian splatting, julio de 2025), Varjo Teleport, Splat Tour (Barcelona) y los casos de Marble/World Labs. No encontré ninguna web pública de una casa que diga explícitamente que se construyó con Claude o Claude Code. Sí existen skills y conectores de Claude Code que cubren cada paso del proceso (vídeo → splat → visor SparkJS), así que el hueco de "casa en 3D hecha con un agente de IA" sigue libre como elemento diferenciador para un portfolio.

### Cited Findings
**Grandes plataformas y producción**
- Zillow presentó SkyTour en su Summer Launch del 15 de julio de 2025: una vista exterior de la casa desde arriba, guiada por el usuario, como parte de Zillow Showcase — [Zillow press release](https://zillow.mediaroom.com/2025-07-15-Summer-just-got-hotter-Zillow-debuts-five-powerful-new-features); [Zillow Group news](https://www.zillowgroup.com/news/take-home-listings-to-new-heights-with-skytour)
- SkyTour combina Structure-from-Motion y 3D Gaussian Splatting sobre imágenes de dron, y se ve en la app móvil y en la web de Zillow — [Zillow: Capturing SkyTour](https://www.zillow.com/news/how-structured-drone-capture-powers-immersive-3d-skytour); [LiDAR News](https://lidarnews.com/zillow-3d-tours-with-gaussian-splatting/); [GeekWire](https://www.geekwire.com/2025/zillow-uses-drone-imagery-for-new-exterior-3d-tour-feature/)
- Inman (25 de noviembre de 2025) describe cómo SkyTour usa tecnología 3D compleja para simplificar la búsqueda de vivienda — [Inman](https://www.inman.com/2025/11/25/zillows-skytour-uses-complex-3d-tech-to-simplify-home-search/)
- Realtor.com ofrece una vista exterior parecida, pero basada en imágenes de satélite y en el "geospatial splatting" de TopHap (según el resumen del buscador sobre la cobertura de SkyTour) — [Real Estate News](https://www.realestatenews.com/2025/08/21/skytour-gives-buyers-a-birds-eye-view-and-agents-a-new-edge)
- Varjo Teleport tiene una página de "3D property tours": se escanea con el móvil y se comparte por enlace, se embebe en una web o se ve en VR — [Teleport 3D property tours](https://get.teleport.varjo.com/product-pages/3d-property-tours); [Teleport Real Estate](https://get.teleport.varjo.com/solutions/real-estate)

**Servicios y startups de tours con splats**
- Splat Tour (Barcelona) convierte un vídeo de móvil por planta en un tour web con panorámicas 360, plano y un paseo opcional en Gaussian splatting — [Radiance Fields (solo snippet)](https://radiancefields.com/splat-tour-turns-phone-video-into-3d-property-tours)
- Real Horizons ofrece paseos de propiedades en el navegador basados en 3DGS — [Real Horizons](https://real-horizons-landing.pages.dev/features/gaussian-splatting-virtual-tours); [blog](https://real-horizons-landing.pages.dev/blog/gaussian-splatting-for-real-estate)
- The Future 3D vende Gaussian splatting para marketing inmobiliario — [thefuture3d.com](https://www.thefuture3d.com/gaussian-splatting/real-estate/)
- Utsubo tiene un artículo de 2026 sobre Gaussian splatting en inmobiliario comercial (pre-alquiler, tours para inversores, marketing de promociones) — [Utsubo](https://www.utsubo.com/blog/gaussian-splatting-commercial-real-estate)
- ultratour.haus aparece como "coming soon" (opción basada en LiDAR); no está verificado — [ultratour](https://ultratour.pages.dev/)

**World Labs / Marble (mundos generados con IA)**
- Marble es el modelo de mundos comercial de World Labs. Genera entornos 3D persistentes y descargables (en Gaussian splats) — [DeepLearning.AI The Batch](https://www.deeplearning.ai/the-batch/world-labs-makes-its-marble-generative-world-model-public-adds-chisel-editing-tool); [SiliconANGLE, 12 nov 2025](https://siliconangle.com/?p=720746)
- "Spatial Real Estate" es un proyecto comunitario del showcase de World Labs: convierte planos 2D en espacios 3D explorables con World Labs, Gaussian splatting y WebXR — [World Labs showcase (solo snippet)](https://www.worldlabs.ai/labs/showcase/spatial-blueprints)
- Interior AI aparece como la primera app de consumo que integró el modelo de World Labs: rediseñar una habitación con IA y recorrerla en 3D, con virtual staging — [World Labs case studies](https://www.worldlabs.ai/case-studies/2-architecture-design)
- Otros casos de estudio de World Labs relacionados con casas: "Memory House" — [World Labs](https://www.worldlabs.ai/case-studies/memory-house)
- La demo "Third-Person Controller" de World Labs cita Claude Code entre sus herramientas, junto a Marble y Spark 2.0. Es el vínculo explícito más cercano entre Claude Code y escenas splat que encontré — [World Labs third-person controller](https://www.worldlabs.ai/third-person-controller)
- La documentación de Spark dice que con pocas líneas cualquiera que use three.js puede añadir splats, "even by vibe coding" — [sparkjs.dev docs](https://sparkjs.dev/docs/overview/)

**Herramientas para agentes (Claude Code), útiles como prueba de "hecho con IA"**
- `lichtpfad/gaussian-splat-skill`: skill de Claude Code que pasa de vídeo de dron a splat con nerfstudio. Pasos: comprobar el entorno (venv, PyTorch+CUDA, nerfstudio, COLMAP, ffmpeg), analizar la escena con 7 presets, extraer frames, ejecutar COLMAP (`ns-process-data`), entrenar `splatfacto-big` y exportar `.ply`. No indica licencia y tiene 2 commits — [GitHub](https://github.com/lichtpfad/gaussian-splat-skill)
- `shi3z/sparkjs-skill`: skill de Claude Code con el API de SparkJS (formatos, edición SDF, LoD, sistema Dyno, controles, consejos de rendimiento). No incluye demos de casas, solo el butterfly.spz — [GitHub](https://github.com/shi3z/sparkjs-skill)
- Skill "Ruoshui SuperSplat" para Claude Code (limpieza, recorte y conversión para PlayCanvas y la web) — [mcpmarket](https://mcpmarket.com/tools/skills/ruoshui-supersplat)
- MakeSplat ofrece un conector para Claude y ChatGPT: el asistente crea un escaneo 3D a partir de un vídeo y devuelve un splat `.ply` y una malla `.glb` — [makesplat.com/connect](https://makesplat.com/connect)
- Plugin de Claude Code "make-pixel-splats" — [claudepluginhub](https://www.claudepluginhub.com/plugins/codepawl-make-pixel-splats-plugins-make-pixel-splats)
- Ejemplo en X de una app (un contador de calorías, no inmobiliaria) hecha "solo con Claude Code + un par de APIs", con visuales image-to-3D — [X @anshuc](https://x.com/anshuc/status/2069277649655243140)

**Comunidad (Hacker News)**
- Show HN: tour virtual de un parque de 50 años que combina tiles OpenSeadragon con escenas splat de PlayCanvas — [HN 45493583](https://hn.svelte.dev/item/45493583)
- Show HN de un tour splat de una catedral. Críticas en los comentarios: la cámara "on rails" limita la exploración y el soporte móvil era malo; sí había movimiento libre con WASD — [HN 48984254](https://hn.nuxt.dev/item/48984254)
- `sphr`: framework de tours en three.js que combina splats con imágenes 360 — [GitHub wiki](https://github.com/lukehollis/sphr/wiki)

**Investigación**
- HouseTour (arXiv 2510.18054): dataset de más de 1.200 vídeos de tours de casas con reconstrucciones 3D y descripciones; 1.298 vídeos transcritos y 878 escenas 3D reconstruidas — [arXiv](https://arxiv.org/abs/2510.18054v1); [GitHub](https://github.com/GradientSpaces/HouseTour); [web](https://house-tour.github.io)

### Inferences
- Para un portfolio, el mejor argumento es "Zillow ya lo hace (exterior con dron); yo lo hago con interior + exterior a partir de un vídeo de móvil, en una landing propia". La pieza "hecho con Claude Code" puede documentarse con las skills citadas: no hay competencia visible que lo publicite.
- Los comentarios de HN sugieren que, en la landing, conviene combinar una visita guiada (cámara con hotspots) con navegación libre, y probar bien en móvil.

### Gaps
- No encontré ningún post de blog, tweet ni repo concreto de "casa → web 3D hecha con Claude Code". Puede existir en X o Reddit sin indexar.
- No pude verificar URLs de escenas públicas concretas de casas en superspl.at, Polycam Explore, Luma o KIRI: la búsqueda no las devolvió y algunos dominios estaban bloqueados.
- No pude abrir radiancefields.com ni worldlabs.ai para confirmar fechas y detalles (Splat Tour, Spatial Real Estate).

## 2. Visores y librerías web para embeber la escena: formatos, tamaño, móvil, hosting, licencias

### Takeaway
La receta recomendada para noviembre de 2026 es Spark (three.js, MIT, de World Labs) cargando `.spz` o `.sog`, o bien el SuperSplat Viewer de PlayCanvas con SOG (15-20× más pequeño que PLY), sirviendo los archivos estáticos desde Vercel o un CDN. GaussianSplats3D (mkkellogg) ya no está en desarrollo activo y su propio README recomienda Spark. Para mallas `.glb`, model-viewer o three.js.

### Cited Findings
**Spark (sparkjs.dev)**
- Licencia MIT. Lee PLY (también PLY comprimido), SPZ, SPLAT, KSPLAT y SOG. Los ejemplos actuales cargan Spark 2.4.0 (`https://sparkjs.dev/releases/spark/2.4.0/spark.module.js`) con three 0.180.0. Paquete npm `@sparkjsdev/spark` — [Spark README](https://raw.githubusercontent.com/sparkjsdev/spark/main/README.md); [GitHub](https://github.com/sparkjsdev/spark)
- Dice que "renders fast even on low-powered mobile devices" y apunta a más del 98% de soporte de WebGL2 (escritorio, iOS, Android, VR/WebXR) — [Spark README](https://raw.githubusercontent.com/sparkjsdev/spark/main/README.md); [sparkjs.dev](https://sparkjs.dev/)
- Spark 2.0 añadió level-of-detail (LoD) y streaming para escenas grandes — [World Labs blog Spark 2.0](https://worldlabs.ai/blog/spark-2.0); [sparkjs.dev](https://sparkjs.dev/)
- Ejemplo mínimo: import map con three y Spark → `new SparkRenderer({ renderer })` → `new SplatMesh({ url: "...spz" })` → `scene.add(...)`. La documentación recomienda crear el WebGLRenderer sin antialias — [Spark README](https://raw.githubusercontent.com/sparkjsdev/spark/main/README.md); [docs](https://sparkjs.dev/docs/overview/)

**PlayCanvas SuperSplat + SOG**
- SOG (Spatially Ordered Gaussians) sucede a SOGS. Comprime en la GPU con WebGPU, sin CUDA, y según la documentación oficial es 15-20× más pequeño que PLY (compresión con pérdida). Otras fuentes dan cifras distintas (hasta un 95%, o un 60-70% según DeepWiki); la oficial es la más fiable — [PlayCanvas blog: open-sources SOG](https://blog.playcanvas.com/playcanvas-open-sources-sog-format-for-gaussian-splatting/); [PlayCanvas SOG format docs](https://developer.playcanvas.com/user-manual/gaussian-splatting/formats/sog/); [DeepWiki](https://deepwiki.com/playcanvas/supersplat/6.2-supported-file-formats)
- La herramienta SplatTransform (CLI, `@playcanvas/splat-transform`) genera `.sog`, tanto el formato bundled recomendado como la variante meta.json + .webp, y también "Streamed SOG" para carga progresiva — [SplatTransform README](https://unpkg.com/@playcanvas/splat-transform@2.5.2/README.md); [Streamed SOG docs](https://developer.playcanvas.com/user-manual/splat-transform/streamed-sog/)
- SuperSplat permite publicar una escena con enlace y snippet de embed (o hacerla pública en Explore), exportar un visor HTML de un solo archivo o ZIP, o usar el paquete npm `@playcanvas/supersplat-viewer`. Exportar a SOG o al visor standalone requiere WebGPU en el navegador del editor — [SuperSplat import/export](https://developer.playcanvas.com/user-manual/supersplat/editor/import-export/); [supersplat-viewer GitHub](https://github.com/playcanvas/supersplat-viewer)
- SuperSplat 3 (septiembre de 2026) pasa la edición a WebGPU; PlayCanvas también anunció mejoras de rendimiento con WebGPU y streaming — [Digital Production](https://digitalproduction.com/2026/09/18/supersplat-3-moves-editing-to-webgpu/); [PlayCanvas blog](https://blog.playcanvas.com/new-in-supersplat-webgpu-and-streaming-bring-huge-performance-wins)

**Otras librerías**
- GaussianSplats3D (`@mkkellogg/gaussian-splats-3d`): licencia MIT, "no longer in active development", recomienda Spark. Formatos .ply, .splat y .ksplat. Problema conocido: "sub-optimal performance on mobile devices" — [GitHub](https://github.com/mkkellogg/GaussianSplats3D)
- gsplat.js: opción ligera. Una guía de terceros recomienda menos de 1M de splats en móvil — [polyvia3d guide](https://polyvia3d.pages.dev/guides/gaussian-splatting-web-viewer)
- Babylon.js tiene soporte de splats como parte de un motor completo, con más peso; en el foro se discute su futuro — [Babylon forum](https://forum.babylonjs.com/t/the-future-of-gs-in-bbl/60666?page=2)
- three.js tiene splatting nativo para el renderer WebGPU (hilo en el foro) y existe "Gaussian Splat Lite 1.0" (WebGPU, streaming LoD) — [three.js forum](https://discourse.threejs.org/t/native-gaussian-splatting-in-three-js-for-webgpu-renderer/93509); [Gaussian Splat Lite](https://discourse.threejs.org/t/gaussian-splat-lite-1-0-webgpu-streaming-lod-and-depth-rendering-for-three-js/94234)
- Hay benchmarks reproducibles que comparan Spark, GaussianSplats3D, Babylon.js, SuperSplat y three.js r186 (paquete three-blocks-benchmark) — [jsDelivr three-blocks-benchmark](https://www.jsdelivr.com/package/npm/three-blocks-benchmark)
- Investigación: WebSplatter (WebGPU, splatting eficiente entre dispositivos en el navegador) — [arXiv 2602.03207](https://arxiv.org/html/2602.03207v1)

### Inferences
- Receta propuesta para la landing (estática, en Vercel): vídeo → COLMAP/nerfstudio, Polycam/KIRI o MakeSplat → `.ply` → limpieza en SuperSplat → exportar a `.sog` (SplatTransform) o a `.spz` → servir desde `/public` o un CDN → visor Spark con three.js en la página (import map) y hotspots o tour guiado con three.js. Alternativa sin código: el embed de SuperSplat en un iframe.
- Un piso escaneado suele tener entre 1 y 5M de splats. Con SOG (15-20×) un PLY de ~250 MB quedaría en ~12-17 MB. Es un cálculo propio derivado del ratio oficial, no una cifra publicada.
- Para móviles: usar LoD/streaming (Spark 2.x o Streamed SOG) y limitar el número de splats.

### Gaps
- No pude confirmar la licencia del SuperSplat Viewer, del editor ni de SplatTransform (probablemente MIT, como el resto de PlayCanvas, pero sin verificar).
- No encontré cifras de rendimiento móvil comparables y publicadas entre librerías.
- No hay datos concretos sobre `.spz` (formato de Niantic) más allá de que Spark lo soporta.

## 3. Escenas y datasets libres de casas o interiores para una demo o portfolio, con licencias

### Takeaway
No hay ningún dataset "de casas" claramente apto para uso comercial. Mip-NeRF 360 (room, counter, kitchen) tiene una licencia ambigua: el proyecto SMERF lo cita como CC BY 4.0, pero no está confirmado en la página original. ScanNet++ prohíbe el uso comercial. Sketchfab tiene modelos CC BY usables con atribución, pero la licencia varía en cada modelo (algunos son NC, SA o "NoAI"). Lo más seguro para un portfolio comercial es escanear una casa propia o con permiso.

### Cited Findings
- Mip-NeRF 360: la página del proyecto no indica licencia. Un paper dice que el proyecto SMERF declara las escenas como CC BY 4.0 (no confirmado). Un mirror en Hugging Face las etiqueta como MIT, pero es un reempaquetado de terceros — [TIB summary](https://service.tib.eu/ldmservice/dataset/mip-nerf-360-dataset); [arXiv 2404.12547](https://arxiv.org/pdf/2404.12547); [HF nvs-bench/mipnerf360](https://huggingface.co/datasets/nvs-bench/mipnerf360/blob/main/README.md)
- ScanNet++: "only for non-commercial research and educational purposes. Commercial use is strictly prohibited"; los términos también obligan al empleador si es una empresa — [ScanNet++ Terms of Use](https://kaldir.vc.in.tum.de/scannetpp/static/scannetpp-terms-of-use.pdf); [ScanNet++](https://scannetpp.mlsg.cit.tum.de/scannetpp/)
- Sketchfab, licencias mixtas: hay modelos CC Attribution (por ejemplo "House", "studio room" y el escaneo "the porcelain room"), otros CC BY-NC (por ejemplo "American vintage house with interior"), otros CC BY-SA o BY-NC-SA, y algunos llevan la etiqueta "NoAI" — [House](https://sketchfab.com/3d-models/house-d3f85975cfad4b24bf14175f4ff3269d); [studio room](https://sketchfab.com/3d-models/studio-room-64efce2484ea4d3aac3661210b2cf944); [the porcelain room](https://sketchfab.com/3d-models/the-porcelain-room-407a75f63a624494a61da40f5cd07bd0); [American vintage house](https://sketchfab.com/3d-models/american-vintage-house-with-interior-5a9e087fbd3a4ae79b4c51d6279f0466); [vintage living room](https://sketchfab.com/3d-models/vintage-living-room-3ac5d18326e24a1ab47279466e4e00ad); [cabin interior](https://sketchfab.com/3d-models/cabin-interior-981ec01231754313ae47127eccb62eec)
- HouseTour (1.298 vídeos y 878 escenas 3D de tours de casas) es un dataset de investigación, con la licencia sin verificar — [GitHub](https://github.com/GradientSpaces/HouseTour)
- Escenas demo de Spark (por ejemplo `https://sparkjs.dev/assets/splats/butterfly.spz`) sirven para probar el pipeline, pero no son casas — [sparkjs-skill](https://github.com/shi3z/sparkjs-skill)

### Inferences
- Para una demo comercial, lo más prudente es (a) escanear una vivienda propia o de un cliente con permiso por escrito, (b) generar un mundo con Marble (revisando sus términos de uso comercial) o (c) usar un modelo de Sketchfab CC BY con atribución visible.
- Las escenas "room", "counter" y "kitchen" de Mip-NeRF 360 sirven para pruebas internas, pero conviene no usarlas como portfolio comercial sin confirmar la licencia.

### Gaps
- No verifiqué las licencias de Zip-NeRF, Tanks and Temples ni Polycam Explore (cada escena tiene la configuración que elige su autor).
- No pude confirmar en la web de SMERF la declaración CC BY 4.0.
- No verifiqué los términos de uso comercial de los mundos generados con Marble.

## 4. Mercado: quién vende el servicio, precios y diferenciadores

### Takeaway
El listón es Matterport: suscripción de unos 14-355 USD al mes según fuentes de terceros, más hosting por espacio y add-ons. Los fotógrafos cobran unos 150-800 USD por tour en EE. UU. Para Gaussian splatting profesional hay una referencia de "desde 2.250 USD" (The Future 3D), y una fuente estima que los freelancers ganan 300-650 USD por escaneo residencial. Las cifras independientes son escasas; casi todas vienen de blogs de vendedores.

### Cited Findings
- Matterport: planes Free, Starter, Professional, Business y Enterprise, con precios configurados según el número de espacios activos y facturación anual — [matterport.com/plans](https://matterport.com/plans)
- Precios reportados por terceros: Starter 14 USD/mes, Professional 69 USD/mes y Business 355 USD/mes según PricingSaaS; SofaBrain da Starter ~10 USD/mes (5 espacios), Pro ~69 USD (25 espacios) y Business ~309 USD — [PricingSaaS](https://pricingsaas.com/companies/matterport); [SofaBrain](https://sofabrain.com/learn/matterport-pricing)
- Add-ons por espacio según SofaBrain: hosting ~20 USD/mes por espacio activo, plano ~50 USD, MatterPak ~100 USD, nube de puntos E57 ~150 USD. Son cifras de terceros — [SofaBrain](https://sofabrain.com/learn/matterport-pricing); [Travvir](https://travvir.com/blog/en/matterport-pricing-explained)
- Posible cambio en octubre de 2026: PricingSaaS indica que Matterport eliminó Starter y Business y reconvirtió Professional en una escala por espacios. Contradice otras fuentes de noviembre de 2026, así que hay que verificarlo — [PricingSaaS diff 2026W42](https://pricingsaas.com/companies/matterport/diffs/2026W42)
- Precio de un tour para el cliente: 150-500 USD con un fotógrafo local (unos 500 USD de media con profesionales); los escaneos tipo Matterport cuestan 300-800+ USD o 200-1.500 USD más ~40 USD/mes de hosting; los retainers con agencias tienen descuentos del 20-40% — [Travvir 2026](https://travvir.com/blog/en/real-estate-virtual-tour-cost); [CloudPano](https://www.cloudpano.com/blog/virtual-tour-cost-pricing-guide)
- Gaussian splatting profesional para inmobiliario: "desde 2.250 USD", con un precio 1,5× el de la fotogrametría — [The Future 3D](https://www.thefuture3d.com/gaussian-splatting/real-estate/)
- "A $200 tool is undercutting $3,500 real estate tour services": freelancers con móvil más Polycam, Luma o KIRI ganarían 300-650 USD por escaneo residencial. Los portales MLS todavía no han estandarizado los tours con splats — [GadgetReview](https://www.gadgetreview.com/?p=411348)
- Varjo Teleport: ~30 USD/mes con 15 escaneos (modelo anterior). Un borrador de precios por créditos fija Pro en 29,99 €/mes (~5 capturas medianas al mes, créditos extra a 0,60 €). Enterprise se cobra por número de imágenes — [Road to VR](https://roadtovr.com/varjo-teleport-3d-model-scanning-app-release/); [Teleport pricing draft](https://get.teleport.varjo.com/drafts/pricing-v3); [Teleport pricing](https://get.teleport.varjo.com/pricing)
- Polycam: los planes diferencian "Embed with watermark" de "Embed with custom branding". El precio de Pro varía según la fuente (19,99 USD/mes o 199,99 USD/año; ~26,99 USD/mes; 12 USD/mes en G2) — [poly.cam/pricing](https://poly.cam/pricing); [Polycam Basic plan](https://poly.cam/pricing/basic-plan); [G2](https://www.g2.com/products/polycam/reviews)
- Polycam publica su propia lista de alternativas a Matterport para equipos pequeños (2026) — [Polycam blog](https://poly.cam/blog/best-matterport-alternatives-for-small-teams-creators-in-2026)

### Inferences
- Posicionamiento posible: "tour fotorrealista con Gaussian splatting a partir de un vídeo de móvil, alojado en una landing propia del inmueble o del Airbnb, sin suscripción mensual de Matterport". Un precio de entrada entre 300 y 800 € por vivienda estaría en la franja de los freelancers y Matterport. Un paquete premium (exterior con dron + interior + landing a medida) podría acercarse al rango "desde 2.250 USD". Es una estimación propia.
- Diferenciadores frente a Matterport: no necesita cámara específica (vale un móvil o un dron), da más realismo (reflejos, vegetación, exteriores), no tiene cuota recurrente por espacio y el resultado es una web propia. Desventajas: falta de estandarización en los MLS y mediciones o planos menos maduros.

### Gaps
- No hay encuestas independientes de precios de servicios con Gaussian splatting en 2026, ni datos del mercado español o europeo.
- No pude confirmar en la página oficial los precios actuales de Matterport (no publica cifras).
- No encontré precios públicos de Splat Tour, Real Horizons ni de Zillow Showcase.
