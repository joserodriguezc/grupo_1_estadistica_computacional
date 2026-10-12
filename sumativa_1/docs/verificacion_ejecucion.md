# Verificación de ejecución

## Entorno

Se instaló el entorno declarado con `uv sync --locked --python 3.14 --link-mode copy`, conservando `pyproject.toml` y `uv.lock` de la instantánea del repositorio.

Python: **3.14.8**. Paquetes: numpy 2.5.3, pandas 3.0.6, scipy 1.18.1, statsmodels 0.15.0, matplotlib 3.11.2, seaborn 0.13.2.

## Ejecución del notebook

Se ejecutaron **47 celdas de código en orden, en un intérprete nuevo**, sin reutilizar variables de una ejecución anterior. Por la restricción de sockets del entorno de comprobación se utilizó la API de IPython en proceso, conservando salidas y contadores válidos en el notebook. El README incluye el procedimiento habitual `jupyter nbconvert --execute` para el equipo. No se verificó una sesión TCP de Jupyter en este entorno.

## Controles independientes

- Dimensiones originales: 10.999 × 12.
- Resultado: 6.563 atrasadas y 4.436 puntuales.
- SHA-256 sin cambios: `7f4d81e18f762de35c411f8003fe4a0565dd886a50e311729041c1aa41b076f6`.
- Cuatro intervalos recalculados desde el CSV; n = 10.999 en cada fila.
- Siete p ajustados por Holm recalculados por ordenación y máximo acumulado; coinciden con la exportación.
- T03 identifica descuento y E4 costo en todas las salidas consolidadas.
- Segmentos: 2.647 registros con descuento > 10 y 8.352 con descuento <= 10.
- Notebook válido y sin salidas de tipo error.
- Fuentes LaTeX compiladas con `latexmk -pdf` y referencias resueltas.
- PDF de 8 páginas totales; inspección visual de todas las páginas, sin recortes ni tablas rotas.

La comprobación reproduce resultados del análisis; no demuestra independencia, representatividad ni causalidad. La ejecución en el equipo local sigue los comandos del README y debe conservar el mismo archivo y lock.
