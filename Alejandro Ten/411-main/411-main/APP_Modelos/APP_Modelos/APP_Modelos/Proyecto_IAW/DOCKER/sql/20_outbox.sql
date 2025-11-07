-- 20_outbox.sql — esquema + tabla + función + trigger (corregido)
CREATE SCHEMA IF NOT EXISTS imp411;

-- Ajustes de tipos: numero_impuesto como TEXT (API lo quiere string),
-- total_a_recaudar como NUMERIC (dinero).
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.tables
    WHERE table_schema='imp411' AND table_name='impuesto_outbox_raw'
  ) THEN
    CREATE TABLE imp411.impuesto_outbox_raw (
      id                BIGSERIAL PRIMARY KEY,
      cif_empresa       TEXT        NOT NULL,
      nif_cliente       TEXT        NOT NULL,
      numero_impuesto   TEXT        NOT NULL,
      total_a_recaudar  NUMERIC(12,2) NOT NULL,
      datos             JSONB       NOT NULL,
      created_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
      sent              BOOLEAN     NOT NULL DEFAULT FALSE,
      sent_at           TIMESTAMPTZ
    );
  END IF;

  -- Si ya existía, garantizamos tipos correctos:
  BEGIN
    ALTER TABLE imp411.impuesto_outbox_raw
      ALTER COLUMN numero_impuesto TYPE TEXT USING numero_impuesto::TEXT;
  EXCEPTION WHEN others THEN
    -- ignorar si ya es TEXT
  END;

  BEGIN
    ALTER TABLE imp411.impuesto_outbox_raw
      ALTER COLUMN total_a_recaudar TYPE NUMERIC(12,2) USING total_a_recaudar::NUMERIC;
  EXCEPTION WHEN others THEN
    -- ignorar si ya es NUMERIC
  END;
END$$;

-- Función del trigger
CREATE OR REPLACE FUNCTION imp411.fn_capture_formulario411()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  INSERT INTO imp411.impuesto_outbox_raw
    (cif_empresa, nif_cliente, numero_impuesto, total_a_recaudar, datos)
  VALUES
    (
      NEW.cif,
      NEW.nif,
      '411',                                -- como TEXT (evita 422 del API)
      COALESCE(NEW.cuota_tributaria, 0),    -- total_a_recaudar FUERA del JSON
      jsonb_build_object(
        'id',               NEW.id,
        'nif',              NEW.nif,
        'iban',             NEW.iban,
        'cif',              NEW.cif,
        'anio',             NEW.anio,       -- ¡sin ñ!
        'base_imponible',   NEW.base_imponible,
        'cuota_tributaria', NEW.cuota_tributaria,
        'importe_ingresar', NEW.importe_ingresar,
        'territorio',       NEW.territorio,
        'fecha_creacion',   NEW.fecha_creacion
      )
    );

  RETURN NEW;
END;
$$;

-- (Re)crear trigger sobre la tabla Django real
DO $$
BEGIN
  IF EXISTS (
    SELECT 1 FROM information_schema.tables
    WHERE table_schema='public' AND table_name='impuesto_411_formulario411'
  ) THEN
    -- Elimina trigger previo si existe
    IF EXISTS (
      SELECT 1 FROM pg_trigger WHERE tgname='tr_capture_formulario411'
    ) THEN
      EXECUTE 'DROP TRIGGER tr_capture_formulario411 ON public.impuesto_411_formulario411';
    END IF;

    -- Crea el trigger correcto (INSERT + UPDATE si quieres capturar cambios)
    EXECUTE 'CREATE TRIGGER tr_capture_formulario411
             AFTER INSERT OR UPDATE ON public.impuesto_411_formulario411
             FOR EACH ROW
             EXECUTE FUNCTION imp411.fn_capture_formulario411()';
  END IF;
END$$;
