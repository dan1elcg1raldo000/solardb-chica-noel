-- sql/03_roles.sql
-- Ejecutar con un usuario administrador.

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_roles WHERE rolname = 'solar_lector'
    ) THEN
        CREATE ROLE solar_lector NOLOGIN;
    END IF;
END $$;

GRANT CONNECT ON DATABASE solardb TO solar_lector;
GRANT USAGE ON SCHEMA public TO solar_lector;
GRANT SELECT ON TABLE lectura_demo TO solar_lector;

-- El rol no recibe INSERT/UPDATE/DELETE.
REVOKE INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER
ON TABLE lectura_demo FROM solar_lector;
