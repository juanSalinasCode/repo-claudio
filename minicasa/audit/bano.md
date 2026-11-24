# Zona BAÑO + ALTILLO

Archivos: `scripts/zones/bano.py`, `scripts/zones/altillo.py`, texturas `tex/bano_granero.jpg`, `tex/bano_marmol.jpg`,
`tex/bano_madera.jpg` (recortadas de f0110, f0140 y f0144). Build: `/opt/3d/minicasa/work/bano`.
Láminas finales: `audit/bano/{granero2,bano2,bano3,altillo2}_audit.jpg`.

## Distribución reconstruida (f0100–f0165)
- **Pared XL (izquierda):** inodoro junto al tabique, de espaldas a XL y mirando a +x (f0136/f0138); portarrollos
  de pie cromado entre el inodoro y la ducha (f0156).
- **Ducha neo-angular** en la esquina (XL, L): plato pentagonal blanco de 0,92 m por lado, retornos fijos de 0,30 m
  y puerta en la cara a 45°. La bisagra está en el extremo delantero (lado XL) y el pomo en el extremo del fondo;
  la puerta abre hacia afuera (+x, −y). Perfiles cromados, monocomando negro y brazo con flor en la pared XL, y un
  canasto colgante negro con frascos.
- **Pared XR (derecha):** desde el tabique hay un estante y toallero negro de metal con toallas, y después un
  vanitorio abierto de madera de 1,30 m que llega hasta el rincón del fondo: tapa maciza, faldones, 4 patas y un
  estante bajo con toallas. Encima está la bacha negra rectangular de apoyo, ubicada justo antes de la ventana,
  con grifería negra de pared (pico y 2 llaves en cruz). Arriba van el espejo grande de marco negro (0,90 m) y la
  barra negra con 5 portalámparas y lamparitas. La ventana del baño es `RIGHT_WINS[1]`; su marco interior y su
  alféizar pasan a blanco, como en el video.
- **Pared del fondo:** estante de madera abierto con 5 estantes, a XR−0,38, con 2 ganchos negros.
- Piso con la textura real de mármol. Las paredes del baño pasan a "Panel blanco baño" liso, porque en el video
  son paneles lisos y el machimbre solo aparece en el cielorraso.
- **Puerta granero:** una hoja de 3 tablas verticales de pino claro con la textura real. Tiene 2 herrajes negros
  tipo strap con rueda, cuelga del riel plano bajo la cenefa y desliza hacia −x. La hoja solapa 10 cm solo del
  lado izquierdo, así que se sigue viendo la jamba derecha (f0110). Se agregaron el contramarco de pino del vano,
  la guía de piso y los soportes del riel. El "Riel granero" de estructura se borra y se recrea en bano.py con el
  mismo nombre.
- **Altillo:** colchón blanco de 1,40 × 1,95 m contra XL, al ras del borde del altillo, con acolchado blanco,
  edredón tostado amontonado y 2 almohadas al fondo. Se quitó la "Baranda altillo": en el video no hay baranda.

Todo se calcula a partir de XL, XR, L, BATH_Y, LOFT_Z, BATH_DOOR y RIGHT_WINS. Los bordes del tabique y de la
viga se leen de los objetos de estructura. Los interactivos se mantienen con sus nombres, grupos y pivotes:
Puerta granero, Inodoro tapa, Mampara ducha, Grifo ducha y Agua ducha, Canilla baño y Agua baño.
Hay unos 2,8k triángulos en el baño y 0,9k en el altillo.

## Auditoría (3 ciclos con audit/cameras.json)
- Ciclo 1: se corrió con las constantes viejas (BATH_Y 4,40) y el baño quedaba detrás de las cámaras.
- Ciclo 2: con BATH_Y ≈ 3,94, que coincide con lo que fijó Medidas, la ducha y el estante calzan.
- Ciclo 3: se agrandó el vanitorio, la bacha pasó bajo el espejo y se ajustó el tamaño del espejo.

Resultado: en bano3 y bano4 los perfiles de la ducha y el estante del fondo coinciden en unos 5 px a 360 px de
ancho. En bano2 coinciden el orden y las alturas de estante, ventana, espejo, bacha y vanitorio, y en granero2
coinciden la hoja y el riel.

## Pendiente / para Medidas (estructura.py)
- **Falta una ventana en la pared XL del baño, sobre el inodoro** (f0136, f0158). Mide unos 0,45 m de ancho, va
  de y ≈ BATH_Y+0,15 a BATH_Y+0,60 y de z ≈ 1,20 a 2,00, con marco blanco.
- La ventana XR del baño (5,10–5,70) se ve más angosta en f0144, de unos 0,45 m. El espejo real es un poco más
  grande que la ventana.
- La cara del tabique del lado baño sigue con `white_planks`. En el video es un panel blanco liso.
- En Workbench el cielorraso del baño se ve oscuro por la iluminación STUDIO, no por el material.
- El piso del altillo en el video es de madera teñida más oscura (~#736A60). Ahora es de pino claro.
- La auditoría usa la puerta granero cerrada, así que bano1 (f0137, con la puerta abierta) no sirve como
  comparación.
