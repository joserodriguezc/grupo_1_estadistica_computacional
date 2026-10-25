# Estadística computacional para la toma de decisiones

Proyecto del Grupo 1 del Magíster en Ciencia de Datos e Inteligencia Artificial (UNAB), MCDI501.
**Integrantes:** José Ignacio Rodríguez, Yerko Gallardo Miranda y Sebastián Rojas Araya.

El proyecto estudia asociaciones entre características de envíos y entregas atrasadas en *E-Commerce Shipping Data*. El diseño es observacional; las asociaciones no se interpretan como causas.

## Evaluaciones

| Carpeta | Estado y contenido | Informe |
|---|---|---|
| [formativa_1/](formativa_1/) | Entrega histórica congelada; no modificar análisis, datos ni resultados | [PDF](formativa_1/docs/informe/informe_formativa1.pdf) |
| [sumativa_1/](sumativa_1/) | Análisis exploratorio e inferencial revisado; notebook, tablas, figuras y fuentes | [PDF](sumativa_1/docs/informe/informe_sumativa1_grupo1.pdf) |
| [sumativa_2/](sumativa_2/) | Validación por *bootstrap*, permutación, Monte Carlo, *jackknife* y sensibilidad | [PDF](sumativa_2/docs/informe/informe_sumativa2_grupo1.pdf) |
| [formativa_2/](formativa_2/) | Regresión logística para anticipar atrasos, integrando los resultados de S1 y S2 | [Notebook](formativa_2/notebooks/formativa_2_grupo1.ipynb) |
| [sumativa_3/](sumativa_3/) | Cierre del proyecto: imputación por regresión lineal múltiple y clasificación con regresión logística, integrando S1 y S2 (en desarrollo) | [PDF](sumativa_3/docs/informe/informe_sumativa3_grupo1.pdf) |

El detalle metodológico y de ejecución de la Sumativa 1 está en [sumativa_1/README.md](sumativa_1/README.md).

### Sumativa 2

La Sumativa 2 lee el CSV y las tablas de referencia de `sumativa_1/`, sin copiar los datos. Incluye dos notebooks con alcances distintos:

| Notebook | Alcance | Salidas en `sumativa_2/` |
|---|---|---|
| [Entrega](sumativa_2/notebooks/sumativa_2_grupo1.ipynb) | Resultados seleccionados que sostienen las conclusiones de S1, ajustados a la rúbrica | `outputs/tablas/`, `outputs/figuras/`, `outputs/resultados_validados.csv` y `docs/resultados_validados.md` |
| [Validación completa](sumativa_2/notebooks/sumativa_2_validacion_completa_grupo1.ipynb) | Respaldo inferencial de los 194 resultados del inventario de S1 | `outputs/validacion_completa/` |

El [informe](sumativa_2/docs/informe/informe_sumativa2_grupo1.pdf) integra el análisis y los anexos A–C. Estos se generan desde las tablas de ambos notebooks mediante [generar_anexos.py](sumativa_2/docs/informe/generar_anexos.py). La [matriz de resultados validados](sumativa_2/docs/resultados_validados.md) resume la evidencia y los insumos para la Sumativa 3.

## Entorno y ejecución

Requisitos: Git, uv y Python 3.14 según `.python-version` y `pyproject.toml`; para los PDF, TeX Live/MiKTeX con los paquetes utilizados por los informes y `latexmk`. El entorno incluye JupyterLab y un kernel de Jupyter. No se requieren credenciales de Kaggle para ejecutar con el CSV disponible.

Todos los comandos siguientes se ejecutan desde la raíz del repositorio.

### Preparar el entorno

```bash
uv sync --locked
```

Las dependencias se fijan en `uv.lock`. En VS Code se puede seleccionar `.venv` como entorno del kernel y ejecutar todas las celdas después de reiniciarlo. También se puede iniciar JupyterLab con `uv run jupyter lab`.

### Ejecutar los análisis

Para reproducir la Sumativa 1:

```bash
uv run jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=180 sumativa_1/notebooks/sumativa_1_grupo1.ipynb
```

Para reproducir la Sumativa 2:

```bash
uv run jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=1800 sumativa_2/notebooks/sumativa_2_grupo1.ipynb
uv run jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=3600 sumativa_2/notebooks/sumativa_2_validacion_completa_grupo1.ipynb
```

Para reproducir la Sumativa 3 (ver [sumativa_3/README.md](sumativa_3/README.md)):

```bash
uv run jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=3600 sumativa_3/notebooks/sumativa_3_grupo1.ipynb
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error sumativa_3/docs/informe/informe_sumativa3_grupo1.tex
```

Para reproducir la Formativa 2:

```bash
uv run jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=600 formativa_2/notebooks/formativa_2_grupo1.ipynb
```

Las tablas de S1 y S2 ya están incluidas: no es necesario volver a ejecutar S1 para ejecutar S2, ni S1 o S2 para ejecutar la Formativa 2. La validación completa comprueba sus huellas contra `sumativa_2/docs/manifiesto_s1.json`; si las tablas cambian, se detiene para señalar la diferencia.

Los comandos con `--inplace` actualizan los notebooks y regeneran sus salidas. Cada notebook reconoce su carpeta de evaluación y guarda allí los resultados; el CSV original no se modifica. La validación completa requiere más tiempo que el notebook de entrega; la duración depende del equipo.

### Generar anexos y compilar los informes

Para la Sumativa 1:

```bash
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error sumativa_1/docs/informe/informe_sumativa1_grupo1.tex
```

Para la Sumativa 2, después de ejecutar ambos notebooks:

```bash
uv run python sumativa_2/docs/informe/generar_anexos.py sumativa_2 sumativa_2/docs/informe/anexos.tex
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error sumativa_2/docs/informe/informe_sumativa2_grupo1.tex
```

La opción `-cd` compila desde la carpeta del informe para resolver sus rutas relativas. Si solo se necesita recompilar los PDF con los resultados incluidos en el repositorio, basta con ejecutar los comandos de `latexmk`: las figuras y `anexos.tex` ya están disponibles.

## Organización de archivos

| Ruta | Contenido |
|---|---|
| `formativa_1/` | Datos, documentación, notebook y resultados de la entrega histórica |
| `sumativa_1/data/raw/` | CSV utilizado por S1 y S2 |
| `sumativa_1/docs/` | Fuente, diccionario, ficha descriptiva, protocolo y registro de integridad |
| `sumativa_1/outputs/` | Tablas y figuras del análisis exploratorio e inferencial |
| `sumativa_2/docs/` | Protocolo y registro de semilla, manifiesto de S1 y resultados validados |
| `sumativa_2/outputs/` | Tablas, figuras y matriz de resultados del notebook de entrega |
| `sumativa_2/outputs/validacion_completa/` | Tablas y figuras del notebook de respaldo |
| `sumativa_1/notebooks/`, `sumativa_2/notebooks/` | Notebooks de análisis con sus resultados de ejecución |
| `sumativa_1/docs/informe/`, `sumativa_2/docs/informe/` | Fuentes LaTeX y PDF de los informes |
| `sumativa_1/scripts/`, `sumativa_2/scripts/` | Verificación de datos, generación del diccionario y gestión de la semilla, según la evaluación |

Las versiones del entorno y los metadatos se registran en [entorno_ejecucion.json](sumativa_1/outputs/tablas/entorno_ejecucion.json) para S1 y [metadatos_ejecucion.json](sumativa_2/outputs/tablas/metadatos_ejecucion.json) para la entrega de S2.

## Integridad y procedencia

Fuente: Gopalani, P. (2021), [E-Commerce Shipping Data, versión 1](https://www.kaggle.com/datasets/prachi13/customer-analytics). La unidad del descuento no está acreditada y el origen muestral es desconocido. Consultar `sumativa_1/docs/fuente_datos.md` para condiciones de uso y diferencias de saltos de línea respecto de Kaggle.

El análisis de la Sumativa 1 es determinista: no utiliza simulación ni remuestreo aleatorio; no requiere semilla. La Sumativa 2 usa la semilla única **1505514103**, congelada en [registro_semilla.json](sumativa_2/docs/registro_semilla.json) según el [protocolo de semilla](sumativa_2/docs/protocolo_semilla.md). Los notebooks leen ese registro local y derivan flujos aleatorios por sección; no es necesario obtener una nueva semilla ni consultar el *beacon* para ejecutar el análisis. Los intervalos son individuales del 95 % y Holm controla la familia de siete pruebas documentada en el protocolo. El código no garantiza representatividad ni independencia.

Para verificar el registro contra el *beacon* (requiere conexión a Internet):

```bash
uv run python sumativa_2/scripts/semilla_beacon.py verificar
```
