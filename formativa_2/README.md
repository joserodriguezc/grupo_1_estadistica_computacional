# Formativa 2 — Regresión logística

Práctica guiada de modelamiento predictivo, preparatoria de la Sumativa 3: anticipar si un envío llegará atrasado con una regresión logística. Las decisiones se apoyan en los resultados de la Sumativa 1 (S1) y la Sumativa 2 (S2).

## Contenido

- `notebooks/formativa_2_grupo1.ipynb`: notebook de entrega, ejecutado y con salidas. Cubre:
  1. hallazgos de S1 y S2;
  2. preparación de datos: faltantes simulados de forma completamente aleatoria (MCAR) e imputados con la mediana, outliers, partición 70/30 estratificada y estandarización;
  3. regresión logística con odds ratios y VIF, y confirmación de la selección con eliminación recursiva de características (RFE);
  4. desempeño en el conjunto de prueba: matriz de confusión, métricas, curva ROC y AUC, más validación cruzada estratificada de 10 particiones y búsqueda de hiperparámetros con GridSearchCV;
  5. síntesis para S3.
- `outputs/tablas/`: hallazgos de S1 y S2, faltantes simulados, partición, coeficientes y odds ratios, VIF, RFE, métricas, validación cruzada, búsqueda de hiperparámetros, sensibilidad y metadatos de ejecución.
- `outputs/figuras/`: odds ratios, matriz de confusión, curva ROC y validación cruzada, en PDF y PNG.

## Datos y reproducibilidad

- **Datos:** se leen desde `sumativa_1/data/raw/ecommerce_shipping.csv`, sin copiarlos. Antes de usarlos se verifica su huella SHA-256.
- **Resultados previos:** se leen desde `sumativa_1/outputs/tablas/` y `sumativa_2/outputs/`.
- **Semilla:** la simulación de faltantes y la partición usan la semilla de S2 (`sumativa_2/docs/registro_semilla.json`). Los faltantes usan el octavo hijo de `SeedSequence(SEMILLA)`; los siete primeros los usa S2.

Desde la raíz del repositorio:

```bash
uv sync --locked
uv run jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=600 formativa_2/notebooks/formativa_2_grupo1.ipynb
```
