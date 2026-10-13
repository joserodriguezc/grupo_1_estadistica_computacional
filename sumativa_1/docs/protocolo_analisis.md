# Protocolo definitivo de análisis — Sumativa 1

**Alcance:** evaluación estadística observacional sobre 10.999 registros y 12 variables de *E-Commerce Shipping Data*, versión 1. La pregunta es qué características de los registros se asocian con la entrega atrasada y qué segmentos merecen auditoría operacional. La unidad de análisis es cada registro; no se puede comprobar que todos correspondan a clientes o cargas independientes.

## Definiciones y preparación

- Objetivo binario: `entrega_atrasada = 1` para atrasada y `0` para puntual; tamaños `n_atr = 6.563`, `n_punt = 4.436`.
- Clasificar variables por significado: nominales, ordinales y cuantitativas. No interpretar `ID` como magnitud ni incorporarlo a correlaciones.
- Auditar integridad del CSV, nulos, duplicados, cardinalidades y categorías. Conservar observaciones extremas si no existe evidencia de error; no imputar datos inexistentes.
- Mantener explícitas las unidades: peso en gramos y costo en USD según la documentación. La unidad de descuento no está documentada.

## Estadística descriptiva

Para variables cuantitativas: `n`, media, mediana, desviación estándar muestral, mínimo, máximo, Q1, Q3, IQR, asimetría corregida y curtosis en exceso (Fisher). Para nominales: frecuencias y porcentajes; para ordinales: frecuencia y orden. Graficar distribuciones y relaciones con la respuesta; emplear **Spearman** para relaciones monótonas entre cuantitativas y **V de Cramér** para intensidad de asociación entre cualitativas.

## Estimación

Cuatro estimaciones: proporción global de atraso, medias de peso, costo y llamadas. Intervalos individuales del 95 %, con tamaño muestral indicado. La **proporción global** y las tasas por subgrupo usan **Wilson**; las **medias** usan el intervalo **t de Student** (n − 1 gl); las **diferencias entre medias**, intervalos **t de Welch**, y las **diferencias entre proporciones** (E2, E3), el intervalo de **Newcombe**. Se documentan método, límites y supuestos.

## Contrastes de hipótesis

Se fija `α = 0,05`, contraste bilateral cuando corresponde, y ajuste **Holm** para la familia de **siete** pruebas. Las diferencias de medias y proporciones se calculan como grupo de atrasadas menos puntuales o grupo de interés menos comparación, según el contraste.

| Código | Hipótesis nula (H0) | Alternativa (H1) | Procedimiento |
|---|---|---|---|
| T01 | Modalidad de transporte y atraso independientes | Existe asociación | χ² de independencia |
| T02 | μ_peso,atr − μ_peso,punt = 0 | Diferencia ≠ 0 | t de Welch |
| T03 | μ_desc,atr − μ_desc,punt = 0 | Diferencia ≠ 0 | t de Welch |
| E1 | Distribuciones del peso iguales entre grupos | Diferencia en distribuciones/rangos | Mann–Whitney bilateral |
| E2 | p_atraso,importancia alta = p_atraso,resto | Tasas diferentes | z de dos proporciones |
| E3 | p_atraso,descuento > 10 = p_atraso,descuento ≤ 10 | Tasas diferentes | z de dos proporciones |
| E4 | μ_costo,atr − μ_costo,punt = 0 | Diferencia ≠ 0 | t de Welch |

**Condiciones de uso:** χ² requiere frecuencias esperadas adecuadas; Welch permite varianzas desiguales pero presupone independencia; Mann–Whitney no representa exclusivamente una comparación de medianas si cambian las formas; z requiere conteos suficientes y utiliza estimación combinada bajo H0. Wilson y Newcombe se emplean porque no se degeneran cuando una proporción observada es 0 o 1. Los valores p exportados como cero numérico pueden reflejar subdesbordamiento.

**Tamaños de efecto:** $d_{av}$ (d de Cohen con desviación estándar promedio) para diferencias de medias, en todo el análisis; correlación biserial de rangos para E1; diferencia de proporciones y riesgo relativo para E2 y E3; V de Cramér para asociación entre categóricas.

## Multiplicidad, interpretación y alcance

Holm controla el error familiar de siete contrastes bajo sus condiciones, **pero no corrige** la exploración o la selección de segmentos tras observar los datos. El umbral de descuento > 10 es un hallazgo exploratorio. No rechazar H0 no equivale a demostrar igualdad; significancia no implica magnitud relevante. Los intervalos requieren condiciones de muestreo e independencia que no pueden validarse completamente: faltan fecha, cliente, ruta y marco muestral. No adjudicar causalidad a descuento, peso o modalidad; confirmar la temporalidad del descuento antes de utilizarlo para predicción.

## Evidencia reproducible

Fuente principal: `notebooks/sumativa_1_grupo1.ipynb`; exportaciones en `outputs/tablas/`; gráficos en `outputs/figuras/`; texto y anexos incorporados en `docs/informe/informe_sumativa1_grupo1.tex`.