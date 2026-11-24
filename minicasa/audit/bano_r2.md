# Baño, altillo y puertas — 2ª ronda (choques)

Build: `/opt/3d/minicasa/work/bano2` · `collisions.py` cerrado y con los interactivos abiertos (`abierto.blend`,
simulado aplicando rot/slide de Puerta granero, Mampara ducha, Inodoro tapa, Puerta entrada, Puerta mosquitero).
Láminas: `audit/bano_r2/` (bano1, bano2, granero1, planta). No toqué core.py ni estructura.py.

## Resultado
- Choques en mis zonas: de **49 a 4**, y los 4 que quedan son con muebles de otras zonas (ver abajo). Entre objetos de mis zonas no queda ninguno.
- Estados abiertos: ninguno choca con nada, salvo la puerta granero abierta contra `Silla plegada 1` (ver abajo).

## Cambios
- **Ducha** (`bano.py`): los vidrios fijos y la hoja de la mampara van a tope con sus perfiles (superior, inferior, U de pared y parantes de bisagra/manija), con 1 mm de luz; ningún perfil cruza el vidrio. Los perfiles se despegaron 1–2 mm de las paredes y del plato.
- **Canasto**: los frascos apoyan 3 mm sobre el estante.
- **Toallas**: las del vanitorio y las del toallero quedan 3 mm sobre sus estantes. El estante superior del toallero pasó a 1,20 m y la barandita a 0,80 m.
- **Inodoro**: la taza se acortó (escala 1,1; profundidad total ≈0,67 m) y la bisagra de la tapa quedó 2,5 cm delante de la mochila. La tapa abre −92° (antes −95°) y ya no atraviesa la mochila.
- **Espejo y barra de luces**: arrancan después del toallero (y≈4,45), sobre el vanitorio.
- **Marco puerta baño**: jambas y dintel forran el hueco BATH_DOOR, con tapajuntas en las dos caras del tabique; no lo atraviesa.
- **Puerta granero**:
  - la hoja quedó a 0,6 cm del riel (y 3,764–3,802) y su borde derecho coincide con la jamba (x −0,43…0,27);
  - el riel y los bulones están dentro de x ≥ XL (pedido de exterior);
  - abre −0,555 m, hasta 1,5 cm de la pared XL, y deja ≈55 cm de paso libre. La pared no permite correrla más.
  - la guía de piso cae dentro del recorrido.
- **Puerta de entrada** (T=0,20):
  - el contramarco forra el vano y los tapajuntas apoyan en las caras exterior e interior de la pared;
  - del lado izquierdo los tapajuntas son angostos (1,2 cm afuera, 2,2 cm adentro), porque la ventana del frente está a 8,5 cm;
  - el umbral quedó dentro del vano;
  - la hoja libra las jambas. El pivote se corrió 6 mm (a d0+0,018) y abre 92°, así libra el contramarco.
- **Farol**: bajó para quedar bajo la tapajunta (BELT_Z). Su vidrio quedó dentro de la caja, en 2 paños.
- **Araña**: las lamparitas son ahora el 2º material del objeto `Araña`; se eliminó el objeto `Araña lamparitas` (nadie lo referenciaba).
- **Altillo**:
  - el colchón (0,20 m) arranca detrás de la cenefa (y≈3,885) y va hasta L−0,04;
  - encima, el acolchado de 5 cm, que cae por los costados;
  - sobre el acolchado, 3 bultos elipsoidales de edredón que no se pisan y una manta doblada a los pies;
  - las almohadas apoyan en el colchón;
  - todo apilado con 2–3 mm de luz. Altura máxima ≈2,84 m (techo 3,12).

## Pendiente: choques con otras zonas (medidas)
1. **Sillón (living) contra la puerta granero**: el sillón llega a y=3,80 (pata .001 y 3,693–3,756; manta hasta 3,81). La hoja ocupa y 3,764–3,802, en x 0,155–0,27. Hace falta que el sillón termine en **y ≤ 3,75** (y la manta también).
2. **Sillas plegadas / mesa (living)**: `Silla plegada 1` (y 3,74–3,80, x −0,88…−0,46) choca con la puerta abierta (x −0,985…−0,285). Hay que moverla a **y ≤ 3,75** o fuera de ese tramo. `Mesa plegable` (x −0,90…−0,30, y 3,80–3,86) se mete 7 cm en el hueco del baño (empieza en x −0,37) y cruza el tapajunta: debería terminar en **x ≤ −0,43**. Además, una puerta abierta sobre −x tapa el tablero eléctrico, la mesa y las sillas: conviene confirmarlo con el video.
3. **Larguero escalera (escalera)**: llega a y=4,154, cruza el tabique (3,86–3,94) y entra 21 cm en el baño, donde choca con el toallero (x 0,918–0,953). Tiene que terminar en **y ≤ 3,85**.
4. **Estante alto entrada (cocina)**: rozaba el tapajunta interior derecho de la puerta. Lo angosté a 3,5 cm y ya no aparece.

## Proporciones (audit.py)
Revisé las láminas bano1, bano2, granero1 y altillo1:
- **ducha**: coincide en ancho, alto y diagonal;
- **vanitorio, bacha, espejo y barra de luces**: alineados con la foto;
- **puerta granero**: herrajes y riel coinciden.

La lámina altillo1 tiene un desfase de cámara general, que no viene de mi zona.
