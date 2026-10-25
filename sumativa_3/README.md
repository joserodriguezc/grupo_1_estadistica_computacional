# Sumativa 3 — Cierre y comunicación del proyecto

Proyecto final integrado. Aplica **regresión lineal múltiple** para imputar datos faltantes y **regresión logística** para clasificar el atraso. Cada decisión se fundamenta en los resultados de la Sumativa 1 (S1, análisis exploratorio e inferencial) y de la Sumativa 2 (S2, validación por remuestreo y simulación).

## Productos

| Producto | Ubicación |
|---|---|
| Notebook maestro | [`notebooks/sumativa_3_grupo1.ipynb`](notebooks/sumativa_3_grupo1.ipynb) |
| Informe final (PDF, máximo 10 páginas) | [`docs/informe/informe_sumativa3_grupo1.pdf`](docs/informe/informe_sumativa3_grupo1.pdf) |
| Presentación (video, 10 minutos) | *(enlace pendiente)* |
| Tablas y figuras | `outputs/tablas/` y `outputs/figuras/` |

## Estructura del notebook y responsables

| Sección | Contenido | Responsable |
|---|---|---|
| 0 | Configuración, datos, semilla, partición común y funciones compartidas | José |
| 1 | Punto de partida: hallazgos de S1 y S2 | José |
| 2 | Parte 1: datos faltantes, imputación por regresión y comparación de estrategias | Yerko |
| 3 | Parte 2: tres modelos logísticos, desempeño, selección, *bootstrap* (3.4, Yerko) y diagnóstico | Sebastián |
| 4 | Parte 3: impacto de la estrategia de imputación | José |
| 5 | Síntesis | José, con el equipo |

## Contrato entre secciones

Cada parte deja definidos estos objetos para las siguientes:

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
  - `MODELO_FINAL`.

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

## Normas de trabajo

- **Ramas y commits:** una rama por tarea (`s3/...`) y PR a `main`; los commits van sin coautoría.
- **Notebook:**
  - cada integrante edita solo sus celdas;
  - se commitea con salidas;
  - antes de entregar, se reejecuta completo con el kernel limpio.
- **Redacción:** las siglas se escriben con su nombre completo en la primera mención; se usa formato numérico es-CL y la convención de figuras de S2.
