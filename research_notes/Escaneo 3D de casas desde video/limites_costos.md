# Límites de uso de Claude y costos en tokens para el proyecto "casa en video → escena 3D + landing page" (a 23-nov-2026)

Notas de investigación. Fuentes consultadas el 2026-11-23. Las páginas de ayuda de Anthropic no muestran fecha exacta ("Updated over N weeks ago"), así que las fechas son aproximadas.

## 1. Planes de Claude, precios y cómo funcionan los límites (5 horas, semanal, uso extra)

### Takeaway
En noviembre de 2026 los planes individuales son Pro ($20), Max ($100, 5x Pro; antes "Max 5x") y Ultra ($200, 10x Pro por semana; es el antiguo "Max 20x", renombrado hacia el 30-oct-2026). Hay una ventana de sesión de 5 horas (salvo en Ultra con cuenta verificada) y un límite semanal compartido entre todos los modelos, más un límite semanal aparte para Fable. Claude Code (también las sesiones en la nube de claude.ai/code) consume del mismo bolsillo que el chat. Pasado el límite, los "usage credits" (antes "extra usage") se cobran a precio de API. Anthropic ya no publica cifras de horas ni de tokens por plan.

### Cited Findings
**Precios de los planes (claude.com/pricing, consultado nov-2026)**
- Free $0 (uso "limitado", sin Claude Code); Pro $20/mes ($17/mes anual, $200 por adelantado); Max $100/mes, "5x Pro usage"; Ultra $200/mes, "10x Pro usage weekly, with no 5-hour limit"; Team Standard $25/asiento al mes ($20 anual), "más uso que Pro"; Team Premium $125 ($100 anual), 5x el uso de un asiento estándar; Enterprise $20/asiento anual con mínimo de 20 asientos, "seat price + usage at API rates". Todos los de pago incluyen Claude Code. — [Claude pricing](https://claude.com/pricing)
- Nota: la página de precios etiqueta Ultra como "20x" pero describe su uso como "10x Pro weekly"; la etiqueta parece un resto del nombre antiguo. — [Claude pricing](https://claude.com/pricing)

**Ultra / cambio de nombre**
- "El plan Max 20x ahora se llama Ultra". Los suscriptores pasan automáticamente, sin cambio de precio. Cuesta $200/mes (web), solo mensual. Incluye "10 times the Pro plan's usage every week". Las cuentas verificadas no tienen límite de 5 horas y las no verificadas tienen uno temporal. Hay un límite semanal para todos los modelos y otro aparte para Fable, y pueden aplicarse "weekly and monthly caps". Incluye créditos mensuales de API (sin importe indicado). — [Support: Ultra plan](https://support.claude.com/en/articles/17728952)
- Medios sitúan el cambio de nombre en torno al 30-oct-2026; el antiguo Max 5x pasa a llamarse simplemente "Max" ($100). — [mixed-news](https://mixed-news.com/en/?p=38997); [letsdatascience](https://letsdatascience.com/news/anthropic-removes-five-hour-claude-limit-for-verified-ultra-56c3c5dc) (secundarias; resumidas en el buscador, no leídas completas)

**Cómo funcionan los límites**
- Los planes de pago tienen un "five-hour session limit" (en Ajustes > Uso aparece "Current session" con el tiempo restante). Los "Weekly limits" se reinician "for all models, and for Fable (if included in your plan)". El artículo no da cifras de mensajes ni de tokens. Lo que más consume: la longitud de los mensajes, los adjuntos, la longitud de la conversación, el uso de herramientas, el modelo, el nivel de esfuerzo y las tareas de varios pasos. El contenido en caché "counts less against your limits", pero la caché expira con la inactividad. — [Support: Usage and rate limits](https://support.claude.com/en/articles/9797557-usage-and-rate-limits)
- En Team/Enterprise, el uso de Claude Code sale de una asignación por asiento que se reinicia "on a rolling five-hour window and a weekly window" y se comparte con el chat y Cowork. Los mensajes "You've hit your session limit / weekly limit" son comunes a todos los modelos, así que cambiar de modelo con `/model` no los evita. Con los mensajes específicos "Opus limit"/"Sonnet limit", cambiar de familia sí permite seguir. — [Claude Code docs: Manage costs](https://code.claude.com/docs/en/costs)
- Enterprise por consumo: sin límites fijos, se cobra según lo consumido. — [Support: Usage and rate limits](https://support.claude.com/en/articles/9797557-usage-and-rate-limits)
- El uso de claude.ai, Desktop y Claude Code sale del mismo pool. — [resultado de búsqueda que resume el artículo de mejores prácticas de soporte](https://support.claude.com/en/collections/18031876-usage-and-limits)

**Promoción y ajuste de los límites semanales de Claude Code en 2026**
- "From May 13, 2026 through September 13, 2026, your weekly usage limit in Claude Code was 50% higher" (Pro, Max, Team y Enterprise legacy por asiento). Los límites de 5 h no cambiaron. **Desde el 14-sep-2026 los límites semanales quedan un 25 % por encima de los anteriores a la promoción** (Pro, Max, Ultra, Team y Enterprise por asiento). Anthropic dice que planea "return weekly limits to their original levels", pero de momento mantiene parte del aumento. — [Support: promoción mayo-sep 2026](https://support.claude.com/en/articles/15910845-claude-code-may-july-2026-weekly-limits-promotion)
- Conflicto: un fragmento indexado anterior (y el slug de la URL, "may-july") decía que la promoción iba hasta el 19-jul-2026. La versión actual de la página dice 13-sep. Seguramente se prolongó. — mismo artículo / [resultado de búsqueda](https://support.claude.com/en/articles/15910845)
- DataCamp (secundaria) afirma que en mayo de 2026 Anthropic "doubled subscription usage limits" y eliminó las reducciones en horas punta, y que no hay una asignación semanal aparte para Opus. No lo verifiqué en una fuente primaria. — [DataCamp](https://www.datacamp.com/tutorial/claude-code-usage-limits)

**Cifras históricas (2025, probablemente obsoletas)**
- Agosto 2025, al introducirse los límites semanales: Pro "40–80 h de Sonnet 4/semana"; Max 5x "140–280 h de Sonnet 4 y 15–35 h de Opus 4"; Max 20x "240–480 h de Sonnet 4 y 24–40 h de Opus 4". — [TechCrunch, 28-jul-2025](https://techcrunch.com/2025/07/28/anthropic-unveils-new-rate-limits-to-curb-claude-code-power-users/)
- Una guía de terceros de oct-2026 indica que hoy no se publican esos múltiplos en horas. — (resumen del buscador; ver [allthings.how](https://allthings.how/claude-code-usage-limits-explained-pro-max-and-weekly-caps/))

**Uso extra / "usage credits"**
- Disponibles en Pro, Max y Ultra (Team y Enterprise tienen su propio artículo). "Usage credits are billed at standard API rates". Se cobran aparte de la suscripción. Permiten fijar un tope mensual o "unlimited", recarga automática (solo web) y alertas. Los créditos mensuales de API incluidos en Max, Ultra y Team **no** sirven como usage credits en Claude, Claude Code o Cowork. — [Support: Extra usage / usage credits](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans)
- En Claude Code, `/usage-credits` abre Ajustes > Uso; `/usage` muestra las barras del plan, el desglose por skills, subagentes y MCP, y recomendaciones. Desde v2.1.234 se puede esperar al reinicio y continuar automáticamente. — [Claude Code docs: Manage costs](https://code.claude.com/docs/en/costs)

### Inferences
- Para un usuario individual, la pregunta práctica es "¿cuántas sesiones de 5 h y qué fracción semanal gasta el proyecto?". Como Anthropic no publica tokens por plan, la única medición fiable es mirar `/usage` (o el bloque `rate_limit_info` de la sesión) antes y después de una sesión representativa y extrapolar.
- Ultra con verificación elimina la ventana de 5 h, lo que conviene a una sesión larga que orquesta trabajos externos. Para un proyecto de este tamaño, Pro o Max probablemente bastan (ver sección 3).

### Gaps
- No encontré ninguna cifra oficial actual de tokens, mensajes u horas por plan (Pro, Max o Ultra) para la ventana de 5 h ni para la semanal. No hay que inventarla.
- Tamaño del límite semanal de Fable e importe de los créditos de API incluidos en Max/Ultra: no publicados.
- La página "About Max plan usage" (11014257) devuelve 404, así que no se pudo verificar texto oficial específico de Max tras el cambio de nombre.

## 2. Precios de API por token (familias 2026), coste de imágenes y caché

### Takeaway
Opus 5.5 cuesta $4/$20 por MTok (entrada/salida) y Sonnet 5.5 $2/$10, ambos con lecturas de caché a 0.05x ($0.20 y $0.10/MTok). Haiku 5.5 cuesta $0.10/$0.50 (por debajo de 100k tokens de prompt). Fable 5.2 es el nivel superior ($8/$40). Las imágenes cuestan ⌈ancho/28⌉×⌈alto/28⌉ tokens. Un fotograma 1080p en un modelo ≥4.7 (alta resolución) son ~2.691 tokens, unos $0.011 en Opus 5.5 la primera vez.

### Cited Findings
**Precios por millón de tokens (base input / caché 5 min / caché 1 h / lectura de caché / output)**
- Claude Fable 5.2: $8 / $10 / $16 / $0.20 / $40. Mythos 5.2 tiene el mismo precio (acceso limitado).
- Claude Fable 5.1 y 5: $10 / $12.50 / $20 / $0.25 (5.1) o $1 (5) / $50.
- **Claude Opus 5.5: $4 / $5 / $8 / $0.20 / $20.** Opus 5, 4.8, 4.7, 4.6 y 4.5: $5 / $6.25 / $10 / $0.50 / $25.
- **Claude Sonnet 5.5: $2 / $2.50 / $4 / $0.10 / $10.** Sonnet 5: $2 / $2.50 / $4 / $0.20 / $10; el precio "introductorio" pasó a ser el estándar y la subida a $3/$15 prevista para el 1-sep-2026 no se aplicó. Sonnet 4.6 y 4.5: $3 / $3.75 / $6 / $0.30 / $15.
- **Claude Haiku 5.5**: $0.10 / $0.125 / $0.20 / $0.01 / $0.50 con prompts ≤100k tokens, y $0.50 / $0.625 / $1 / $0.05 / $2.50 con prompts >100k. Haiku 4.5: $1 / $1.25 / $2 / $0.10 / $5.
- Todo lo anterior procede de: — [Claude API pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- Multiplicadores de caché: escritura 5 min 1.25x, escritura 1 h 2x, lectura 0.1x en general, pero **0.05x en Opus 5.5 y Sonnet 5.5** y 0.025x en Fable/Mythos 5.1 y 5.2. Batch: -50 %. Contexto de 1M tokens sin recargo en modelos ≥4.6 (excepto Haiku 5.5). Modo rápido: Opus 5.5 $8/$40. Residencia de datos en EE. UU.: 1.1x. — [Claude API pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- Los modelos 4.7 y posteriores usan un tokenizador nuevo que produce "approximately 30% more tokens for the same text". — [Claude API pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- Los tokens de razonamiento (thinking) se facturan como salida. Opus 5.5, Sonnet 5.5, Haiku 5.5 y Fable siempre usan razonamiento extendido, que se controla con `/effort`. — [Claude Code docs: Manage costs](https://code.claude.com/docs/en/costs)
- Herramientas: web search $10 por 1.000 búsquedas; web fetch sin recargo (una página media de 10 kB son ~2.500 tokens); la definición de la herramienta bash añade 325 tokens en modelos ≥4.7. — [Claude API pricing](https://platform.claude.com/docs/en/about-claude/pricing)

**Imágenes (visión)**
- Fórmula actual: "Each patch is a 28×28-pixel block… An image costs ⌈width/28⌉ × ⌈height/28⌉ visual tokens." Es decir, ≈ ancho×alto/784, lo que sustituye a la regla antigua de ancho×alto/750. — [Vision docs](https://platform.claude.com/docs/en/build-with-claude/vision)
- Niveles: **alta resolución (Claude 4.7 y posteriores, incluidos Opus 5.5 y Sonnet 5.5): lado largo máx. 2.576 px y 4.784 tokens**. Estándar (resto): 1.568 px y 1.568 tokens. Las imágenes mayores se reducen. — [Vision docs](https://platform.claude.com/docs/en/build-with-claude/vision)
- Tabla de ejemplos: 1000×1000 → 1.296 tokens; 1920×1080 → 2.691 tokens en alta resolución (1.560 en estándar, reducida a 1456×819); 3840×2160 → 4.784 tokens en alta resolución (reducida a 2576×1449). "At Claude Opus 5.5's $4 USD per million (high-resolution tier), the same [1000×1000] image costs about $5.18 USD per thousand and the 4K image about $19.14 USD per thousand." — [Vision docs](https://platform.claude.com/docs/en/build-with-claude/vision)
- Límites: 20 imágenes por mensaje en claude.ai; 600 por petición en la API (100 en modelos de 200k). Si una petición lleva más de 20 imágenes, rige un límite más estricto por imagen, así que hay que mantener ≤3.000 px. Máx. 8000×8000 px y 10 MB. — [Vision docs](https://platform.claude.com/docs/en/build-with-claude/vision)
- "High-resolution images can use up to roughly three times more visual tokens… downsample images before sending to control token costs." — [Vision docs](https://platform.claude.com/docs/en/build-with-claude/vision)

### Inferences (cálculos propios con los precios citados)
- Un fotograma 1920×1080 en Opus 5.5 son 2.691 tokens: ≈$0.0108 como entrada nueva, ≈$0.0135 al escribirlo en caché de 5 min, y ≈$0.00054 cada vez que se relee desde caché en peticiones posteriores. En Sonnet 5.5 cuesta la mitad.
- 30 fotogramas 1080p ≈ 81k tokens, unos $0.40 al escribirlos en caché con Opus 5.5. Si se quedan en el contexto principal durante 50 peticiones más, se releen ≈4M tokens de caché ≈ $0.81. En total, ≈$1.2 de API equivalente. Poco en dólares, pero ocupa ~8 % de una ventana de 1M y encarece cada turno siguiente.
- Para reducirlo: bajar los fotogramas a ~1000 px de lado largo (~1.300 tokens) o hacer una hoja de contactos (un mosaico de 4×4 miniaturas en una sola imagen ≤2.576 px = máx. 4.784 tokens), o revisarlos en un subagente (quizá con Haiku 5.5) que devuelva solo un resumen en texto.

### Gaps
- No verifiqué si las sesiones con suscripción descuentan del límite con la misma proporción relativa entre modelos que los precios de API (Opus 2x Sonnet). Es razonable suponerlo, pero Anthropic no lo publica.

## 3. Consumo típico de tokens de Claude Code y estimación para este proyecto; coste de GPU externo

### Takeaway
Según Anthropic, Claude Code cuesta de media ~$13 por desarrollador y día activo ($150–250/mes, con el 90 % por debajo de $30/día) en despliegues empresariales. Para este proyecto (orquestar ffmpeg y una API de splats, revisar algunos fotogramas y construir una landing con un visor 3D), una estimación realista es de **~4–8 sesiones y ~10–40M tokens en total, casi todos lecturas de caché, ≈ $10–40 de API equivalente con Opus 5.5 (≈ la mitad con Sonnet 5.5)**. Eso cabe holgadamente en el límite semanal de Max y probablemente también en Pro, aunque en Pro puede agotar 1–3 ventanas de 5 h. El entrenamiento del splat se hace en GPU externa y no consume tokens de Claude (unos pocos dólares por escena en GPU alquilada, o suscripciones de $15–18/mes en apps).

### Cited Findings
**Datos oficiales de Anthropic**
- "Across enterprise deployments, the average cost is around $13 per developer per active day and $150-250 per developer per month, with costs remaining below $30 per active day for 90% of users." — [Claude Code docs: Manage costs](https://code.claude.com/docs/en/costs)
- Ejemplo oficial de `/usage`: "claude-sonnet-4-6: 1.2k input, 5.3k output, 940.0k cache read, 50.0k cache write ($0.55)". Ilustra que la mayor parte de los tokens son lecturas de caché. — [Claude Code docs: Manage costs](https://code.claude.com/docs/en/costs)
- Por qué crece el uso en sesiones largas: cada petición reenvía la conversación completa y cada uso de herramienta es otra petición; los fallos de caché tras pausas reprocesan todo el contexto; los subagentes, las tareas programadas y la compactación suman consumo. Recomendaciones: `/clear` entre tareas, Sonnet para la mayoría del código, subagentes para salidas verbosas, hooks que filtren logs. Los equipos de agentes gastan "~7x more tokens". — [Claude Code docs: Manage costs](https://code.claude.com/docs/en/costs)
- Ejemplo oficial de Managed Agents con Opus 5.5: una sesión de 1 h con 50k tokens de entrada y 15k de salida cuesta $0.58 (o $0.43 con caché). Es un caso ilustrativo y pequeño, no una media. — [Claude API pricing](https://platform.claude.com/docs/en/about-claude/pricing)

**Anécdotas (secundarias, resumidas por el buscador; no leídas completas porque dev.to no era accesible desde esta sesión)**
- Tareas simples (un componente o un endpoint): ~10k–20k tokens en total. Un desarrollador contó 50 sesiones y 3,8M tokens en 30 días (abr–may 2026), ~76k por sesión. Un modelo teórico de sesión media plantea ~40 llamadas con ~90k tokens de contexto cada una (~3,6M procesados). Un análisis de 38 sesiones sumó 42,9M tokens, sobre todo relecturas del historial. Firecrawl estima que se cargan 20–30k tokens antes del primer mensaje. — [Coralogix](https://coralogix.com/blog/where-did-all-my-claude-code-tokens-go); [dev.to (38 sesiones)](https://dev.to/lsvishaal/i-analyzed-38-claude-code-sessions-only-06-of-tokens-were-actual-code-output-56li); [Firecrawl](https://www.firecrawl.dev/blog/claude-code-token-efficiency); [dev.to (coste por sesión)](https://dev.to/dylan_brown_4c803aefcfe51/how-much-does-claude-code-actually-cost-per-session-i-did-the-math-1lk7)
- Un usuario de Indie Hackers dice haber consumido el equivalente a ~$30.983 en tokens de API en un mes con el plan de $200. Es un caso extremo y solo se conoce por el título. — [Indie Hackers](https://indiehackers.com/post/i-used-30-983-of-ai-tokens-last-month-in-claude-code-on-200-mo-plan-3337a369a6)

**GPU / servicios externos (no se facturan en tokens de Claude)**
- RunPod (instantáneas de jul–oct 2026, varían): H100 PCIe ~$1.99/h (Community) o $2.89/h (Secure); H100 SXM ~$2.69–3.99/h; RTX 4090 ~$0.34–0.89/h; almacenamiento en volumen de red $0.07/GB al mes. — [RunPod pricing](https://www.runpod.io/pricing); [Spheron: RunPod H100 2026](https://www.spheron.network/blog/runpod-h100-pricing-2026/); [Thunder Compute](https://www.thundercompute.com/blog/Runpod-pricing-vs-thunder-compute)
- Apps de escaneo / splats: Polycam ~$17.99/mes o $99.99/año; KIRI Engine ~$14.99/mes o $59.99/año, con un plan básico gratis (3DMag, jul-2026; las fuentes no coinciden). La app de captura de Luma parece abandonada (análisis de oct-2026). — [3DMag](https://www.3dmag.com/3d-scanners/best-3d-scanning-apps/); [KIRI pricing](https://www.kiriengine.app/pricing); [Polycam pricing](https://poly.cam/pricing); [Radiance Fields: alternativas a Luma](https://radiancefields.com/luma-ai-alternatives)

### Inferences (estimación propia; hipótesis explícitas)
Hipótesis: el modelo es Opus 5.5 ($4 entrada, $5 escritura en caché de 5 min, $0.20 lectura de caché, $20 salida), la caché acierta un ~90–95 % y el razonamiento está en esfuerzo medio o alto.

| Fase | Peticiones | Contexto medio | Lecturas de caché | Escrituras de caché | Salida (incl. thinking) | ≈ Coste Opus 5.5 |
|---|---|---|---|---|---|---|
| Orquestar el pipeline (ffmpeg, llamadas a la API de splats, scripts y depuración) | 60–120 | 60–100k | 4–10M | 0.3–0.6M | 60–150k | $3–8 |
| Revisar fotogramas (20–40 imágenes, ver sección 2) | 10–30 | +50–110k | 1–4M | 0.1–0.15M | 10–30k | $1–2 |
| Landing page HTML/JS con visor 3D (p. ej. three.js o visor de splats), iteraciones | 100–250 | 60–120k | 6–25M | 0.4–1.2M | 100–300k | $5–20 |
| Total del proyecto | ~200–400 | | **~11–40M** | ~1–2M | ~0.2–0.5M | **≈ $10–35** (Sonnet 5.5 ≈ $5–18) |

- Para comparar: $10–35 equivale a ~1–3 "días activos" medios de Anthropic ($13/día). Max ($100) y Ultra ($200) están pensados para un uso diario muy superior, así que el proyecto debería ocupar una fracción pequeña del límite semanal de Max (orden de un 5–20 %, sin poder confirmarlo con cifras oficiales). En Pro ($20) es probable que alguna ventana de 5 h se agote en las fases intensas, sobre todo con Opus, y que el proyecto use una parte significativa del límite semanal. Conviene usar Sonnet para la iteración de la web, `/clear` entre fases y subagentes para revisar imágenes, o tener usage credits (precio de API) como colchón.
- Las sesiones en la nube (claude.ai/code) consumen del mismo pool de la suscripción. El tiempo de CPU del contenedor no se cobra en tokens; los comandos largos (ffmpeg, esperar a la API) solo cuestan tokens por su salida en la terminal. Hay que limitar esa salida (p. ej. `-loglevel error` en ffmpeg y redirigir logs a archivos).
- Si el entrenamiento de 3DGS dura ~0,5–2 h en una GPU de clase 4090 o H100 a $0.34–3.99/h, la GPU cuesta ~$0.2–8 por escena. El orden de magnitud es comparable o menor que el de los tokens; el cálculo es mío porque ninguna fuente da tiempos para escenas de casas.
- El mejor método de medición en este proyecto es anotar el porcentaje de `/usage` (o `get_session` → `rate_limit_info`) al empezar y al terminar cada fase.

### Gaps
- No hay estudios rigurosos de tokens por "landing page con visor 3D". Las anécdotas son heterogéneas y algunas fuentes (dev.to) no se pudieron leer completas por restricciones de red de la sesión (dev.to tendría que estar permitido en la configuración de red).
- No hay equivalencia oficial entre dólares de API y porcentaje del límite semanal de cada plan. La traducción "$X → % del límite de Max" es una inferencia aproximada.
- Los tiempos de entrenamiento de splats para escenas interiores de casa completas y los precios oficiales actuales de Polycam, Luma y KIRI no se verificaron en páginas primarias.
