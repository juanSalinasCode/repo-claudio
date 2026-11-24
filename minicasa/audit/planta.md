# Planta interior: presupuesto de paredes y choques (2ª ronda)

Zonas: `cocina.py`, `living.py`, `escalera.py`. Build: `/opt/3d/minicasa/work/planta`.

## Cómo medí
- Usé la nube COLMAP alineada (`work/medidas`, clase `House`), filtrada por color y por altura junto a cada pared, más rayos de las cámaras proyectados sobre el piso o sobre planos (`House.hit`).
- Mueble negro: frente en x 0.62–0.67, puntos en y 0.72–1.56 y tapa menta a z≈0.90. En f0091 el anafe termina en y≈1.65.
- Sillón (f0104): la pata delantera está en el piso en (x 0.31, y 2.55). La nube turquesa va de y 2.6 a 3.8.
- Heladera (f0096): en el plano x=−0.36 los laterales quedan en y 2.25 y 2.79, y la altura es ≈1.5.
- Secuencia comprobada en f0013, f0034, f0091, f0096, f0104 y f0187.

## Presupuesto de cada pared (constantes en `cocina.py`, que usan `living.py` y `escalera.py`)

### Pared −x (cocina), de 0 a PY=3.86

| y0 | y1 | elemento | constante |
|---:|---:|---|---|
| 0.00 | 0.33 | hueco de escoba | `KY0` |
| 0.33 | 0.78 | cajonera de 3 (`Cajon 1-3`) | `YA1` |
| 0.78 | 1.46 | puerta doble | `YB0` |
| 1.46 | 2.20 | puerta doble bajo la bacha (bacha 1.56–2.10, ventana 1.51–2.21) | `KY1` |
| 2.20 | 2.28 | luz por el marco y el alféizar de la ventana (llegan a 2.27) | |
| 2.28 | 2.83 | heladera (0.55 × 0.60 × 1.47; frente de puertas en x −0.305) | `FRIDGE_Y0/Y1` |
| 2.83 | 3.51 | paso libre | |
| 3.51 | 3.71 | sillas plegadas y mesa plegada, contra el tabique (x −0.98…−0.38) | `STORE_Y1` |
| 3.71 | 3.86 | barrido de la hoja granero (3.764–3.802) y tabique | `PY` |

### Pared +x (living), de 0 a PY=3.86

| y0 | y1 | elemento | constante |
|---:|---:|---|---|
| 0.00 | 0.80 | barrido de la puerta de entrada | |
| 0.80 | 1.62 | mueble negro de cubos 2×3 (fondo 0.32, alto 0.86) | `CUBE_Y0/Y1` |
| 1.62 | 2.55 | pie de la escalera: el larguero apoya en 1.96–2.04 y las pedadas 1–2 van delante del sillón, bajo la ventana 1.50–2.21 | |
| 2.55 | 3.75 | sillón (x 0.30–0.90, respaldo 0.74, apoyabrazos 0.62) | `SOFA_Y0/Y1`, `SOFA_X0/X1` |
| 3.75 | 3.86 | hoja granero y tabique | |
| 2.11 | 3.84 | escalera, en altura: 8 pedadas de 0.28 con z = 0.32 + 0.26·i; avance 0.21; llega al altillo (2.40) | `STAIR_Y1` |

Pasillo libre: 0.60 m entre el frente de la heladera (−0.305) y el sillón (0.30). Entre la mesada (−0.365) y el mueble negro (0.67) quedan 1.03 m.

## Cambios
- **Bajo mesada**: ahora es una carcasa (base, fondo, laterales, divisores y travesaños) con hueco en la cajonera y bajo la bacha. La mesada tiene el hueco de la bacha. Saqué `Bacha hueco` y la cajonera trasera, que no entraba en el presupuesto. La canilla y los jabones quedan fuera del alféizar.
- **Mueble de cubos**: estantes y cubículos con el mismo cálculo, y los canastos apoyados sin cruzar nada. Saqué `Repisa ventana`, que duplicaba el alféizar. El florero y el cartel LIFE van sobre el alféizar y el mandala delante, junto al termostato.
- **Heladera**: el interior es un revestimiento hueco por compartimento (antes era un bloque macizo). El canto curvo de la puerta ya no se mete en el cuerpo. Ángulos de apertura: puerta 100° y freezer 90°, que es lo que entra antes del sillón.
- **Mesa y sillas**: guardadas delante del barrido de la puerta granero. Abiertas, quedan en el pasillo con centro en (0.0, 3.08).
- **Sillón**: más corto (1.20 m) y con menos fondo. Corregí los almohadones, que se superponían, y las mantas, que atravesaban el sillón.
- **Escalera**: el primer peldaño queda más alto para que la pedada plegada no atraviese el piso. Las pedadas son de 0.28. El larguero desliza solo en x, termina en y ≤ 3.82 y no llega al piso ni al tabique.

## Choques
| | pares que involucran mis zonas | > 5 cm |
|---|---:|---:|
| antes (`audit/colisiones.md`) | 72 | 26 |
| después, estado cerrado (todo el modelo) | **0** | 0 |
| abiertos: cajones, puerta y freezer de la heladera, escalera desplegada y puerta granero abierta | 1* | 0 |
| abiertos: mesa y sillas desplegadas, con la puerta granero abierta y cerrada | 0 | 0 |

\* `Heladera logo` contra `Heladera puerta`: es una calcomanía plana, hija de la puerta. Es un falso positivo de la prueba de paridad.

Abrir a la vez la mesa y la heladera sí choca (puerta y freezer contra la mesa y la silla 1). Es lo esperable en un pasillo de 0.60 m.

Planta: `audit/planta/planta_despues.png`. Láminas: `audit/planta/{living2,heladera1,entrada1}_audit.jpg`.

## Pendiente
- En living2 el sillón del video parece algo más profundo, hacia el pasillo. Lo dejé en 0.60 para que el freezer pueda abrirse a 90°.
- La mesa y las sillas guardadas (f0111–f0122) no las medí con cámaras. Se dimensionaron por el espacio libre.
