# Cierre de la Sumativa 1

Base revisada: commit `3677f40739f87d82f3d6c2004a4eb719b6f6eae4` del repositorio del equipo. Se atiende la retroalimentación de Formativa 1 (79/99), sin modificar sus entregables históricos. Referencia de alcance: plantilla de Sumativa 1 del profesor, máximo 8 páginas sin anexos, al menos tres medias numéricas con IC y dos pruebas pertinentes. El informe corregido tiene 8 páginas totales, incluida portada, cuatro estimaciones y siete pruebas.

## Matriz de respuesta a la retroalimentación

| Criterio | Observación | Corrección y evidencia |
|---|---|---|
| Descriptiva | Asimetría y curtosis en Tabla 2 | Ambas incluidas en Tabla 2; notebook usa `stats.skew(bias=False)` y `stats.kurtosis(fisher=True,bias=False)`; CSV con precisión completa |
| Descriptiva | Leer la matriz con valores concretos | Figura 4 y texto: peso–descuento −0,316; llamadas–costo 0,294; llamadas–compras 0,273; costo–compras 0,194; matriz exportada |
| Estimación | Explicar el sentido del 95 % | Sección 3 y notebook: cobertura del procedimiento en muestreo repetido; parámetro fijo, no probabilidad posterior ni rango del 95 % de envíos |
| Estimación | n en Tabla 3 | Cuatro filas con n = 10.999 y unidades; resultados verificados contra el CSV |
| Hipótesis | E1–E3 solo en tabla | Sección 4.4: H0/H1, procedimiento, estadístico, n de grupos, resultado y limitaciones de E1–E4 |
| Hipótesis | Cambio de T03 tras mirar los datos | Protocolo, notebook e informe reconocen exploración; T03 descuento y E4 costo, con una familia de siete para Holm |
| Documentación | README insuficiente | README de raíz y de sumativa explican estructura, requisitos, carga, ejecución, compilación y límites |
| Documentación | Temporales de LaTeX rastreados | `.gitignore` general y script PowerShell para retirarlos del índice sin borrar copias ni análisis de Formativa 1; paquete sin temporales |
| Documentación | Funciones scipy no identificadas | Sección 6 detalla carga, descriptiva, Spearman, IC, χ², Welch, Mann-Whitney, z, Cramér y Holm; notebook registra versiones |
| Interpretación | Cifras en conclusiones | Sección 5: atraso 59,67 %; peso 3.272,64 frente a 4.168,67 g; descuento 18,66 frente a 5,55 |
| Interpretación | Recomendación concreta | Auditar 2.647 registros con descuento > 10, todos atrasados; comparar con 8.352 de descuento <= 10, atraso 46,89 %; verificar temporalidad y campañas |
| Presentación | Decimales ambiguos | Comas protegidas en fórmulas y espacios finos para millares; revisión del PDF compilado |
| Presentación | Sección de foro repetía la consigna | Se elimina el enunciado de foro del informe sumativo; no se inventan nuevas participaciones |
| Presentación | Figuras sin referencia | Las seis figuras incluidas están citadas por número en el cuerpo |

## Otras correcciones de coherencia

- Clasificación semántica en lugar de identificar variables por cardinalidad.
- La franja de peso (2.000, 4.000] g tiene una puntual: separación casi completa, no completa.
- No se interpreta Mann-Whitney como contraste exclusivo de medianas sin supuestos de forma.
- p = 0 de máquina se identifica como subdesbordamiento, sin inventar un límite como 10^-300.
- IC Wilson [99,86 %; 100 %] para el grupo con descuento > 10; cautela con el IC Wald de la diferencia.
- El 95 % y la multiplicidad son distintos: los IC del informe son individuales y no simultáneos.

## Integración en el repositorio

El paquete se extrajo y preparó a partir de la instantánea indicada. Copiar sus archivos sobre la raíz del repositorio y revisar el diff antes de confirmar cambios. No incluye los datos crudos: conservar `sumativa_1/data/raw/ecommerce_shipping.csv` existente, cuya huella se verifica.

Retirar la antigua exportación redundante, si existe:

```powershell
Remove-Item sumativa_1/outputs/tablas/contrastes_holm_7_exploratorio.csv -ErrorAction SilentlyContinue
```

Para retirar los temporales ya rastreados del índice, conservando los archivos locales:

```powershell
./scripts/limpiar_temporales_git.ps1
git status
```

Este paso debe realizarse al incorporar el paquete; cambiar `.gitignore` no lo sustituye. El script no modifica datos, notebooks, informes PDF ni fuentes .tex, y no crea commits ni PR.

La evaluación final corresponde al docente; la matriz identifica evidencia de corrección y no garantiza una calificación.
