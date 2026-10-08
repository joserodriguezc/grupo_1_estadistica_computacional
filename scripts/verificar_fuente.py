"""Verifica data/raw/ecommerce_shipping.csv (Train.csv renombrado) contra docs/registro_fuente.json.

No modifica archivos. Usa solo la biblioteca estándar.
"""

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path


def leer_csv(contenido):
    lector = csv.reader(io.StringIO(contenido.decode("utf-8-sig"), newline=""))
    encabezado = next(lector)
    filas = list(lector)
    if any(len(fila) != len(encabezado) for fila in filas):
        raise ValueError("El CSV contiene filas con cantidad de campos inconsistente.")
    return encabezado, filas


def forma_de_bytes(huella, tamano, registro):
    """Identifica si los bytes son los originales (CRLF) o la forma normalizada LF."""
    if huella == registro["sha256"] and tamano == registro["size_bytes"]:
        return "original_crlf"
    if (
        huella == registro["sha256_lf_normalized"]
        and tamano == registro["size_bytes_lf_normalized"]
    ):
        return "normalizada_lf"
    return None


def main():
    raiz = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--archivo", type=Path, default=raiz / "data/raw/ecommerce_shipping.csv"
    )
    parser.add_argument("--registro", type=Path, default=raiz / "docs/registro_fuente.json")
    parser.add_argument(
        "--comparar", type=Path, help="CSV para comparar, p. ej. un Train.csv recién descargado."
    )
    args = parser.parse_args()

    registro = json.loads(args.registro.read_text(encoding="utf-8"))["file"]
    contenido = args.archivo.read_bytes()
    columnas, filas = leer_csv(contenido)
    huella = hashlib.sha256(contenido).hexdigest()
    forma = forma_de_bytes(huella, len(contenido), registro)
    indice_id = columnas.index("ID")
    verificaciones = {
        "sha256_y_tamano": forma is not None,
        "columnas_y_orden": columnas == registro["columns"],
        "filas": len(filas) == registro["rows"],
        "numero_columnas": len(columnas) == registro["column_count"],
        "celdas_vacias": sum(v == "" for fila in filas for v in fila)
        == registro["empty_cells"],
        "ids_distintos": len({fila[indice_id] for fila in filas})
        == registro["unique_id_count"],
    }
    resultado = {
        "archivo": str(args.archivo),
        "sha256": huella,
        "tamano_bytes": len(contenido),
        "forma_bytes": forma or "no_coincide_con_registro",
        "registros": len(filas),
        "columnas": len(columnas),
        "verificaciones": verificaciones,
    }
    if args.comparar:
        otro = args.comparar.read_bytes()
        otras_columnas, otras_filas = leer_csv(otro)
        equivalente = columnas == otras_columnas and filas == otras_filas
        resultado["comparacion"] = {
            "archivo": str(args.comparar),
            "sha256": hashlib.sha256(otro).hexdigest(),
            "tamano_bytes": len(otro),
            "bytes_identicos": contenido == otro,
            "contenido_tabular_identico": equivalente,
            "identicos_normalizando_crlf": contenido.replace(b"\r\n", b"\n")
            == otro.replace(b"\r\n", b"\n"),
        }
        verificaciones["comparacion_tabular"] = equivalente
    resultado["conforme"] = all(verificaciones.values())
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return 0 if resultado["conforme"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
