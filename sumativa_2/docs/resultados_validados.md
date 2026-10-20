# Resultados validados — Sumativa 2 (S2), grupo 1

Generado por `sumativa_2/notebooks/sumativa_2_grupo1.ipynb` con la semilla 1505514103 y B = 10.000 réplicas en cada técnica.

## Estado de cada resultado

| id | resultado | valor_s1 | metodo_s2 | evidencia_s2 | estado |
|---|---|---|---|---|---|
| PAR-1 | Proporción de atraso | 59.6691 | Bootstrap percentil y BCa | BCa [58.7508; 60.5873]; ancho/S1 = 1.002 | respaldado |
| PAR-2 | Peso medio | 3634.0167 | Bootstrap percentil y BCa | BCa [3602.7570; 3665.2821]; ancho/S1 = 1.023 | respaldado |
| PAR-3 | Costo medio | 210.1968 | Bootstrap percentil y BCa | BCa [209.3138; 211.1132]; ancho/S1 = 1.002 | respaldado |
| PAR-4 | Llamadas medias | 4.0545 | Bootstrap percentil y BCa | BCa [4.0337; 4.0755]; ancho/S1 = 0.978 | respaldado |
| EFE-1 | Diferencia de peso medio (atrasado − puntual) | -896.0283 | Bootstrap percentil y BCa | BCa [-955.4048; -836.5055]; ancho/S1 = 0.991 | respaldado, magnitud sensible |
| T01 | Prueba χ² de independencia entre modalidad de envío y atraso | 0.7434 | Permutación | p perm. = 0.69113 (6911 excedencias); cota de Bonferroni (7) = 1.0000 | no concluyente |
| T02 | Prueba t de Welch de peso medio entre envíos atrasados y puntuales | -29.2722 | Permutación | p perm. = 0.00010 (0 excedencias); cota de Bonferroni (7) = 0.0007 | respaldado, magnitud sensible |
| T03 | Prueba t de Welch de descuento medio entre envíos atrasados y puntuales | 54.7029 | Permutación | p perm. = 0.00010 (0 excedencias); cota de Bonferroni (7) = 0.0007 | sensible |
| COR-1 | r punto-biserial Descuento – Atraso | 0.3971 | Bootstrap emparejado percentil | IC [0.3879; 0.4065]; EE//r/ = 0.012 | sensible |
| COR-2 | r punto-biserial Peso – Atraso | -0.2688 | Bootstrap emparejado percentil | IC [-0.2867; -0.2509]; EE//r/ = 0.034 | respaldado, magnitud sensible |
| COR-3 | ρ de Spearman Descuento – Peso | -0.3157 | Bootstrap emparejado percentil | IC [-0.3327; -0.2984]; EE//r/ = 0.028 | sensible |
| COR-4 | r punto-biserial Costo – Atraso | -0.0736 | Bootstrap emparejado percentil | IC [-0.0924; -0.0549]; EE//r/ = 0.129 | sensible |
| COR-5 | r punto-biserial Compras previas – Atraso | -0.0555 | Bootstrap emparejado percentil | IC [-0.0746; -0.0374]; EE//r/ = 0.173 | sensible |
| MC-1 | Tasa de atraso en lotes de 1.000 envíos | 59.6691 | Monte Carlo binomial | rango 95 % [56.6; 62.7] %; percentil 99 = 63.3 %; P(>60 %) = 0.398 | sensible |

## Sensibilidad

| id | sensibilidad |
|---|---|
| PAR-1 | Winsorización 1/99: 59.6691; Exclusión IQR: 49.5170; Descuento ≤ 10: 46.8870 |
| PAR-2 | Winsorización 1/99: 3633.1763; Exclusión IQR: 3956.6958; Descuento ≤ 10: 4035.6285 |
| PAR-3 | Winsorización 1/99: 210.2277; Exclusión IQR: 213.6862; Descuento ≤ 10: 214.6341 |
| PAR-4 | Winsorización 1/99: 4.0545; Exclusión IQR: 4.1330; Descuento ≤ 10: 4.1517 |
| EFE-1 | Winsorización 1/99: -897.3692; Exclusión IQR: -449.6153; Descuento ≤ 10: -283.7460 |
| T01 | Winsorización 1/99: efecto 0.008, p perm. 0.6931; Exclusión IQR: efecto 0.013, p perm. 0.5005; Descuento ≤ 10: efecto 0.005, p perm. 0.9013 |
| T02 | Winsorización 1/99: efecto -897.369, p perm. 0.0001; Exclusión IQR: efecto -449.615, p perm. 0.0001; Descuento ≤ 10: efecto -283.746, p perm. 0.0001 |
| T03 | Winsorización 1/99: efecto 13.118, p perm. 0.0001; Exclusión IQR: efecto 0.858, p perm. 0.0001; Descuento ≤ 10: efecto -0.083, p perm. 0.1858 |
| COR-1 | Winsorización 1/99: 0.397 [0.388; 0.406]; Exclusión IQR: 0.121 [0.100; 0.141]; Descuento ≤ 10: -0.014 [-0.036; 0.007] |
| COR-2 | Winsorización 1/99: -0.270 [-0.287; -0.251]; Exclusión IQR: -0.139 [-0.160; -0.117]; Descuento ≤ 10: -0.088 [-0.109; -0.066] |
| COR-3 | Winsorización 1/99: -0.316 [-0.333; -0.299]; Exclusión IQR: -0.081 [-0.103; -0.059]; Descuento ≤ 10: 0.007 [-0.015; 0.028] |
| COR-4 | Winsorización 1/99: -0.074 [-0.093; -0.055]; Exclusión IQR: -0.010 [-0.033; 0.012]; Descuento ≤ 10: 0.003 [-0.018; 0.025] |
| COR-5 | Winsorización 1/99: -0.056 [-0.074; -0.037]; Exclusión IQR: -0.042 [-0.064; -0.020]; Descuento ≤ 10: -0.012 [-0.033; 0.010] |
| MC-1 | P(>60 %) con p = Wilson inferior: 0.203; P(>60 %) con p = Estimación S1: 0.407; P(>60 %) con p = Wilson superior: 0.633; DE dos segmentos / homogéneo = 0.89 |

## Recomendaciones para la Sumativa 3 (S3)

| id | recomendacion_s3 |
|---|---|
| PAR-1 | Usar 59,67 % [58,75; 60,58] como tasa de referencia; reportar por segmento de descuento. |
| PAR-2 | Media válida como resumen, pero el peso es bimodal: modelar con tramos o términos no lineales. |
| PAR-3 | Variable de bajo poder explicativo para el atraso; conservar solo como control. |
| PAR-4 | Media estable; las llamadas pueden ser posteriores al envío: revisar su temporalidad antes de usarlas como predictor. |
| EFE-1 | Incluir el peso en S3; su efecto se reduce fuera del descuento alto: estimar interacción peso × segmento. |
| T01 | No priorizar la modalidad de envío; no rechazar no demuestra igualdad. |
| T02 | Asociación peso–atraso robusta en dirección; reportar el tamaño por segmento. |
| T03 | La diferencia de descuento depende del segmento > 10 (ids 1 a 3.134): auditar su procedencia antes de modelar. |
| COR-1 | La asociación existe solo por el segmento > 10, todo atrasado y contenido en los 3.135 primeros registros; modelarlo aparte (separación completa). |
| COR-2 | Conservar el peso: la única correlación que excluye el cero en todos los escenarios. |
| COR-3 | Descuento y peso están relacionados: modelarlos conjuntamente para evitar confusión. |
| COR-4 | Correlación débil y sensible: no fundamentar decisiones en ella. |
| COR-5 | Correlación débil y sensible: no fundamentar decisiones en ella. |
| MC-1 | Fijar límites de alerta por tamaño de lote y en relación con el IC de p; segmentar por descuento. |

## Síntesis

La conclusión más robusta de la Sumativa 1 es la asociación negativa del peso con el atraso, que se mantiene en todos los métodos y escenarios. La asociación del descuento depende por completo del segmento con descuento mayor que 10, que coincide con los 3.135 primeros registros del archivo, todos atrasados. Los parámetros y sus intervalos se confirman con *bootstrap*, BCa y *jackknife*. Las pruebas de permutación reproducen las decisiones de la Sumativa 1. La simulación Monte Carlo muestra que un umbral de 60 % de atraso por lote se superaría con frecuencia solo por azar.
