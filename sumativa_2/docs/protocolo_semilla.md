# Protocolo de la semilla — Sumativa 2

La Sumativa 2 usa métodos con aleatoriedad (bootstrap, Montecarlo y otros). Para que los resultados sean reproducibles, todo el trabajo usa **una única semilla**, obtenida de una fuente pública de aleatoriedad y fijada por una regla registrada **antes** de que exista el valor.

## Fuente

**Random UChile**, el *beacon* de aleatoriedad de la Universidad de Chile (API `https://random.uchile.cl/beacon/2.1-beta`). Emite un pulso cada 60 segundos. Cada pulso tiene una dirección permanente (`/chain/{cadena}/pulse/{pulso}`), un valor aleatorio de 512 bits (`outputValue`), una firma digital y el valor del pulso anterior, por lo que no puede alterarse después de emitido.

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

**Pendiente de obtención.** El pulso fijado se emite el 2026-10-14 a las 15:00 UTC. Después de esa hora se ejecuta `obtener` y se registra la semilla en un commit separado.
