# Estadística Computacional — Grupo 1

## Sumativa 1 — Análisis estadístico de entregas atrasadas

Repositorio del Grupo 1, MCDI501 (Magíster en Ciencia de Datos e Inteligencia Artificial, UNAB). Integrantes: José Ignacio Rodríguez, Yerko Gallardo Miranda y Sebastián Rojas Araya.

## Objetivo y resultados

Se analiza *E-Commerce Shipping Data* (versión 1), con **10.999 registros y 12 columnas**, para describir características asociadas con el atraso de entregas. Se observan **6.563 envíos atrasados (59,67 %) y 4.436 puntuales (40,33 %)**. El diseño es observacional: los hallazgos no demuestran causalidad ni representatividad externa.

El estudio incluye estadísticas descriptivas, cuatro estimaciones con intervalos del 95 %, siete contrastes de hipótesis ajustados por Holm y dos anexos dentro del **mismo informe PDF**: figuras complementarias y justificación de técnicas estadísticas.

## Archivos de la entrega

- `sumativa_1/notebooks/sumativa_1.ipynb`: notebook ejecutable (96 celdas, 47 de código).
- `sumativa_1/docs/informe/informe_sumativa1.tex`: **único archivo fuente LaTeX**, con ambos anexos integrados; no requiere otros `.tex`.
- `sumativa_1/docs/informe/informe_sumativa1.pdf`: informe unificado, **21 páginas en total**, incluidos los anexos.
- `sumativa_1/outputs/figuras/`: figuras utilizadas tanto en el cuerpo principal como en los anexos; **sin subcarpeta `anexos`**.
- `sumativa_1/outputs/tablas/`: resultados cuantitativos, pruebas y metadatos de ejecución.
- `sumativa_1/docs/protocolo_analisis.md`: diseño estadístico final de esta evaluación.
- `sumativa_1/docs/fuente_datos.md`, `sumativa_1/docs/ficha_descriptiva.md`, `sumativa_1/docs/diccionario_variables.csv`: documentación del conjunto de datos.
- `sumativa_1/docs/registro_fuente.json`: metadatos de obtención, tamaños y huellas SHA-256 del CSV.
- `sumativa_1/scripts/verificar_fuente.py`: verifica la integridad del CSV contra el registro; `sumativa_1/scripts/generar_diccionario.py`: genera `diccionario_variables.csv`.

## Reproducir desde la raíz del repositorio

Se requiere Python compatible con `.python-version`, `uv`, Jupyter y una instalación LaTeX con `latexmk` y los paquetes utilizados por el informe.

```bash
uv sync --locked
uv run jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=180 sumativa_1/notebooks/sumativa_1.ipynb
cd sumativa_1/docs/informe
latexmk -pdf -interaction=nonstopmode -halt-on-error informe_sumativa1.tex
```

En VS Code también se puede abrir el notebook, seleccionar `.venv` y ejecutar todas las celdas desde un kernel reiniciado. Compilar **solo `informe_sumativa1.tex`**, desde su directorio para conservar las rutas relativas `../../outputs/figuras/`.

## Criterios de interpretación

La variable `entrega_atrasada` se codifica como `1 = atrasada`, `0 = puntual`. Las diferencias entre grupos se calculan como **atrasadas menos puntuales**. El descuento conserva unidades originales no documentadas. Las tasas y pruebas son descriptivas/inferenciales condicionadas a supuestos no verificables completamente, especialmente independencia y representatividad. El umbral de descuento mayor que 10 es exploratorio y requiere validación externa.

Fuente: [Gopalani (2021), E-Commerce Shipping Data (Kaggle)](https://www.kaggle.com/datasets/prachi13/customer-analytics).

**Organización:** este `README.md` describe la Sumativa 1; el de la raíz describe el repositorio y el de `formativa_1/` corresponde a la entrega histórica. Los documentos metodológicos permanecen en `sumativa_1/docs/`.

