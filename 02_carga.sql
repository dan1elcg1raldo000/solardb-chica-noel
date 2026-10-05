-- sql/02_carga.sql
-- Carga idempotente: una misma pareja (dispositivo_id, ts) no se duplica.

INSERT INTO lectura_demo (
    dispositivo_id,
    ts,
    p_ac,
    irradiancia,
    temp_modulo,
    payload
)
SELECT
    (payload ->> 'device_id')::INT,
    (payload ->> 'ts')::TIMESTAMPTZ,
    (payload ->> 'p_ac')::NUMERIC(10,3),
    (payload ->> 'irradiancia')::NUMERIC(8,1),
    (payload ->> 'temp_modulo')::NUMERIC(5,1),
    payload
FROM stg_lectura_raw
ON CONFLICT (dispositivo_id, ts) DO NOTHING;

-- Consultas JSONB solicitadas:
SELECT payload ->> 'device_id' AS dispositivo
FROM stg_lectura_raw
LIMIT 5;

SELECT payload -> 'irradiancia' AS irradiancia
FROM stg_lectura_raw
WHERE payload ? 'alarma'
LIMIT 5;
