# Fuente de datos

## Identificación y responsabilidad

**Proyecto:** Grupo 1 de Estadística computacional para la toma de decisiones.  
**Tarea:** Obtener y registrar la fuente de datos.  
**Responsable de ejecución:** José Ignacio Rodríguez.  
**Revisor:** Sebastián Rojas.  
**Estado:** Obtención y verificaciones iniciales completadas; revisión de Sebastián pendiente.

| Campo | Registro |
|---|---|
| Dataset | E-Commerce Shipping Data |
| Publicadora | Prachi Gopalani (`prachi13`) |
| Plataforma | Kaggle |
| Identificador | `prachi13/customer-analytics` |
| ID de Kaggle | 1176727 |
| Fuente | https://www.kaggle.com/datasets/prachi13/customer-analytics |
| Versión obtenida | 1, Initial release |
| Publicación de la versión | 23-02-2021, 12:01:47.463 UTC |
| Descarga completada | 2026-10-07T22:09:30.767294-03:00 (hora de Chile) |
| Archivo original (Kaggle) | `Train.csv` |
| Archivo en el proyecto | `ecommerce_shipping.csv` (renombrado desde `Train.csv`, sin modificar sus bytes) |
| Ubicación | `data/raw/ecommerce_shipping.csv` |
| Tamaño del CSV | 440,462 bytes |
| Dimensiones | 10.999 registros y 12 columnas; encabezado excluido del conteo de registros |
| Codificación | UTF-8 con BOM |
| Saltos de línea originales | CRLF |

La publicadora describe una empresa internacional de comercio electrónico que vende productos electrónicos. La documentación no identifica la empresa, el período de observación ni el mecanismo de selección. Se distingue la autoría de la publicación de la procedencia empresarial, que no está corroborada.

## Integridad del archivo original

SHA-256 de `Train.csv`, igual al de `data/raw/ecommerce_shipping.csv` en su forma original:

```text
dcdc3fd8f0507ec400174ef70d88d634321cc2ce8f4ea11bf4e8c847fdd325b3
```

Los bytes se extrajeron directamente del miembro `Train.csv` del ZIP descargado y el archivo solo se renombró a `ecommerce_shipping.csv`. No se abrió y guardó el archivo en Excel, no se reescribió con pandas y no se cambiaron delimitadores, codificación, encabezados, orden de filas ni saltos de línea.

El tamaño y la huella corresponden al CSV extraído, no al ZIP. El registro `docs/registro_fuente.json` también conserva el tamaño y SHA-256 del ZIP, la URL de descarga y la fecha en UTC.

## Verificación inicial

| Control | Resultado |
|---|---|
| Lectura | CSV legible con `utf-8-sig` y separador coma |
| Registros | 10.999 |
| Columnas | 12 |
| Celdas vacías detectadas por el lector CSV | 0 |
| IDs distintos | 10.999 |
| Categorías de bodega | A, B, C, D y F |
| Comparación con la verificación del plan | Coinciden dimensiones, ausencia de celdas vacías y unicidad de ID |

La ausencia de celdas vacías no descarta códigos especiales de ausencia ni sustituye la auditoría de calidad de datos (tipos, dominios y rangos). La unicidad de ID no demuestra independencia ni ausencia de clientes repetidos.

Columnas originales, en su orden:

```text
ID, Warehouse_block, Mode_of_Shipment, Customer_care_calls, Customer_rating, Cost_of_the_Product, Prior_purchases, Product_importance, Gender, Discount_offered, Weight_in_gms, Reached.on.Time_Y.N
```

La descripción de Kaggle confirma que `Reached.on.Time_Y.N` tiene **1 = no llegó a tiempo** y **0 = llegó a tiempo**. También declara costo en USD y peso en gramos. La unidad del descuento no está especificada.

La descripción enumera bodegas A–E, mientras el archivo contiene A, B, C, D y F. Se documenta la discrepancia; no se reemplaza F por E.

## Renombre y almacenamiento en Git

En el proyecto, `Train.csv` se renombró a `ecommerce_shipping.csv` (commit `4664077`). El renombre no alteró el contenido: la copia de trabajo en Windows tiene el mismo tamaño (440.462 bytes) y el mismo SHA-256 que el original de Kaggle.

Git almacena el archivo con saltos de línea LF porque el repositorio se trabajó con `core.autocrlf=true`, que convierte CRLF a LF al hacer commit. Por eso el archivo puede tener dos formas de bytes según el equipo que lo descargue:

| Forma | Dónde aparece | Saltos de línea | Tamaño | SHA-256 |
|---|---|---|---|---|
| Original | Kaggle; copia de trabajo en Windows con `autocrlf=true` | CRLF | 440.462 bytes | `dcdc3fd8…dd325b3` |
| Normalizada | Blob en Git; copia de trabajo en macOS/Linux o sin `autocrlf` | LF | 429.462 bytes | `7f4d81e1…1b076f6` |

SHA-256 completo de la forma normalizada:

```text
7f4d81e18f762de35c411f8003fe4a0565dd886a50e311729041c1aa41b076f6
```

La diferencia de 11.000 bytes corresponde a un `` por cada una de las 11.000 líneas, incluido el encabezado. Ambas formas tienen los mismos encabezados, orden de filas y valores, y el script de verificación acepta las dos e informa cuál encontró.

Instantánea consultada: árbol `f8de61f944040079a7655297ff791cd815675429`; blob del CSV `3a19806eccf1bcb198feeb28ac07cda12a7e1a2d`.

## Condiciones de uso y atribución

La licencia declarada por Kaggle es **Other (specified in description)**. La descripción consultada al obtener la versión 1 indica que la publicadora pone los datos a disposición de usuarios de Kaggle y menciona un proyecto en GitHub, pero no incorpora una licencia estándar ni términos explícitos de redistribución.

No se atribuirá al dataset una licencia MIT, CC0 o Creative Commons que no esté declarada. La disponibilidad para descarga y la atribución no bastan para confirmar autorización de redistribución.

Para la entrega académica se citará la fuente y se documentará la obtención. El CSV ya está versionado en el repositorio como `data/raw/ecommerce_shipping.csv`. Si el repositorio es público, su publicación queda sujeta a la misma condición no confirmada; este entregable no modifica ni elimina ese archivo.

Referencia propuesta:

> Gopalani, P. (2021). *E-Commerce Shipping Data* (versión 1) [Conjunto de datos]. Kaggle. https://www.kaggle.com/datasets/prachi13/customer-analytics

## Procedimiento reproducible de obtención

1. Abrir la página oficial y verificar dataset, publicadora y versión.
2. Descargar la versión 1 usando la URL fijada a continuación.
3. Extraer `Train.csv` mediante una herramienta ZIP, sin abrirlo y volver a guardarlo como CSV.
4. Renombrarlo y conservarlo como `data/raw/ecommerce_shipping.csv`.
5. Comparar tamaño y SHA-256 con este registro.
6. Registrar una nueva fecha de descarga para cada obtención posterior. No reutilizar la fecha de esta adquisición como propia.

URL fijada a versión 1:

```text
https://www.kaggle.com/api/v1/datasets/download/prachi13/customer-analytics?datasetVersionNumber=1
```

Ejemplo en PowerShell, desde la raíz del proyecto:

```powershell
$y01Destino = Join-Path (Get-Location) "data/raw/ecommerce_shipping.csv"
if (Test-Path $y01Destino) {
    throw "ecommerce_shipping.csv ya existe. Verifica su huella antes de reemplazarlo."
}
$y01Temporal = Join-Path ([System.IO.Path]::GetTempPath()) ([guid]::NewGuid().ToString())
New-Item -ItemType Directory -Path $y01Temporal | Out-Null
$y01Zip = Join-Path $y01Temporal "dataset_v1.zip"
$y01Extraido = Join-Path $y01Temporal "extraido"
Invoke-WebRequest -Uri "https://www.kaggle.com/api/v1/datasets/download/prachi13/customer-analytics?datasetVersionNumber=1" -OutFile $y01Zip
Expand-Archive -LiteralPath $y01Zip -DestinationPath $y01Extraido
New-Item -ItemType Directory -Force -Path "data/raw" | Out-Null
Copy-Item -LiteralPath (Join-Path $y01Extraido "Train.csv") -Destination $y01Destino
Get-FileHash -LiteralPath $y01Destino -Algorithm SHA256
```

Si Kaggle solicita autenticación, descargar la versión 1 desde la página oficial con la cuenta propia y repetir la verificación. No sustituir por copias de terceros.

Verificación reproducible con el script incluido, desde la raíz del proyecto:

```powershell
uv run python scripts/verificar_fuente.py
```

Comparación opcional con un `Train.csv` recién descargado de Kaggle (ruta de ejemplo):

```powershell
uv run python scripts/verificar_fuente.py --comparar ruta/a/Train.csv
```

El script usa únicamente la biblioteca estándar de Python y no modifica los archivos.

## Conservación y coordinación con el análisis

- `data/raw/ecommerce_shipping.csv`: `Train.csv` renombrado; entrada del análisis. No se edita.
- `docs/fuente_datos.md`: este documento.
- `docs/registro_fuente.json`: metadatos, huellas (original y normalizada LF) y resultados de la adquisición.
- `scripts/verificar_fuente.py`: verificación de integridad y comparación opcional.

Para que Git conserve los bytes originales (CRLF) en todos los equipos, se puede añadir a `.gitattributes`:

```gitattributes
/data/raw/ecommerce_shipping.csv -text
```

y volver a registrar el archivo con `git add --renormalize data/raw/ecommerce_shipping.csv`. Después, el blob tendría el SHA-256 original. Verificar la huella tras el cambio.

## Criterios de aceptación

- [x] Fuente oficial y publicadora identificadas.
- [x] Versión 1 verificada y descargada.
- [x] Archivo legible y dimensiones 10.999 × 12 reproducidas.
- [x] Bytes originales conservados y SHA-256 calculado.
- [x] Fecha, tamaño, nombre y procedimiento registrados.
- [x] Condición de licencia revisada y limitación documentada.
- [x] Renombre a `ecommerce_shipping.csv` documentado y equivalencia de bytes verificada.
- [x] Diferencia CRLF/LF explicada por `core.autocrlf` de Git.
- [ ] Sebastián revisa la evidencia y confirma que el análisis usará `data/raw/ecommerce_shipping.csv`.

Los criterios técnicos de obtención se cumplen. La revisión de Sebastián y la aclaración de los permisos de redistribución permanecen pendientes; no se afirma autorización de publicación del CSV.
