import os, time, json, sys
import psycopg2
import psycopg2.extras
import requests

ENDPOINT = os.getenv("IMP411_ENDPOINT", "http://172.20.10.12:8000/api/impuestos")
INTERVAL = int(os.getenv("IMP411_INTERVAL_SEC", "30"))
BATCH = int(os.getenv("IMP411_BATCH", "100"))

def get_conn():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "db"),
        port=int(os.getenv("POSTGRES_PORT", "5432")),
        dbname=os.getenv("POSTGRES_DB", "proyecto"),
        user=os.getenv("POSTGRES_USER", "proyecto"),
        password=os.getenv("POSTGRES_PASSWORD", "proyecto")
    )

SQL_FETCH = f"""
SELECT
  cif_empresa, nif_cliente, numero_impuesto,
  json_agg(jsonb_build_object('id', id, 'datos', datos, 'created_at', created_at) ORDER BY id) AS items
FROM imp411.impuesto_outbox_raw
WHERE sent = FALSE
GROUP BY cif_empresa, nif_cliente, numero_impuesto
LIMIT %s;
"""

SQL_MARK_SENT = """
UPDATE imp411.impuesto_outbox_raw
SET sent = TRUE, sent_at = now()
WHERE id = ANY(%s::bigint[]);
"""

def tick_once():
    with get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(SQL_FETCH, (BATCH,))
            groups = cur.fetchall()

    for g in groups:
        ids = [item["id"] for item in g["items"]]
        payload = {
            "cif_empresa": g["cif_empresa"],
            "nif_cliente": g["nif_cliente"],
            "numero_impuesto": g["numero_impuesto"],
            "datos": [item["datos"] for item in g["items"]]
        }

        try:
            r = requests.post(ENDPOINT, json=payload, timeout=10)
            ok = 200 <= r.status_code < 300
        except Exception as e:
            print(f"[sender] POST error: {e}", file=sys.stderr)
            ok = False

        if ok:
            with get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(SQL_MARK_SENT, (ids,))
                conn.commit()
            print(f"[sender] enviado {len(ids)} → marcado sent")
        else:
            print(f"[sender] fallo al enviar grupo {g['cif_empresa']}/{g['nif_cliente']}/{g['numero_impuesto']} (ids {ids})")

if __name__ == "__main__":
    while True:
        try:
            tick_once()
        except Exception as e:
            print(f"[sender] error: {e}", file=sys.stderr)
        time.sleep(INTERVAL)
