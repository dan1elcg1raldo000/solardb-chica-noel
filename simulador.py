import json
import os
import random
from datetime import datetime, timedelta, timezone

TZ = timezone(timedelta(hours=-5))
INICIO = datetime(2026, 10, 5, 6, 0, tzinfo=TZ)
DISPOSITIVOS = (1, 2)
INTERVALO_MINUTOS = 5
NUM_LECTURAS = 144

random.seed(811)

os.makedirs("data", exist_ok=True)

with open("data/lecturas.jsonl", "w", encoding="utf-8") as f:
    for i in range(NUM_LECTURAS):
        ts = INICIO + timedelta(minutes=INTERVALO_MINUTOS * i)

        for device_id in DISPOSITIVOS:
            msg = {
                "device_id": device_id,
                "ts": ts.isoformat(),
                "p_ac": round(random.uniform(0, 5.0), 3),
                "irradiancia": round(random.uniform(0, 1000), 1),
                "temp_modulo": round(random.uniform(18, 60), 1),
                # Campo nuevo elegido para la práctica:
                "voltaje_dc": round(random.uniform(300, 850), 1),
            }

            if random.random() < 0.03:
                msg["alarma"] = "GRID_FAULT"

            f.write(json.dumps(msg, ensure_ascii=False) + "\n")

print("Generación terminada: data/lecturas.jsonl")
print(f"Registros generados: {NUM_LECTURAS * len(DISPOSITIVOS)}")
