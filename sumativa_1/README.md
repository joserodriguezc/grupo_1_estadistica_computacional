# Evaluación Sumativa 1

Análisis exploratorio e inferencial de entregas atrasadas en comercio electrónico.

## Archivos principales

- [Notebook ejecutado](notebooks/sumativa_1.ipynb).
- [Informe PDF](docs/informe/informe_sumativa1.pdf): 8 páginas totales, incluida la portada.
- [Fuente LaTeX](docs/informe/informe_sumativa1.tex).
- [Diccionario](docs/diccionario_variables.csv) y [ficha descriptiva](docs/ficha_descriptiva.md).
- [Protocolo](docs/protocolo_analisis.md).
- [Matriz de correcciones](docs/cierre_sumativa1.md).
- [Verificación](docs/verificacion_ejecucion.md).

## Reproducir

Desde la raíz del repositorio:

```powershell
uv sync --locked
uv run jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=180 sumativa_1/notebooks/sumativa_1.ipynb
Push-Location sumativa_1/docs/informe
latexmk -pdf -interaction=nonstopmode -halt-on-error informe_sumativa1.tex
Pop-Location
```

Reiniciar el kernel antes de ejecutar manualmente. `uv.lock` fija las dependencias del equipo. Las copias del entorno dentro de la evaluación permiten identificar su estructura; los comandos anteriores usan el entorno de la raíz.

## Secuencia del análisis

1. Carga y clasificación por significado y escala.
2. Auditoría de tipos, nulos, dominios, duplicados y extremos.
3. Centro, dispersión, asimetría y exceso de curtosis; frecuencias y relaciones.
4. Cuatro estimaciones globales con IC normal del 95 % y supuestos.
5. Tres contrastes principales y cuatro complementarios; Holm conjunto.
6. Síntesis, segmentos a auditar y registro de versiones y SHA-256.

## Resultados y métodos

`descriptiva_cuantitativas.csv` incorpora forma; `correlacion_spearman.csv` contiene la matriz completa; `estimaciones.csv` e `intervalos_confianza.csv` incluyen n; `contrastes_holm_7.csv` es la consolidación única. `segmento_descuento.csv` documenta las proporciones e IC Wilson de los grupos con descuento > 10 y <= 10.

T01: chi-cuadrado modalidad. T02: Welch peso. T03: Welch descuento, añadido tras EDA. E1: Mann-Whitney peso. E2: z importancia alta. E3: z descuento > 10. E4: Welch costo. No se presenta el cambio de T03 o el umbral 10 como preespecificado. Holm no elimina selección exploratoria, dependencia ni confusión.

Los p exportados como cero reflejan precisión finita y no probabilidad matemática nula. El IC normal de diferencia de proporciones en E3 se documenta con cautela por la proporción 1; el informe usa también Wilson por grupo. No se requieren semillas porque no hay pasos aleatorios.

## Límites

No se documentan empresa, período, selección ni dependencia. Descuento no equivale necesariamente a porcentaje o moneda. Los resultados orientan una investigación operacional, no cambios causales de transporte o política comercial.
