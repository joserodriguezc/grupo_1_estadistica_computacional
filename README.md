# grupo_1_estadistica_computacional

Repositorio del Grupo 1 — MCDI501 Estadística Computacional para la Toma de Decisiones.
Cada evaluación se entrega en su propia carpeta, autocontenida (datos, notebook, salidas e informe):

| Carpeta | Entregable | Notebook | Informe |
|---|---|---|---|
| `formativa_1/` | Evaluación Formativa 1 (congelada, no modificar) | `notebooks/formativa_1.ipynb` | `docs/informe/informe_formativa1.pdf` |
| `sumativa_1/` | Evaluación Sumativa 1 (formativa + mejoras de visualización) | `notebooks/sumativa_1.ipynb` | `docs/informe/informe_sumativa1.pdf` |

El entorno (`pyproject.toml`, `uv.lock`) es común y se instala desde la raíz con `uv sync`.
Cada carpeta incluye su propia copia de `pyproject.toml`, que el notebook usa para ubicar su raíz.

Para regenerar la sumativa:

```bash
uv run jupyter nbconvert --to notebook --execute --inplace sumativa_1/notebooks/sumativa_1.ipynb
cd sumativa_1/docs/informe && latexmk -pdf informe_sumativa1.tex
```
