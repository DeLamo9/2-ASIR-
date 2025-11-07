from django.db import migrations

FORWARD_SQL = r"""
-- 1) Esquema y tabla outbox (idempotente)
CREATE SCHEMA IF NOT EXISTS imp411;

CREATE TABLE IF NOT EXISTS imp411.impuesto_outbox_raw (
  id              BIGSERIAL PRIMARY KEY,
  cif_empresa     TEXT NOT NULL,
  nif_cliente     TEXT NOT NULL,
  numero_impuesto INT  NOT NULL,
  datos           JSONB NOT NULL,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  sent            BOOLEAN NOT NULL DEFAULT FALSE,
  sent_at         TIMESTAMPTZ
);

-- 2) Función que captura los INSERT en la tabla del modelo
CREATE OR REPLACE FUNCTION imp411.fn_capture_formulario411()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO imp411.impuesto_outbox_raw (cif_empresa, nif_cliente, numero_impuesto, datos)
  VALUES (
    NEW.cif,
    NEW.nif,
    411,
    jsonb_build_object(
      -- OJO: tras 0002 el campo es 'anio' (sin tilde)
      'anio', NEW.anio,
      'iban', NEW.iban,
      'base_imponible', NEW.base_imponible,
      'cuota_tributaria', NEW.cuota_tributaria,
      'importe_ingresar', NEW.importe_ingresar,
      'territorio', NEW.territorio,
      'fecha_creacion', NEW.fecha_creacion
    )
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 3) Crear el trigger solo si la tabla existe y el trigger no existe (idempotente)
DO $$
BEGIN
  IF EXISTS (
    SELECT 1
    FROM information_schema.tables
    WHERE table_schema = 'public'
      AND table_name   = 'impuesto_411_formulario411'
  ) THEN
    IF NOT EXISTS (
      SELECT 1 FROM pg_trigger WHERE tgname = 'trg_formulario411_after_insert'
    ) THEN
      EXECUTE 'CREATE TRIGGER trg_formulario411_after_insert
               AFTER INSERT ON public.impuesto_411_formulario411
               FOR EACH ROW
               EXECUTE FUNCTION imp411.fn_capture_formulario411()';
    END IF;
  END IF;
END
$$;
"""

REVERSE_SQL = r"""
-- 1) Eliminar el trigger si existe (y la tabla existe)
DO $$
BEGIN
  IF EXISTS (
    SELECT 1
    FROM information_schema.tables
    WHERE table_schema = 'public'
      AND table_name   = 'impuesto_411_formulario411'
  ) THEN
    IF EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'trg_formulario411_after_insert') THEN
      EXECUTE 'DROP TRIGGER trg_formulario411_after_insert ON public.impuesto_411_formulario411';
    END IF;
  END IF;
END
$$;

-- 2) Eliminar la función (si existe)
DROP FUNCTION IF EXISTS imp411.fn_capture_formulario411();
"""

class Migration(migrations.Migration):

    dependencies = [
        ('Impuesto_411', '0002_rename_ejercicio_formulario411_anio_and_more'),
    ]

    operations = [
        migrations.RunSQL(sql=FORWARD_SQL, reverse_sql=REVERSE_SQL),
    ]
