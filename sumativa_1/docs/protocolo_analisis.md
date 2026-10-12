# Protocolo de análisis de la Sumativa 1

Equipo: José Ignacio Rodríguez, Yerko Gallardo y Sebastián Rojas.

## Problema y alcance

Identificar características y segmentos de envíos asociados con atraso para una investigación operacional posterior. Diseño observacional; unidad provisional: registro de envío asociado a un cliente. Fuente: E-Commerce Shipping Data, versión 1; 10.999 registros y 12 columnas. ID no implica independencia ni secuencia temporal. Codificación: 1 = atrasada, 0 = puntual; diferencias = atrasadas menos puntuales.

## Descriptiva y calidad

Clasificar por significado y escala documentados, no por número de valores únicos. Cuantitativas: n, media, mediana, DE muestral, cuartiles, IQR, extremos, asimetría ajustada y exceso de curtosis. Nominales: frecuencia y porcentaje; ordinales: orden preservado. Spearman entre cuantitativas, sin ID ni códigos nominales. Mantener raw intacto y auditar tipos, dominios, nulos, duplicados y extremos. No imputar ni crear faltantes artificiales.

## Estimación

Cuatro parámetros: proporción de atraso, peso medio, costo medio y llamadas medias. IC global normal del 95 %, con n efectivo y supuestos explícitos; el 95 % describe cobertura del procedimiento bajo muestreo repetido. Para tasas por subgrupo, Wilson. IC de diferencias de medias: t de Welch. Los intervalos son individuales, sin corrección simultánea.

## Hipótesis y códigos vigentes

| Código | H0 | H1 | Método |
|---|---|---|---|
| T01 | Modalidad y atraso independientes | Asociados | χ² |
| T02 | Diferencia de peso medio = 0 | Distinta de 0 | Welch bilateral |
| T03 | Diferencia de descuento medio = 0 | Distinta de 0 | Welch bilateral |
| E1 | Distribuciones de peso iguales | Diferencia detectable por rangos | Mann-Whitney bilateral asintótico |
| E2 | Tasa de atraso en importancia alta = resto | Diferentes | z bilateral combinado |
| E3 | Tasa de atraso con descuento > 10 = <= 10 | Diferentes | z bilateral combinado |
| E4 | Diferencia de costo medio = 0 | Distinta de 0 | Welch bilateral |

El plan inicial incluyó modalidad, peso y costo. Durante el EDA se añadió descuento y costo pasó a E4. Ese cambio y las pruebas complementarias se documentan como exploratorios, sin afirmar preespecificación anterior a observar los datos. Se conserva α = 0,05 y se aplica Holm a una familia de siete valores p. El ajuste no corrige selección de hipótesis ni del umbral de descuento, que surgió del EDA. No se sustituye esta familia por otra para favorecer significancia.

## Supuestos e interpretación

Independencia no verificable con estas columnas. χ²: frecuencias esperadas suficientes. Welch: dos grupos, varianzas distintas permitidas, revisión de forma e influencia; no exige igualdad de varianzas. Mann-Whitney: independencia, método asintótico con empates; no se afirma prueba exclusiva de medianas. z: proporción combinada bajo H0 y conteos esperados suficientes. En E3 la proporción observada 1 exige cautela con Wald; se reporta Wilson por grupo. No interpretar p = 0 de máquina como probabilidad nula.

No rechazar H0 no prueba igualdad. Magnitud, incertidumbre y limitaciones acompañan la significancia. La recomendación es auditar los 2.647 envíos con descuento > 10 y contrastarlos con <= 10, investigando campañas, productos y temporalidad antes de actuar. No atribuir causas ni generalizar a todo el comercio electrónico.

## Trazabilidad

Notebook: `notebooks/sumativa_1.ipynb`; matriz y resultados: `outputs/tablas/`; figuras: `outputs/figuras/`; fuente y PDF: `docs/informe/`. Versiones utilizadas y SHA-256: `outputs/tablas/entorno_ejecucion.json`. Sin pasos aleatorios; no se requiere semilla. La Formativa 1 queda congelada.
