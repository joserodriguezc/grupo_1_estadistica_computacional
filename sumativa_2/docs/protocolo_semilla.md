# Protocolo de la semilla — Sumativa 2

La Sumativa 2 usa métodos con aleatoriedad (bootstrap, Montecarlo y otros). Para que los resultados sean reproducibles, todo el trabajo usa **una única semilla**, obtenida de una fuente pública de aleatoriedad y fijada por una regla registrada **antes** de que exista el valor.

## Fuente

**Random UChile**, el Faro de Aleatoriedad (*Randomness Beacon*) de la Universidad de Chile (API `https://random.uchile.cl/beacon/2.1-beta`). Cada minuto genera aleatoriedad "fresca": un número de **512 bits** (`outputValue`). Cada pulso tiene una dirección permanente (`/chain/{cadena}/pulse/{pulso}`), una firma digital y el valor del pulso anterior, por lo que no puede alterarse después de emitido.

### Cómo se genera cada pulso

Según Random UChile, cada minuto se ejecuta el mismo algoritmo en tres partes:

1. **Entropía externa.** Durante los primeros 30 segundos se recolectan datos de fuentes públicas difíciles de predecir. Una fuente es válida si entrega la misma información a cualquier persona que la consulte al mismo tiempo, está a cargo de un organismo confiable sin motivos para sesgarla, refleja un fenómeno aleatorio con un mínimo de entropía en cada emisión, cambia con frecuencia y está disponible la mayor parte del tiempo. Las fuentes actuales son:

   | Fuente | Organismo | Dato que aporta |
   |---|---|---|
   | Sismos | Centro Sismológico Nacional | Último sismo registrado en Chile: fecha (UTC), latitud, longitud, profundidad y magnitud |
   | Radio | Radio Universidad de Chile (transmisión en línea) | Bytes de unos 7 segundos de transmisión, muestreados cada minuto |
   | Ethereum | Blockchain de Ethereum | Hash del último bloque |
   | Buses | Red Movilidad | Posición de cada bus activo en Santiago: fecha (UTC), patente, latitud, longitud, velocidad, recorrido y dirección |

2. **Entropía local.** Un generador de números verdaderamente aleatorios (TRNG), un hardware basado en un proceso cuántico, produce 512 bits cada minuto. Ese valor se usa en el minuto siguiente y queda oculto mediante un esquema criptográfico de compromiso (*commitment*), que impide cambiarlo después.

3. **Criptografía y publicación.** La entropía externa se concatena y pasa por una función verificable de retraso (VDF, *Verifiable Delay Function*), que obliga a esperar un tiempo mínimo para obtener el resultado, sin importar el poder de cómputo disponible. Ese resultado se concatena con la entropía local y con información propia del sistema, se firma digitalmente y se obtiene el valor de 512 bits que se publica como pulso del minuto.

### Por qué sirve para fijar la semilla

Random UChile sostiene que este algoritmo demuestra matemáticamente que ni la propia institución ni ninguna otra entidad puede manipular el valor de forma efectiva ni predecirlo con más de 60 segundos de anticipación. Como la regla de este protocolo se publicó unas 14 horas antes de que se emitiera el pulso fijado, nadie del equipo pudo conocer la semilla ni influir en ella al definirla.

La semilla usa los últimos 32 bits del valor de 512 bits (ver la derivación). Esa reducción no afecta su imprevisibilidad: depende de un valor que nadie conocía de antemano.

Fuente: Random UChile, <https://random.uchile.cl/>.

## Regla (fijada antes de la emisión del pulso)

1. **Pulso:** el primer pulso con `timeStamp` igual o posterior a **2026-10-14T15:00:00.000Z** (12:00 hora de Chile), obtenido con `GET /pulse?timeGE=2026-10-14T15:00:00.000Z`.
2. **Estado del pulso:** se acepta el pulso que entregue la regla cualquiera sea su `statusCode`; el estado solo se registra. Así no queda margen para descartar un pulso y elegir otro.
3. **Derivación:** `SEMILLA = int(outputValue, 16) mod 2**32`. El módulo 2³² hace que la semilla sea un entero válido para NumPy, SciPy, `random` y scikit-learn (`random_state` exige un entero menor que 2³²).
4. **Una sola obtención:** la semilla se obtiene una vez y queda en `docs/registro_semilla.json`. No se vuelve a obtener ni se reemplaza.

Esta regla y el script que la aplica se subieron al repositorio antes de la emisión del pulso. La fecha del commit y del push en GitHub prueban que la semilla no se eligió después de conocer su valor.

## Procedimiento

Desde la raíz del repositorio:

```bash
# Una sola vez, después de 2026-10-14T15:00:00Z; antes de esa hora el script se niega a continuar
uv run python sumativa_2/scripts/semilla_beacon.py obtener

# Cualquier persona, en cualquier momento
uv run python sumativa_2/scripts/semilla_beacon.py verificar
```

`obtener` consulta el pulso, comprueba que cumpla la regla y escribe `docs/registro_semilla.json`. Si el registro ya existe, se detiene sin modificarlo.

`verificar` vuelve a consultar el pulso registrado y comprueba que:

- su `outputValue`, `timeStamp`, índices y firma coinciden con los del *beacon*;
- cumple la regla: su `timeStamp` es igual o posterior al momento fijado y el del pulso anterior es previo;
- está encadenado con el pulso anterior (el valor `previous` del pulso es el `outputValue` del anterior);
- la semilla registrada se deriva de su `outputValue`.

## Uso en el análisis

Toda la aleatoriedad del notebook parte de un único generador creado con la semilla registrada:

```python
import json
import numpy as np

SEMILLA = json.loads((RAIZ / 'docs/registro_semilla.json').read_text(encoding='utf-8'))['semilla']
rng = np.random.default_rng(SEMILLA)
```

- Las funciones de NumPy y SciPy reciben ese generador, por ejemplo `scipy.stats.bootstrap(..., random_state=rng)`.
- Si se necesitan flujos independientes (por ejemplo, un generador por simulación), se derivan con `np.random.SeedSequence(SEMILLA).spawn(k)`.
- No se escribe la semilla a mano en el código ni se usan otras semillas.

## Estado

**Semilla obtenida y congelada.**

| Dato | Valor |
|---|---|
| **SEMILLA** | **1505514103** |
| Pulso | Cadena 2, pulso 1053589: <https://random.uchile.cl/beacon/2.1-beta/chain/2/pulse/1053589> |
| `timeStamp` | 2026-10-14T15:00:00.000Z (el pulso exacto del momento fijado) |
| `statusCode` | 0 (normal) |
| Obtenida | 2026-10-14T18:34:11Z |

La regla se publicó en GitHub el 2026-10-14 a las 00:55 UTC, unas 14 horas antes de la emisión del pulso. El registro completo, con el `outputValue` de 512 bits y la firma del pulso, está en `docs/registro_semilla.json`; `verificar` lo comprueba contra el *beacon*.
