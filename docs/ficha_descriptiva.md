# Ficha descriptiva del conjunto de datos

**Tarea:** Y02 Construir diccionario y ficha descriptiva.
**Responsable de ejecución:** Yerko Gallardo.
**Revisor:** José Ignacio Rodríguez.
**Estado:** Borrador para revisión; aprobación conjunta con J01 pendiente.

Complementa `docs/fuente_datos.md` (procedencia e integridad) y `docs/diccionario_variables.csv` (detalle por variable, generado con `scripts/generar_diccionario.py`).

## 1. Contexto

*E-Commerce Shipping Data* (Gopalani, 2021, versión 1) reúne registros de envíos de una empresa de comercio electrónico de productos electrónicos, según la descripción de la publicadora. La empresa, el período y el mecanismo de selección no están documentados.

El archivo analizado contiene **10.999 registros y 12 columnas**, sin celdas vacías y con 10.999 valores distintos de `ID`.

## 2. Problema de decisión

Identificar características o segmentos de envíos asociados con entregas atrasadas que justifiquen una investigación operacional posterior. El diseño es observacional: se estudian asociaciones, no causas (ver `docs/protocolo_analisis.md`).

## 3. Unidad de análisis (provisional)

Registro de envío asociado a un cliente. Que `ID` sea único no prueba que cada cliente aparezca una sola vez ni que los registros sean independientes. Ambos supuestos quedan declarados como limitación.

## 4. Variable de resultado

`Reached.on.Time_Y.N`: **1 = no llegó a tiempo (atrasada)**, **0 = llegó a tiempo**. Codificación confirmada en la descripción de Kaggle. Se conserva la columna original y se creará el alias `entrega_atrasada` con los mismos valores.

Distribución observada: 6.563 atrasadas (59,7 %) y 4.436 a tiempo (40,3 %), sobre 10.999 registros.

## 5. Clasificación de variables

| Variable | Tipo estadístico | Unidad | Dominio observado |
|---|---|---|---|
| `ID` | Identificador nominal | — | 1 a 10.999 |
| `Warehouse_block` | Cualitativa nominal | — | A, B, C, D, F |
| `Mode_of_Shipment` | Cualitativa nominal | — | Flight, Road, Ship |
| `Customer_care_calls` | Cuantitativa discreta (conteo) | llamadas | 2 a 7 |
| `Customer_rating` | Cualitativa ordinal | puntos | 1 a 5 |
| `Cost_of_the_Product` | Cuantitativa de razón | USD (según Kaggle) | 96 a 310 |
| `Prior_purchases` | Cuantitativa discreta (conteo) | compras | 2 a 10 (sin 9) |
| `Product_importance` | Cualitativa ordinal | — | low < medium < high |
| `Gender` | Cualitativa nominal | — | F, M |
| `Discount_offered` | Cuantitativa | **no especificada** | 1 a 65 |
| `Weight_in_gms` | Cuantitativa de razón | gramos (según Kaggle) | 1.001 a 7.846 |
| `Reached.on.Time_Y.N` | Nominal binaria (resultado) | — | 0, 1 |

Distinciones aplicadas:

- `Customer_rating` y `Product_importance` son ordinales: se conserva el orden y no se suponen distancias iguales. `Customer_care_calls` y `Prior_purchases` son conteos, no ordinales.
- `ID` se excluye de estadísticas sustantivas y correlaciones. No implica orden cronológico.

## 6. Relaciones propuestas

| Relación | Variables | Uso previsto |
|---|---|---|
| Modalidad y atraso | `Mode_of_Shipment`, `Reached.on.Time_Y.N` | Contraste χ² (T01) |
| Peso y atraso | `Weight_in_gms`, `Reached.on.Time_Y.N` | Welch (T02) |
| Costo y atraso | `Cost_of_the_Product`, `Reached.on.Time_Y.N` | Welch (T03) |
| Bodega y atraso | `Warehouse_block`, `Reached.on.Time_Y.N` | Exploratoria, sin prueba formal |
| Relaciones numéricas | Variables cuantitativas sin `ID` | Exploratoria, para fases posteriores |

## 7. Incertidumbres abiertas

1. **Bodega F.** El archivo contiene A, B, C, D y F, mientras la descripción de Kaggle menciona A–E. F reúne 3.666 registros, el doble de cada una de las otras (1.833 a 1.834). No se recodifica F como E. Se desconoce si F es una categoría agrupada o un error de documentación.
2. **Unidad de `Discount_offered`.** No está especificada. No se interpreta como porcentaje ni como moneda.
3. **Momento de registro.** No se documenta cuándo se registraron `Customer_care_calls` y `Customer_rating`. Podrían ser posteriores al atraso, por lo que su asociación con él no demuestra capacidad de anticiparlo.
4. **Selección y dependencia.** No se conoce cómo se seleccionaron los registros ni si un cliente aparece varias veces.
5. **Escala de `Customer_rating`.** No se especifica el sentido de la escala 1–5. Se asume 5 = mejor calificación, a verificar.

## 8. Decisiones iniciales

- El archivo original no se modifica; las transformaciones se hacen en la carga analítica (Y03).
- No se imputa ni se crean faltantes: no hay celdas vacías. Y03 revisará códigos especiales de ausencia.
- No se eliminan extremos válidos ni perfiles repetidos sin justificación.

## 9. Referencia

Gopalani, P. (2021). *E-Commerce Shipping Data* (versión 1) [Conjunto de datos]. Kaggle. https://www.kaggle.com/datasets/prachi13/customer-analytics
