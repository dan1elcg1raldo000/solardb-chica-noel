# SolarDB — Gobernanza, ETL e IoT

## Integrantes
- INTEGRANTE 1: Erick Noel Delgado Serna
- INTEGRANTE 2: Daniel Felipe Chica Giraldo

## Curso
Bases de Datos I (SD1006) — Grupo 811 — 2026-II

## Descripción
Práctica de SolarDB Pascual centrada en gobernanza de datos, automatización ETL e IoT sobre PostgreSQL.

El flujo simula dos inversores que producen telemetría JSON, guarda los mensajes en una tabla de staging y transforma los datos hacia una tabla relacional. La clave primaria `(dispositivo_id, ts)` y `ON CONFLICT DO NOTHING` permiten que la carga sea idempotente.

## Estructura
- `data/lecturas.jsonl`: datos JSONL de muestra.
- `etl/simulador.py`: genera telemetría de dos dispositivos.
- `etl/run_etl.py`: punto único de entrada para la ingesta.
- `sql/01_tablas.sql`: tablas de staging, destino y bitácora.
- `sql/02_carga.sql`: transformación y carga idempotente.
- `sql/03_roles.sql`: rol `solar_lector` de solo lectura.
- `docs/`: PDF de la consulta.

## Requisitos
- PostgreSQL 15 o superior.
- Python 3.10+.
- `psycopg2-binary`.

## Preparación
1. Crear una base de datos llamada `solardb`.
2. Ejecutar `sql/01_tablas.sql`.
3. Ejecutar `sql/03_roles.sql`.
4. Instalar dependencias:
   `pip install -r requirements.txt`
5. Crear un `.env` local o definir `DATABASE_URL` en el entorno.
6. Ejecutar:
   `python etl/simulador.py`
7. Ejecutar el pipeline:
   `python etl/run_etl.py`

## Prueba de idempotencia
Ejecutar el pipeline dos veces con el mismo archivo y consultar:

```sql
SELECT COUNT(*) FROM lectura_demo;
```

El segundo ciclo no debe duplicar las claves `(dispositivo_id, ts)` ya existentes.

## Evidencia de permisos
Con `solar_lector` debe funcionar:

```sql
SELECT * FROM lectura_demo;
```

y debe fallar un `INSERT` sobre `lectura_demo`.

## Programación horaria
Ejemplo de cron cada hora:

```cron
0 * * * * cd /ruta/al/repositorio && /usr/bin/python3 etl/run_etl.py
```

## Participación
| Integrante | Aportes |
|---|---|
| Erick Noel Delgado Serna | Gobernanza de datos, SQL de tablas/roles, parte de la consulta y pruebas ETL |
| Daniel Felipe Chica Giraldo | ETL/JSON, IoT, documentación, README y pruebas de idempotencia |
