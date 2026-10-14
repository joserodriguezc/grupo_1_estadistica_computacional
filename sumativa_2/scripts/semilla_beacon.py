"""Obtiene y verifica la semilla de la Sumativa 2 desde el beacon de aleatoriedad de la Universidad de Chile.

Regla fijada antes de que se emita el pulso (ver docs/protocolo_semilla.md):
    pulso = primer pulso con timeStamp >= MOMENTO_FIJADO  (GET /pulse?timeGE=MOMENTO_FIJADO)
    SEMILLA = int(outputValue, 16) mod 2**32

Uso, desde la raíz del repositorio:
    uv run python sumativa_2/scripts/semilla_beacon.py obtener     # una sola vez, después del momento fijado
    uv run python sumativa_2/scripts/semilla_beacon.py verificar   # cualquier persona, en cualquier momento
    uv run python sumativa_2/scripts/semilla_beacon.py probar 2026-10-13T12:00:00.000Z   # ensayo sin escribir

Solo usa la biblioteca estándar de Python.
"""
import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = "https://random.uchile.cl/beacon/2.1-beta"
MOMENTO_FIJADO = "2026-10-14T15:00:00.000Z"
MODULO = 2**32
RAIZ = Path(__file__).resolve().parents[1]
REGISTRO = RAIZ / "docs/registro_semilla.json"


def leer(url):
    pedido = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(pedido, timeout=30) as r:
        return json.load(r)["pulse"]


def instante(ts):
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def pulso(cadena, indice):
    return leer(f"{BASE}/chain/{cadena}/pulse/{indice}")


def semilla_de(output_value):
    return int(output_value, 16) % MODULO


def buscar(momento):
    """Primer pulso con timeStamp >= momento, mediante el parámetro timeGE de la API."""
    try:
        return leer(f"{BASE}/pulse?timeGE={momento}")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            sys.exit(f"Aún no se emite un pulso con timeStamp >= {momento} (el beacon responde 404).")
        raise


def comprobar_regla(p, objetivo):
    """El pulso cumple la regla y está encadenado con su predecesor."""
    assert instante(p["timeStamp"]) >= objetivo, "El pulso es anterior al momento fijado."
    previo = pulso(p["chainIndex"], p["pulseIndex"] - 1)
    assert instante(previo["timeStamp"]) < objetivo, "Existe un pulso anterior que también cumple la regla."
    enlace = {v["type"]: v["value"] for v in p.get("listValues", [])}
    assert enlace.get("previous") == previo["outputValue"], "El pulso no está encadenado con su predecesor."
    return previo


def registro_de(p):
    return {
        "proposito": "Semilla única de la Sumativa 2 (bootstrap, Montecarlo y otros métodos aleatorios).",
        "fuente": "Random UChile, beacon de aleatoriedad de la Universidad de Chile",
        "api": BASE,
        "regla": "Primer pulso con timeStamp >= momento_fijado_utc (consulta /pulse?timeGE=momento_fijado_utc)",
        "momento_fijado_utc": MOMENTO_FIJADO,
        "derivacion": "semilla = int(outputValue, 16) mod 2**32",
        "pulso": {k: p[k] for k in ("uri", "version", "chainIndex", "pulseIndex", "timeStamp", "statusCode",
                                    "certificateId", "outputValue", "signatureValue")},
        "obtenido_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "semilla": semilla_de(p["outputValue"]),
    }


def obtener():
    if REGISTRO.exists():
        sys.exit(f"{REGISTRO} ya existe: la semilla es definitiva y no se vuelve a obtener. Use 'verificar'.")
    p = buscar(MOMENTO_FIJADO)
    comprobar_regla(p, instante(MOMENTO_FIJADO))
    if p["statusCode"] != 0:
        print(f"Aviso: el pulso tiene statusCode {p['statusCode']} (0 = normal).")
    REGISTRO.write_text(json.dumps(registro_de(p), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Pulso {p['uri']} ({p['timeStamp']})")
    print(f"SEMILLA = {semilla_de(p['outputValue'])}  -> registrada en {REGISTRO.relative_to(RAIZ.parent)}")


def verificar():
    r = json.loads(REGISTRO.read_text(encoding="utf-8"))
    p = leer(r["pulso"]["uri"])
    for campo in ("chainIndex", "pulseIndex", "timeStamp", "outputValue", "signatureValue"):
        assert p[campo] == r["pulso"][campo], f"{campo} no coincide con el beacon."
    assert r["momento_fijado_utc"] == MOMENTO_FIJADO, "El momento fijado del registro difiere del script."
    comprobar_regla(p, instante(MOMENTO_FIJADO))
    assert semilla_de(p["outputValue"]) == r["semilla"], "La semilla no corresponde al outputValue."
    print(f"Conforme: el pulso {p['uri']} coincide con el beacon, cumple la regla y produce SEMILLA = {r['semilla']}.")


def probar(momento):
    p = buscar(momento)
    previo = comprobar_regla(p, instante(momento))
    print(f"Momento {momento}: pulso {p['pulseIndex']} ({p['timeStamp']}), anterior {previo['timeStamp']}, "
          f"semilla {semilla_de(p['outputValue'])} (ensayo: no se escribe nada).")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="accion", required=True)
    sub.add_parser("obtener")
    sub.add_parser("verificar")
    sub.add_parser("probar").add_argument("momento", help="ISO 8601 en UTC, p. ej. 2026-10-13T12:00:00.000Z")
    a = ap.parse_args()
    {"obtener": obtener, "verificar": verificar}.get(a.accion, lambda: probar(a.momento))()
