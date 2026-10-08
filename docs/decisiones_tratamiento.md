# Decisiones de tratamiento de datos

**Tarea:** Y03 Auditar calidad y preparar datos analíticos.
**Responsable de ejecución:** Yerko Gallardo.
**Revisor:** José Ignacio Rodríguez.
**Estado:** Borrador para revisión.

Los controles se ejecutan en `notebooks/formativa_1.ipynb` (secciones 0 y 1) y se exportan a `outputs/tablas/calidad_datos.csv`. La carga del original y la base analítica se construyen en la sección 0 del notebook.

## 1. Resumen de la auditoría

Sobre 10.999 registros y 12 columnas: 23 controles OK, 4 hallazgos informativos y ninguna alerta.

| Aspecto | Resultado |
|---|---|
| Nulos | 0 celdas vacías; no se imputa ni se crean faltantes |
| `ID` | 10.999 valores únicos (no prueba independencia) |
| Dominios categóricos | Bodega A, B, C, D, F; modalidad Flight, Road, Ship; género F, M |
| Ordinales | `Product_importance` low, medium, high; `Customer_rating` 1 a 5 |
| Resultado | Valores {0, 1}; 6.563 atrasadas (1) y 4.436 a tiempo (0) |
| Alias | `entrega_atrasada` coincide con `Reached.on.Time_Y.N` en los 10.999 registros |
| Rangos | Sin ceros ni negativos en las variables numéricas |
| Duplicados | 0 con `ID` y 0 sin `ID` |
| Extremos (regla 1,5 × IQR) | `compras_previas`: 1.003 altos; `descuento_ofrecido`: 2.209 altos; el resto, ninguno |

## 2. Decisiones

| N.º | Decisión | Motivo | Filas antes → después |
|---|---|---|---|
| D1 | El original no se modifica; las transformaciones ocurren al cargar | Trazabilidad | 10.999 → 10.999 |
| D2 | Sin exclusiones de filas | No hay nulos, duplicados ni valores inválidos | 10.999 → 10.999 |
| D3 | Sin imputación ni faltantes artificiales | No hay ausencias | — |
| D4 | Se conservan los extremos IQR de `compras_previas` y `descuento_ofrecido` | Son conteos y descuentos válidos y asimétricos, no errores | — |
| D5 | Se crea `entrega_atrasada` (1 = atrasada) y se conserva la columna original | Convención del protocolo | — |
| D6 | `importancia_producto` se declara ordinal: low < medium < high | Clasificación Y02 | — |
| D7 | Los nombres analíticos reemplazan a los originales en la base analítica | Legibilidad; correspondencia en `docs/diccionario_variables.csv` | — |
| D8 | La bodega F se mantiene sin recodificar | Discrepancia con la descripción A–E; documentada | — |

## 3. Hallazgos exploratorios

Los umbrales se observaron mirando el resultado. No son pruebas de hipótesis y no forman parte de la familia de contrastes planificados.

1. **Descuento.** Con `Discount_offered` > 10 hay 2.647 registros, todos atrasados (100 %). Con descuento ≤ 10 hay 8.352 registros, con 46,9 % de atraso. La unidad del descuento no está especificada y podría registrarse con o después del resultado. Se usará con cautela en la interpretación y se declarará en las limitaciones.
2. **Peso.** Entre 2.001 y 4.000 g hay 1.788 registros, con 99,9 % de atraso. Fuera de ese tramo hay 9.211 registros, con 51,9 %. La distribución de `Weight_in_gms` tiene un hueco casi vacío en ese rango, por lo que la media resume mal la forma. Esto debe considerarse al interpretar T02.
3. **Bodega F.** Concentra 3.666 registros, el doble de cada una de las otras. Su proporción de atraso (59,9 %) no se distingue de las demás. Se desconoce si es una categoría agrupada.

## 4. Pendientes

- Confirmar el motivo de la concentración en la bodega F y la unidad del descuento (sin fuente disponible).
- Formalizar los controles como funciones reutilizables en `src/func/validacion.py` (S02, Sebastián).
