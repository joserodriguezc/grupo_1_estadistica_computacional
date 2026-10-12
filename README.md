# Estadística computacional para la toma de decisiones

Proyecto del Grupo 1 del Magíster en Ciencia de Datos e Inteligencia Artificial (UNAB), MCDI501.
**Integrantes:** José Ignacio Rodríguez, Yerko Gallardo y Sebastián Rojas.

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

```powershell
uv sync --locked
uv run jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=180 sumativa_1/notebooks/sumativa_1.ipynb
Push-Location sumativa_1/docs/informe
latexmk -pdf -interaction=nonstopmode -halt-on-error informe_sumativa1.tex
Pop-Location
```

El notebook reconoce la raíz de la sumativa desde el repositorio o su carpeta `notebooks/`, sin rutas personales. Todas las salidas se guardan en `sumativa_1/outputs/`; el CSV no se modifica. También se puede abrir el notebook en VS Code, seleccionar `.venv` y ejecutar todas las celdas después de reiniciar el kernel.

Se conservan `uv.lock` y las declaraciones de versión existentes. La verificación adjunta se realizó con Python 3.14.8 y las versiones del lock; registra también el método de ejecución usado en el entorno de comprobación.

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

El análisis es determinista: no utiliza simulación ni remuestreo aleatorio; no requiere semilla. Los intervalos son individuales del 95 % y Holm controla una familia de siete pruebas exploratorias documentadas. El código no garantiza representatividad ni independencia.

## Higiene de archivos

`.gitignore` excluye temporales en todas las evaluaciones. Los archivos ya rastreados siguen en Git hasta retirarlos del índice. Para quitar **solo los temporales rastreados**, conservando las copias locales y los entregables de la Formativa 1:

```powershell
./scripts/limpiar_temporales_git.ps1
```

Revisar después `git status`. El script no crea commits ni pull requests.
