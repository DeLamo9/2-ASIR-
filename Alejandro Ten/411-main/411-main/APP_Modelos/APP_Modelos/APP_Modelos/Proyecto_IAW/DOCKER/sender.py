import os
import sys
import time
import json
import logging
from typing import Any, Dict, List

import psycopg2
import psycopg2.extras
import requests


# ---------------------------
# Config
# ---------------------------
ENDPOINT = (os.getenv("IMP411_ENDPOINT", "http://web:8000/api/impuestos").rstrip("/") + "/")
INTERVAL_SEC = int(os.getenv("IMP411_INTERVAL_SEC", "30"))
BATCH_SIZE = int(os.getenv("IMP411_BATCH", "100"))

DB_HOST = os.getenv("POSTGRES_HOST", "db")
DB_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
DB_NAME = os.getenv("POSTGRES_DB", "proyecto")
DB_USER = os.getenv("POSTGRES_USER", "proyecto")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "proyecto")

HTTP_TIMEOUT = 15
RETRIES = 2  # nº reintentos por fila


# ---------------------------
# Logging
# ---------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [sender] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("imp411-sender")


# ---------------------------
# DB helpers
# ---------------------------
def get_conn():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )

SQL_SELECT_PENDING = """
SELECT id, cif_empresa, nif_cliente, numero_impuesto, datos
FROM imp411.impuesto_outbox_raw
WHERE sent = FALSE
ORDER BY id
LIMIT %s
FOR UPDATE SKIP LOCKED;
"""

SQL_MARK_SENT = """
UPDATE imp411.impuesto_outbox_raw
SET sent = TRUE, sent_at = NOW()
WHERE id = ANY(%s::bigint[]);
"""


# ---------------------------
# Utils
# ---------------------------
def to_json_obj(value: Any) -> Dict[str, Any]:
    """
    Acepta JSONB (dict) o TEXT (str) y devuelve dict.
    Si no se puede parsear, lanza ValueError.
    """
    if isinstance(value, dict):
        return value
    if value is None:
        return {}
    # psycopg2 puede traer memoryview/bytes
    if isinstance(value, (bytes, bytearray, memoryview)):
        value = bytes(value).decode("utf-8", errors="replace")
    if isinstance(value, str):
        s = value.strip()
        if not s:
            return {}
        try:
            parsed = json.loads(s)
        except json.JSONDecodeError as e:
            raise ValueError(f"datos no es JSON válido: {e.msg}") from e
        if isinstance(parsed, dict):
            return parsed
        else:
            # si el texto contiene un array, lo envolvemos en objeto
            return {"_": parsed}
    # último intento: castear a str y parsear
    try:
        parsed = json.loads(str(value))
        return parsed if isinstance(parsed, dict) else {"_": parsed}
    except Exception as e:
        raise ValueError(f"tipo de datos no parseable a JSON: {type(value)} ({e})")


# ---------------------------
# HTTP
# ---------------------------
def post_one(payload: dict) -> bool:
    for attempt in range(1, RETRIES + 2):
        try:
            r = requests.post(
                ENDPOINT,
                json=payload,
                timeout=HTTP_TIMEOUT,
                headers={"Accept": "application/json"},
            )
            if 200 <= r.status_code < 300:
                return True
            log.warning("API %s respondió %s: %s", ENDPOINT, r.status_code, r.text[:500])
        except requests.RequestException as e:
            log.warning("Error HTTP intento %s/%s: %s", attempt, RETRIES + 1, e)
        time.sleep(1.5 * attempt)
    return False


# ---------------------------
# Loop
# ---------------------------
def tick_once():
    sent_ids: List[int] = []

    with get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SET SESSION CHARACTERISTICS AS TRANSACTION READ WRITE;")
            cur.execute(SQL_SELECT_PENDING, (BATCH_SIZE,))
            rows = cur.fetchall()

            if not rows:
                log.info("sin pendientes")
                return

            ok, fail = 0, 0
            for row in rows:
                try:
                    datos_obj = to_json_obj(row["datos"])
                except ValueError as e:
                    fail += 1
                    log.warning("id %s descartado: %s", row["id"], e)
                    continue

                payload = {
                     "numero_impuesto": str(row["numero_impuesto"]),
                     "cif_empresa":     row["cif_empresa"],
                     "nif_cliente":     row["nif_cliente"],
                     "total_a_recaudar": datos_obj.get("cuota_tributaria", 0),  # ← aquí fuera de "datos"
                     "datos":            datos_obj
                }


                if post_one(payload):
                    sent_ids.append(row["id"])
                    ok += 1
                else:
                    fail += 1
                    log.warning("fallo al enviar %s/%s/%s (id %s)",
                                row["cif_empresa"], row["nif_cliente"], row["numero_impuesto"], row["id"])

            if sent_ids:
                cur.execute(SQL_MARK_SENT, (sent_ids,))
                log.info("marcados como sent: %s", len(sent_ids))
            log.info("ciclo: enviados=%s, fallidos=%s", ok, fail)


def main():
    log.info("iniciando sender → endpoint=%s, interval=%ss, batch=%s", ENDPOINT, INTERVAL_SEC, BATCH_SIZE)
    try:
        with get_conn() as _:
            pass
    except Exception as e:
        log.error("No se pudo conectar a Postgres (%s:%s/%s): %s", DB_HOST, DB_PORT, DB_NAME, e)
        sys.exit(1)

    while True:
        try:
            tick_once()
        except Exception as e:
            log.exception("error en tick_once: %s", e)
        time.sleep(INTERVAL_SEC)


if __name__ == "__main__":
    main()
