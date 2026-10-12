# Estadística computacional para la toma de decisiones

Proyecto del Grupo 1 del Magíster en Ciencia de Datos e Inteligencia Artificial (UNAB), MCDI501.
**Integrantes:** José Ignacio Rodríguez, Yerko Gallardo Miranda y Sebastián Rojas Araya.

El proyecto estudia asociaciones entre características de envíos y entregas atrasadas en *E-Commerce Shipping Data*. El diseño es observacional; las asociaciones no se interpretan como causas.

## Evaluaciones

| Carpeta | Estado y contenido | Informe |
|---|---|---|
| `formativa_1/` | Entrega histórica congelada; no modificar análisis, datos ni resultados | `docs/informe/informe_formativa1.pdf` |
| `sumativa_1/` | Análisis exploratorio e inferencial revisado; notebook, tablas, figuras y fuentes | `docs/informe/informe_sumativa1.pdf` |

El detalle metodológico y de ejecución está en [sumativa_1/README.md](sumativa_1/README.md).

## Entorno y ejecución

Requisitos: Git, uv y Python 3.14 según `.python-version` y `pyproject.toml`; para el PDF, TeX Live/MiKTeX y `latexmk`. El entorno incluye un kernel de Jupyter. No se requieren credenciales de Kaggle para ejecutar con el CSV ya disponible.

Desde la raíz del repositorio:

```bash
uv sync --locked
uv run jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=180 sumativa_1/notebooks/sumativa_1.ipynb
cd sumativa_1/docs/informe
latexmk -pdf -interaction=nonstopmode -halt-on-error informe_sumativa1.tex
cd ../../..
```

El notebook reconoce la raíz de la sumativa desde el repositorio o su carpeta `notebooks/`, sin rutas personales. Todas las salidas se guardan en `sumativa_1/outputs/`; el CSV no se modifica. También se puede abrir el notebook en VS Code, seleccionar `.venv` y ejecutar todas las celdas después de reiniciar el kernel.

Se conservan `uv.lock` y las declaraciones de versión existentes. Las versiones de Python y de los paquetes usados en la ejecución se registran en `sumativa_1/outputs/tablas/entorno_ejecucion.json`.

## Estructura de cada evaluación

- `data/raw/`: copia de los datos y referencia de integridad.
- `docs/`: fuente, diccionario, ficha y protocolo.
- `notebooks/`: análisis ordenado y resultados de ejecución.
- `outputs/tablas/`: resultados CSV y metadatos de ejecución.
- `outputs/figuras/`: PDF vectorial y PNG; el pairplot se conserva como PNG.
- `docs/informe/`: fuente `.tex` y PDF del informe; no se versionan temporales.
- `scripts/`: verificaciones y generación del diccionario.

## Integridad y procedencia

Fuente: Gopalani, P. (2021), [E-Commerce Shipping Data, versión 1](https://www.kaggle.com/datasets/prachi13/customer-analytics). La unidad del descuento no está acreditada y el origen muestral es desconocido. Consultar `sumativa_1/docs/fuente_datos.md` para condiciones de uso y diferencias de saltos de línea respecto de Kaggle.

El análisis es determinista: no utiliza simulación ni remuestreo aleatorio; no requiere semilla. Los intervalos son individuales del 95 % y Holm controla la familia de siete pruebas documentada en el protocolo. El código no garantiza representatividad ni independencia.
