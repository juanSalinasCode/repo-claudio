# Escaneo 3D de casas (interior + exterior) desde video: métodos y herramientas (estado a noviembre 2026)

> Nota metodológica: investigación hecha el 2026-11-23 con WebSearch. WebFetch estaba bloqueado por la red del contenedor para la mayoría de dominios (kiriengine.app, docs.worldlabs.ai, orbitimagery.com fallaron con ENOTFOUND), así que muchas cifras vienen de resúmenes de búsqueda y no de lectura completa de la página. Los puntos marcados **[conocimiento previo]** provienen del conocimiento del modelo (corte jun-2026) y no se re-verificaron en esta sesión; la URL es la del repo/página oficial conocida. Precios: verificar siempre la página oficial antes de presupuestar.

## 1. Técnicas: qué existe, cuáles funcionan desde video plano, y cómo extraer fotogramas

### Takeaway
Para una casa completa el pipeline práctico en 2026 sigue siendo: video -> fotogramas nítidos (ffmpeg + filtro de nitidez) -> poses (COLMAP/GLOMAP o, cada vez más, un modelo feed-forward tipo VGGT/MapAnything/VGGT-Ω) -> optimización 3DGS/2DGS (gsplat, Postshot, etc.) para el tour visual, y fotogrametría/LiDAR (RealityScan, OpenMVS) si se necesitan mallas/medidas. Los modelos feed-forward (VGGT, MASt3R, MapAnything, Depth Anything 3, AnySplat y sucesores 2026) ya dan geometría métrica en segundos, pero a ~512 px y con límites de número de vistas; para escenas largas (casa entera) aparecen variantes "long-context"/streaming en 2026 pero son investigación, no producto. Los generadores tipo World Labs Marble inventan contenido: no sirven como reconstrucción fiel de una vivienda real.

### Cited Findings
**Feed-forward (sin optimización por escena)**
- MapAnything (Meta, sep-2025): reconstrucción métrica feed-forward "universal"; desacopla poses y profundidad en componentes invariantes a escala + factores de escala globales; sin optimización en tiempo de test — [GitHub facebookresearch/map-anything](https://github.com/facebookresearch/map-anything); [arXiv 2509.13414](https://arxiv.org/pdf/2509.13414)
- Depth Anything 3 (nov-2025): acepta imagen monocular, video o multivista; tiene variante métrica; su evaluación F1 usa umbral de 0,05 m — [arXiv 2511.10647](https://arxiv.org/html/2511.10647v1)
- VGGT-Ω ("Scaling feed-forward 3D reconstruction", arXiv 2605.15195, 2026) es el sucesor de VGGT; entrada a 512 px (MapAnything 518 px, DA3 504 px) — [arXiv 2605.15195](https://arxiv.org/pdf/2605.15195) (solo vía resumen de búsqueda; no se pudo leer el paper)
- π³ citado como arquitectura unificada que infiere geometría multivista, cámaras y profundidad — [resultado de búsqueda, MapAnything paper](https://map-anything.github.io/assets/MapAnything.pdf)
- Para secuencias largas (relevante para una casa entera) hay trabajos 2026: MetricTrail (reconstrucción métrica en streaming para secuencias largas, arXiv 2611.07555) — [arXiv](https://arxiv.org/pdf/2611.07555); LonGaussian (feed-forward Gaussian de contexto largo, arXiv 2610.23250) — [arXiv](https://arxiv.org/pdf/2610.23250); ReCoSplat (feed-forward online por render-and-compare, 2603.09968) — [arXiv](https://arxiv.org/pdf/2603.09968); OF³GS on-the-fly feed-forward 3DGS desde imágenes sin pose — [arXiv 2606.03254](https://arxiv.org/pdf/2606.03254); DeltaSplat (pose-free, refinamiento iterativo) — [arXiv 2610.09853](https://arxiv.org/pdf/2610.09853); FlexSplat (BMVC 2026, front-end VGGT, orientado a objetos) — [GitHub](https://github.com/amir-sbg/FlexSplat)
- **[conocimiento previo]** VGGT (Meta/Oxford, CVPR 2025 best paper) predice cámaras, profundidad y nube de puntos desde 1 a cientos de vistas en un pase; necesita GPU CUDA, la memoria crece con nº de fotogramas (en el README, ~decenas de GB para ~200 fotogramas en H100) — [GitHub facebookresearch/vggt](https://github.com/facebookresearch/vggt)
- **[conocimiento previo]** MASt3R / DUSt3R (Naver) y MASt3R-SfM: emparejamiento denso + alineamiento global; funcionan con imágenes sin pose; licencia CC BY-NC-SA (no comercial) — [GitHub naver/mast3r](https://github.com/naver/mast3r)
- **[conocimiento previo]** AnySplat (2025): 3DGS feed-forward desde imágenes sin pose/calibración (colecciones casuales) — [arXiv 2505.23716](https://arxiv.org/abs/2505.23716)

**Optimización por escena (3DGS/2DGS/NeRF)**
- **[conocimiento previo]** 3DGS original (INRIA, graphdeco-inria/gaussian-splatting): requiere GPU CUDA, el README recomendaba 24 GB VRAM para calidad de paper; licencia no comercial de INRIA — [GitHub](https://github.com/graphdeco-inria/gaussian-splatting)
- **[conocimiento previo]** gsplat (nerfstudio-project): librería CUDA Apache-2.0, menos memoria y más rápida que la implementación original; nerfstudio (Apache-2.0) integra splatfacto/nerfacto y `ns-process-data video` (extrae fotogramas + COLMAP) — [GitHub gsplat](https://github.com/nerfstudio-project/gsplat); [nerfstudio](https://github.com/nerfstudio-project/nerfstudio)
- OpenSplat (AGPL) entrena en CUDA, ROCm, Metal o **solo CPU (~100x más lento)**; necesita puntos dispersos de COLMAP/OpenSfM/ODM/nerfstudio (no admite inicialización aleatoria); ~2 GB de VRAM por millón de gaussianas — [GitHub pierotofy/OpenSplat](https://github.com/pierotofy/opensplat)
- CLM y GS-Scale (2025) descargan gaussianas a memoria del host para entrenar escenas grandes en GPUs de consumo — [arXiv 2511.04951](https://arxiv.org/html/2511.04951v1); [arXiv 2509.15645](https://arxiv.org/html/2509.15645v1)
- Métodos por escena típicos: "de unos minutos (3DGS) a ~1 h" por escena en una GPU — [arXiv 2505.18342](https://arxiv.org/pdf/2505.18342)
- Para geometría de interiores: 2DGS-Room (2DGS guiado por semillas con restricciones geométricas) — [arXiv 2412.03428](https://arxiv.org/pdf/2412.03428); DN-Splatter (priors de profundidad y normales; mallado) — [arXiv 2403.17822](https://arxiv.org/pdf/2403.17822); LighthouseGS (capturas móviles tipo panorama en interiores) — [arXiv 2507.06109](https://arxiv.org/html/2507.06109v2)

**Fotogrametría clásica**
- RealityScan 2.0 = RealityCapture renombrado (Epic) — [realityscan.com](https://www.realityscan.com/news/realityscan-20-new-release-brings-powerful-new-features-to-a-rebranded-realitycapture)
- **[conocimiento previo]** COLMAP (BSD; SfM+MVS; MVS denso requiere CUDA, SfM corre en CPU), GLOMAP (SfM global, mucho más rápido), OpenMVS (MVS/malla/textura, CPU), Meshroom/AliceVision (MPL2; depth maps requieren CUDA) — [COLMAP](https://github.com/colmap/colmap); [GLOMAP](https://github.com/colmap/glomap); [OpenMVS](https://github.com/cdcseacave/openMVS); [Meshroom](https://github.com/alicevision/Meshroom)

**Generadores de mundos**
- World Labs Marble: modelo comercial de "world model" lanzado nov-2025; acepta texto, imágenes y video vía World API; genera mundos (splats) y exporta malla GLB — [SiliconANGLE](https://siliconangle.com/2025/11/12/world-labs-launches-marble-commercial-world-model-generating-entire-virtual-environments/); [World Labs blog](https://worldlabs.ai/blog/announcing-the-world-api); Marble 1.1 con auto-expansión — [NYU Shanghai RITS](https://rits.shanghai.nyu.edu/ai/world-labs-releases-marble-1-1-auto-expanding-3d-world-generation)

**Extracción de fotogramas**
- Guía: extraer a ~2–3 fps para capturas a paso de caminar, con `mpdecimate` para eliminar casi duplicados (muchos fotogramas redundantes ralentizan COLMAP) — [polyvia3d guide](https://polyvia3d.pages.dev/guides/gaussian-splatting-from-video)
- Un gist de preparación 3DGS usa `--fps 1` como ejemplo — [gist hyperlogic](https://gist.github.com/hyperlogic/3fac47498cc715cc8162040fe9b70dba)
- `sharp-frames` (Reflct, pip, requiere ffmpeg): modo "best-n" (N fotogramas más nítidos con separación mínima; ejemplo 300) y modo "batched" (el más nítido de cada lote) — [GitHub reflct/sharp-frames-python](https://github.com/reflct/sharp-frames-python); [Radiance Fields](https://radiancefields.com/reflct-sharp-frame-selector)
- Otras herramientas: sharp-frame-extractor (cansik), framegrabber — [ecosyste.ms](https://awesome.ecosyste.ms/projects/github.com%2Fcansik%2Fsharp-frame-extractor); [GitHub Spatial-Explorer/framegrabber](https://github.com/Spatial-Explorer/framegrabber)

### Inferences
- Pipeline recomendado para el agente: `ffmpeg -i in.mp4 -vf "fps=3,mpdecimate,scale=1920:-2" f_%05d.jpg` -> puntuación de nitidez (varianza del Laplaciano con OpenCV, CPU, barato) -> quedarse con el más nítido por ventana -> 200–600 fotogramas por planta/zona, más para casa entera (orden de 1.000+ en total). Esto es síntesis propia; ninguna fuente da un número universal.
- Para casa completa, dividir en "chunks" (exterior dron, exterior a pie, cada planta) con fotogramas de solape en las transiciones (puertas), registrar por separado y fusionar, es más robusto que un solo modelo; los feed-forward actuales están limitados en nº de vistas y resolución (~512 px).
- Licencias: implementación INRIA y MASt3R/DUSt3R son no comerciales; para producto usar gsplat/nerfstudio (Apache-2.0), COLMAP/GLOMAP (BSD), OpenMVS (AGPL) y verificar licencias de pesos de VGGT/MapAnything (no verificado aquí).

### Gaps
- No se pudo leer VGGT-Ω, MetricTrail ni LonGaussian: se desconoce nº máximo de fotogramas, VRAM y licencia.
- No se verificó la licencia actual de pesos de VGGT/MapAnything/DA3 (algunas versiones tenían pesos comerciales y otras no).
- No se encontró benchmark directo feed-forward vs COLMAP+3DGS en casas completas.

## 2. CPU-only vs GPU; cloud GPU y coste por reconstrucción

### Takeaway
En el contenedor (4 CPU, 15 GB RAM, sin GPU) solo es viable: extracción/selección de fotogramas, SfM disperso (COLMAP/GLOMAP en CPU, horas para ~1.000 imágenes), OpenMVS en CPU (lento), y OpenSplat en CPU (~100x más lento: impracticable para casa entera). Entrenamiento 3DGS y modelos feed-forward requieren GPU CUDA; lo razonable es delegar a GPU en la nube (Modal/RunPod) o a un servicio con API (KIRI, World Labs, Polycam/Teleport). Coste de cómputo bruto: del orden de céntimos a pocos dólares por reconstrucción.

### Cited Findings
- OpenSplat CPU-only ~100x más lento que GPU — [GitHub OpenSplat README](https://github.com/pierotofy/OpenSplat/blob/main/README.md)
- ~2 GB VRAM por millón de gaussianas (estimación OpenSplat) — [GitHub OpenSplat](https://github.com/pierotofy/opensplat)
- Modal (facturación por segundo, snapshots oct–nov 2026): H100 ≈ $3,95/h ($0,001097/s), L4 ≈ $0,80/h, B200 ≈ $6,25/h; Modal cobra CPU y RAM aparte — [tech-insider 2026](https://tech-insider.org/gpu-cloud-providers-serverless-gpu-pricing-modal-runpod-nebius-2026/); [dupple Modal pricing](https://dupple.com/learn/modal-pricing)
- RunPod: H100 PCIe $2,89/h Secure / desde $1,99/h Community; H100 SXM $4,39/h Secure / desde $2,69/h Community; facturación por segundo — [RunPod pricing](https://www.runpod.io/gpu-cloud/pricing). L4 en RunPod: fuentes en conflicto ($0,48/h serverless según [computeprices](https://computeprices.com/compare/modal-vs-runpod) vs grupo 24 GB a $1,10/h en la página de RunPod)
- Guía 2026 para desplegar 3DGS en GPU cloud: la facturación por minuto hace económico separar preprocesado (CPU) y entrenamiento (GPU) — [Spheron blog](https://www.spheron.network/blog/deploy-3d-gaussian-splatting-gpu-cloud/)
- **[conocimiento previo]** 3DGS original: 24 GB VRAM recomendados; gsplat reduce memoria notablemente (README de gsplat) — [graphdeco-inria](https://github.com/graphdeco-inria/gaussian-splatting); [gsplat](https://github.com/nerfstudio-project/gsplat)

### Inferences
- Estimación propia (no fuente): entrenamiento gsplat 30k iteraciones de una zona de ~300–600 imágenes ≈ 15–40 min en L4/A10/4090 -> ~$0,30–$1 en Modal L4 o RunPod; casa completa con varios chunks y una GPU de 24–48 GB, ~$1–5 de cómputo. VGGT/feed-forward con cientos de fotogramas necesita 40–80 GB (A100/H100), pero corre en segundos-minutos -> <$1.
- Mínimo práctico de VRAM: 12–16 GB para escenas pequeñas con gsplat; 24 GB cómodo; 48–80 GB para feed-forward con muchas vistas o escenas grandes sin chunking.
- HF Spaces (ZeroGPU) y Replicate sirven para demos, pero tienen límites de tiempo por llamada; no se encontraron precios por reconstrucción.

### Gaps
- No se encontraron tiempos medidos de COLMAP en CPU ni benchmarks de gsplat con VRAM/tiempo por nº de imágenes en 2026.
- Precios de Replicate y HF Spaces para modelos de splatting no encontrados.

## 3. Servicios/apps hospedados: precio, API, formatos, licencia

### Takeaway
Para un agente, las opciones con API real y pago por uso son KIRI Engine (≈$1 por escaneo 3DGS/fotogrametría, recarga mínima 500 créditos) y World Labs World API (≈$1,3–1,7 por mundo, pero genera, no reconstruye fielmente). Luma abandonó su API de captura; Polycam/Scaniverse/Teleport/Matterport son esencialmente apps sin API pública documentada (Polycam: ambigua; Matterport tiene SDK/API de plataforma pero captura propia). Postshot es software de escritorio Windows/GPU (CLI solo en plan Studio). RealityScan es gratis bajo $1M de ingresos.

### Cited Findings
- **KIRI Engine API**: 3DGS Scan = 1 crédito; cada llamada 1 crédito independientemente del método; crédito = $1; recarga mínima 500 créditos — [KIRI API](https://www.kiriengine.app/api) (vía resumen de búsqueda; fetch bloqueado). Docs con endpoint "Video Upload" — [docs.kiriengine.app](https://docs.kiriengine.app/category/3dgs-scan). App: Pro desbloquea 3DGS; KIRI 3.13 añadió "High Quality Gaussian Splatting" — [Radiance Fields](https://radiancefields.com/kiri-engine-3-13-unveils-high-quality-gaussian-splatting)
- **World Labs (Marble)**: API por créditos prepagados, $1 = 1.250 créditos, mínimo $5, no caducan; créditos de app ≠ créditos API; coste por mundo marble-1.1-plus mediana $1,280, media $1,714; puede añadir 0–1.500 créditos para mundos grandes; export malla GLB HQ = 3.500 créditos ($2,80); tres variantes de modelo — [docs.worldlabs.ai/api/pricing](https://docs.worldlabs.ai/api/pricing) (vía resumen). App: Standard $20/mes, Pro $35/mes (lanzamiento 2025) — [SiliconANGLE](https://siliconangle.com/2025/11/12/world-labs-launches-marble-commercial-world-model-generating-entire-virtual-environments/)
- **Luma AI**: el cliente Python de la API de captura avisa que ya no se mantiene — [GitHub lumaapi-python](https://github.com/lumalabs/lumaapi-python); Luma cierra Flythroughs el 1-ene-2026 — [Radiance Fields](https://radiancefields.com/luma-ai-to-sunset-flythroughs-on-january-1-2026); subidas de radiance fields suspendidas — [Radiance Fields](https://radiancefields.com/radiance-field-uploads-suspended-on-luma-ai); app iOS Luma 3D Capture v1.3.14 (ene-2026), Android retirada — [App Store](https://apps.apple.com/MX/app/id1615849914). **Luma ya no es opción para el producto.**
- **Polycam**: plan Basic ~$12,5/mes (anual) / $30 mensual con capturas y Gaussian Splats ilimitados; planes Free/Basic/Business/Enterprise — [poly.cam basic plan](https://poly.cam/fr-fr/basic-plan); [poly.cam/llms.txt](https://poly.cam/llms.txt). Polycam dice Basic $12,50/mes a Business $34/mes con exportaciones ilimitadas — [Polycam vs Matterport](https://poly.cam/blog/polycam-vs-matterport-2026). API: contradictorio (GetApp dice que no hay API; SoftwareAdvice la lista) — [GetApp](https://www.getapp.com/augmented-reality-software/a/polycam); [SoftwareAdvice](https://www.softwareadvice.com/product/515621-Polycam)
- **Matterport**: plan gratuito; captura con cámaras 360 compatibles o con iOS/Android — [matterport.com/plans](https://matterport.com/plans); Pro $19/mes, Pro Plus $33/mes, Teams $125/mes (según Polycam, competidor) — [Polycam blog](https://poly.cam/blog/best-matterport-alternatives-for-small-teams-creators-in-2026); cámara Pro3 desde ~$5.995 — [thefuture3d](https://www.thefuture3d.com/blog-0/2026/3/2/matterport-pricing-guide-2026/); los precios han cambiado varias veces en dos años (misma fuente)
- **Varjo Teleport**: "Export splat models and fly-through videos"; pago por captura desde $30, licencia anual por puesto, opción on-premise; 5 escaneos gratis — [Teleport pricing](https://get.teleport.varjo.com/pricing); export PLY — [UploadVR](https://www.uploadvr.com/varjo-teleport-launch/); Teleport 2.0 ~$30/mes con cámaras mirrorless y Vision Pro — [Auganix](https://www.auganix.org/vr-news-varjo-teleport-2-0/); términos permiten usar el contenido subido para mejorar su tecnología — [useblurry](https://www.useblurry.com/read/best-gaussian-splat-hosting-options-august-2026)
- **Postshot (Jawset)**: Free no comercial, con marca de agua, sin exportar splats; Indie ~26 €/mes o 204 €/año (uso comercial, export PLY/SPZ); Studio ~59 €/mes o 468 €/año (HDR 16/32-bit, CLI) — [Radiance Fields Postshot](https://radiancefields.com/platforms/postshot); [SplatMart](https://www.splatmart.com/blog/best-3dgs-software-2026)
- **RealityScan 2.0**: gratis para estudiantes, educadores y empresas con ingresos brutos anuales < $1M; suscripción por encima — [realityscan.com](https://www.realityscan.com/news/realityscan-20-new-release-brings-powerful-new-features-to-a-rebranded-realitycapture); [licencia](https://www.realityscan.com/license); ~$1.250/usuario/año por encima del umbral (tercero, no oficial) — [metashape-la](https://www.metashape-la.com/en/agisoft-metashape-vs-realitycapture-complete-comparison-2026/)
- **Scaniverse (Niantic Spatial)**: página de precios de Niantic Spatial existe — [nianticspatial.com/pricing](https://nianticspatial.com/pricing); **[conocimiento previo]** Scaniverse es gratis, procesa en el dispositivo y Niantic creó/liberó el formato SPZ (MIT) — [GitHub nianticlabs/spz](https://github.com/nianticlabs/spz)
- Herramientas recomendadas por PlayCanvas para crear splats (Postshot, etc.) — [PlayCanvas docs](https://developer.playcanvas.com/user-manual/gaussian-splatting/creating/recommended-tools/)
- **[conocimiento previo]** Formatos: .ply (3DGS estándar), .splat (antimatter15, compacto sin SH), .spz (Niantic, ~10x más pequeño), .sog (PlayCanvas/SuperSplat "Spatially Ordered Gaussians", comprimido para web), glTF con extensión KHR_gaussian_splatting en desarrollo en Khronos; mallas GLB/OBJ desde fotogrametría — [PlayCanvas SuperSplat](https://github.com/playcanvas/supersplat)

### Inferences
- Para un producto operado por un agente: (a) KIRI API como backend "llave en mano" (barato, ~$1/escena) o (b) pipeline propio en Modal/RunPod con gsplat + visor web (SuperSplat/PlayCanvas, Spark) exportando .sog/.spz — esta opción da control de licencia y calidad.
- Matterport sigue siendo el estándar del sector inmobiliario (tours + planos + medidas), pero usa su propio ecosistema; un producto basado en splats compite en realismo visual y exterior (dron), no en medidas.

### Gaps
- Precio actual de Scaniverse/Niantic Spatial y licencia comercial de sus exports: no verificados.
- Si KIRI API acepta video directo o solo fotos (el endpoint "Video Upload" describe subir un photoset): no aclarado.
- Si Polycam tiene API pública en 2026: contradictorio.
- Términos de licencia comercial de Marble para mundos generados: no verificados.

## 4. Precisión dimensional y problemas típicos

### Takeaway
3DGS estándar es de calidad "visualización" (error geométrico del orden de centímetros a ~decímetros, sin escala absoluta a menos que se añada); para medidas fiables se usa LiDAR o fotogrametría con escala/GCPs. Variantes georreferenciadas/con priors mejoran a ~1,5 cm horizontal en exteriores aéreos. Paredes blancas, ventanas y reflejos, y la conexión interior-exterior son los principales puntos de fallo.

### Cited Findings
- Error geométrico medio ~7,82 cm (σ 11,49 cm) para splats estándar vs LiDAR — cifra de vendedor repetida en varias páginas, sin estudio primario trazable — [thefuture3d](https://www.thefuture3d.com/gaussian-splatting/)
- Splatting georreferenciado: 1,5 cm RMSE horizontal, 5,3 cm RMSE vertical (citando paper MDPI Drones 2026); 3DGS estándar no es de grado topográfico — [aerocartwright](https://aerocartwright.com/library/gaussian-splatting-drone-operators/)
- 3DGS semántico "medible" con supervisión de profundidad para inspección de edificios (2026) — [arXiv 2610.13143](https://arxiv.org/pdf/2610.13143)
- Caso real inmobiliario: COLMAP solo registró 2 de 304 fotogramas de dron en el primer intento; registro completo tras corregir la captura — [Orbit Imagery](https://orbitimagery.com/blog/gaussian-splatting-finally-gives-real-estate-exterior-3d-tour-its-been-missing/)
- Paredes sin textura: SfM no genera puntos fiables -> inicialización mala, geometría errónea y artefactos — [CMU MSCV project](https://mscvprojects.ri.cmu.edu/2024team2/methods/)
- Reflejos/efectos dependientes de vista generan artefactos; datasets interiores difíciles por baja textura, reflejos e iluminación variable; se comparan COLMAP vs SuperPoint-SuperGlue/LoFTR — [arXiv 2609.36969](https://arxiv.org/pdf/2609.36969); reflexiones guiadas por lo visible — [arXiv 2610.13757](https://arxiv.org/pdf/2610.13757)
- Movimiento dominado por rotación y baseline estrecho dificultan poses en interiores sin textura — [LighthouseGS](https://arxiv.org/html/2507.06109v2)
- Depth Anything 3 evalúa reconstrucción con F1 a 0,05 m (indica el orden de precisión que se mide en feed-forward) — [arXiv 2511.10647](https://arxiv.org/html/2511.10647v1)
- Drones en interiores para evaluación de propiedades (investigación) — [arXiv 2508.01965](https://arxiv.org/pdf/2508.01965); OpenFlyScan: reconstrucción aérea guiada por calidad para drones de consumo — [arXiv 2609.24253](https://arxiv.org/pdf/2609.24253)

### Inferences
- Para medidas en el producto: escalar con una referencia conocida (cinta métrica / marcador ArUco / altura de puerta estándar) o usar modelos métricos (MapAnything, DA3 metric) y declarar tolerancias de ±2–5 % en interiores; no prometer precisión topográfica.
- Interior-exterior: el puente más fiable es grabar un recorrido continuo cruzando la puerta (con la puerta abierta, dentro->fuera y fuera->dentro) y bajar el dron a altura de persona cerca de la fachada para solapar con la captura a pie.

### Gaps
- No hay estudio primario 2025-2026 encontrado con error dimensional medido de splats en casas completas desde video de móvil.
- Precisión de Matterport phone capture vs Pro3 no verificada en esta sesión.

## 5. Buenas prácticas de captura para una casa completa

### Takeaway
Capturar con traslación (caminar, no girar sobre sí mismo), velocidad lenta, exposición bloqueada, buena luz uniforme, solape fuerte en transiciones (puertas/escaleras), y para exterior combinar órbitas de dron a varias alturas con un recorrido a pie que conecte con la entrada. 360° acelera interiores; dron no aplica dentro.

### Cited Findings
- Guía de herramientas de captura 2026: dron no relevante en interiores; cámaras 360° recomendadas para habitaciones (rápidas) — [ar-go.co](https://ar-go.co/blog/gaussian-splatting-capture-tools/)
- Movimiento suave de recorrido (walkthrough) funciona especialmente bien para interiores (inmobiliario, construcción), mejor que waypoints discretos — [aerocartwright](https://aerocartwright.com/library/gaussian-splatting-drone-operators/)
- Evitar capturas rotacionales/baseline estrecho en interiores — [LighthouseGS](https://arxiv.org/html/2507.06109v2)
- Teleport 2.0 admite cámaras mirrorless (mejor calidad de imagen que el móvil) — [Auganix](https://www.auganix.org/vr-news-varjo-teleport-2-0/)

### Inferences
- Protocolo sugerido (síntesis): 4K 30/60 fps, obturación rápida (≥1/120) para evitar motion blur, exposición/balance de blancos bloqueados, todas las luces encendidas y persianas consistentes; por habitación, perímetro a ~1 m de la pared mirando al centro + pase por el centro mirando a las paredes, a 2 alturas (pecho y cerca del techo/suelo); en paredes blancas incluir siempre bordes, esquinas y muebles en el encuadre; ventanas en ángulo oblicuo. Exterior: órbitas de dron a ~45° y ~20 m, más órbita baja; recorrido a pie alrededor de la casa; tramo continuo exterior->entrada->interior.
- Separar el procesado en chunks y fusionar con fotogramas compartidos en transiciones.

### Gaps
- No se encontraron protocolos oficiales (de Polycam/KIRI/Matterport) leídos en detalle para casa completa; las recomendaciones arriba son síntesis.
