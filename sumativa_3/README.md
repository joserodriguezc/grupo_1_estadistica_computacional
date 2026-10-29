# Sumativa 3 — Cierre y comunicación del proyecto

Proyecto final integrado. Aplica **regresión lineal múltiple** para imputar datos faltantes y **regresión logística** para clasificar el atraso. Cada decisión se fundamenta en los resultados de la Sumativa 1 (S1, análisis exploratorio e inferencial) y de la Sumativa 2 (S2, validación por remuestreo y simulación).

## Productos

| Producto | Ubicación |
|---|---|
| Notebook maestro | [`notebooks/sumativa_3_grupo1.ipynb`](notebooks/sumativa_3_grupo1.ipynb) |
| Informe final (PDF, máximo 10 páginas) | [`docs/informe/informe_sumativa3_grupo1.pdf`](docs/informe/informe_sumativa3_grupo1.pdf) |
| Anexo técnico: técnicas estadísticas del proyecto (PDF) | [`docs/informe/anexo_tecnico_grupo1.pdf`](docs/informe/anexo_tecnico_grupo1.pdf) |
| Presentación (video, 10 minutos) | [Video en Google Drive](https://drive.google.com/file/d/17S2-DDoHsmyMLkQLdXjXKSkJi6s6zR37/view?usp=sharing) |
| Láminas de la presentación | [`docs/presentacion/presentacion_sumativa3_estilo_UNAB.pptx`](docs/presentacion/presentacion_sumativa3_estilo_UNAB.pptx) |
| Tablas y figuras | `outputs/tablas/` y `outputs/figuras/` |

## Estructura del notebook

| Sección | Contenido |
|---|---|
| 0 | Configuración, datos, semilla, partición común y funciones compartidas |
| 1 | Punto de partida: hallazgos de S1 y S2 |
| 2 | Parte 1: datos faltantes, imputación por regresión y comparación de estrategias |
| 3 | Parte 2: tres modelos logísticos en el segmento con descuento ≤ 10, desempeño, selección, *bootstrap* y diagnóstico |
| 4 | Parte 3: impacto de la estrategia de imputación |
| 5 | Síntesis y recomendaciones |

## Objetos compartidos entre secciones

Cada sección deja definidos estos objetos, que usan las siguientes:

- **Sección 0:**
  - `df`: datos completos de S1 (10.999 envíos);
  - `IDX_TRAIN` e `IDX_TEST`: partición común 70/30 estratificada, la misma de la Formativa 2;
  - `particionar(datos)`;
  - `generador('s3_faltantes')` y `generador('s3_bootstrap')`;
  - funciones `disenar`, `ajustar_logit`, `tabla_odds_ratios`, `metricas_clasificacion` e `intervalos_bootstrap`.
- **Sección 1:** `pares_s1_s2`, con el ρ de Spearman de S1 y su estabilidad en S2 para cada par de variables numéricas.
- **Parte 1:**
  - `df_faltantes`, con los NaN simulados;
  - `DATASETS = {'eliminacion', 'mediana', 'regresion'}`: DataFrames sin NaN que conservan el índice original;
  - `ESTRATEGIA`, la clave elegida.
- **Parte 2:**
  - `MODELOS = {'M1', 'M2', 'M3'}`, cada uno con sus `numericas` y `categoricas`;
  - `MODELO_FINAL` y `UMBRAL_SEGMENTO` (descuento ≤ 10).

## Datos y reproducibilidad

- **Datos:** se leen desde `sumativa_1/data/raw/ecommerce_shipping.csv`, sin copiarlos, y se verifica su huella SHA-256.
- **Referencias:** se leen desde `sumativa_1/outputs/tablas/`, `sumativa_2/outputs/` y `formativa_2/outputs/tablas/`.
- **Semilla:** es la de S2 (`sumativa_2/docs/registro_semilla.json`, del *beacon* de la Universidad de Chile). Los flujos 8 y 9 de `SeedSequence(SEMILLA).spawn(10)` corresponden a los faltantes y al *bootstrap* de S3.

Desde la raíz del repositorio:

```bash
uv sync --locked
uv run jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=3600 sumativa_3/notebooks/sumativa_3_grupo1.ipynb
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error sumativa_3/docs/informe/informe_sumativa3_grupo1.tex
```
