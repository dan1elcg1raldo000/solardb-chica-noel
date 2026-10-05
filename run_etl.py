import json
import os
from datetime import datetime, timezone
from pathlib import Path

import psycopg2

DATABASE_URL = os.environ["DATABASE_URL"]
DATA_FILE = Path("data/lecturas.jsonl")

def load_messages(conn):
    started = datetime.now(timezone.utc)
    read = 0
    loaded = 0
    rejected = 0
    error = None
    status = "OK"

    try:
        with conn.cursor() as cur:
            with DATA_FILE.open("r", encoding="utf-8") as f:
                for line in f:
                    read += 1
                    try:
                        payload = json.loads(line)
                        cur.execute(
                            """
                            INSERT INTO stg_lectura_raw (payload)
                            VALUES (%s::jsonb)
                            """,
                            (json.dumps(payload, ensure_ascii=False),)
                        )
                    except Exception:
                        rejected += 1

            cur.execute(
                """
                INSERT INTO lectura_demo
                    (dispositivo_id, ts, p_ac, irradiancia, temp_modulo, payload)
                SELECT
                    (payload ->> 'device_id')::INT,
                    (payload ->> 'ts')::TIMESTAMPTZ,
                    (payload ->> 'p_ac')::NUMERIC(10,3),
                    (payload ->> 'irradiancia')::NUMERIC(8,1),
                    (payload ->> 'temp_modulo')::NUMERIC(5,1),
                    payload
                FROM stg_lectura_raw
                ON CONFLICT (dispositivo_id, ts) DO NOTHING
                """
            )
            loaded = cur.rowcount

            finished = datetime.now(timezone.utc)
            cur.execute(
                """
                INSERT INTO etl_log
                    (inicio, fin, filas_leidas, filas_cargadas,
                     filas_rechazadas, estado, error)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (started, finished, read, loaded, rejected, status, error)
            )

        conn.commit()
        print(f"ETL OK | leídas={read} cargadas={loaded} rechazadas={rejected}")

    except Exception as exc:
        conn.rollback()
        finished = datetime.now(timezone.utc)
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO etl_log
                    (inicio, fin, filas_leidas, filas_cargadas,
                     filas_rechazadas, estado, error)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (started, finished, read, loaded, rejected, "ERROR", str(exc))
            )
        conn.commit()
        raise

if __name__ == "__main__":
    with psycopg2.connect(DATABASE_URL) as conn:
        load_messages(conn)
