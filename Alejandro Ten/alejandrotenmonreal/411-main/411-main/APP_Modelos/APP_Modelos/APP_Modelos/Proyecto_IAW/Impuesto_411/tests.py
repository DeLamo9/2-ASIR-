from decimal import Decimal
import json

from django.test import TestCase
from django.urls import reverse

from .models import Formulario411


class Impuesto411APITests(TestCase):
  def _post(self, payload):
    return self.client.post(
      reverse("api_411"),
      data=json.dumps(payload),
      content_type="application/json",
    )

  def test_crea_registro_y_calcula_cuotas(self):
    payload = {
      "nif": "12345678Z",
      "iban": "es12 3456 7890 1234 5678 9012",
      "año": 2024,
      "cif": "A12345678",
      "base_imponible": "1000.50",
      "territorio": "Canarias",
    }

    response = self._post(payload)

    self.assertEqual(response.status_code, 201)
    data = response.json()
    self.assertTrue(data["ok"])

    obj = Formulario411.objects.get(pk=data["id"])
    self.assertEqual(obj.año, 2024)
    self.assertEqual(obj.base_imponible, Decimal("1000.50"))
    self.assertEqual(obj.cuota_tributaria, Decimal("3.00"))
    self.assertEqual(obj.importe_ingresar, Decimal("3.00"))
    self.assertEqual(obj.iban, "ES1234567890123456789012")

  def test_devuelve_400_si_falta_base_imponible(self):
    payload = {
      "nif": "12345678Z",
      "iban": "ES7632100001187654321098",
      "año": 2024,
      "cif": "A12345678",
      "base_imponible": "",
    }

    response = self._post(payload)

    self.assertEqual(response.status_code, 400)
    body = response.json()
    self.assertFalse(body["ok"])
    self.assertIn("base_imponible", " ".join(body.get("errores", [])))

  def test_devuelve_400_si_anio_no_es_entero(self):
    payload = {
      "nif": "12345678Z",
      "iban": "ES7632100001187654321098",
      "año": "dosmil",  # valor no numérico
      "cif": "A12345678",
      "base_imponible": "50",
    }

    response = self._post(payload)

    self.assertEqual(response.status_code, 400)
    body = response.json()
    self.assertFalse(body["ok"])
    self.assertTrue(any("entero" in msg for msg in body.get("errores", [])))

  def test_devuelve_400_si_base_negativa(self):
    payload = {
      "nif": "12345678Z",
      "iban": "ES7632100001187654321098",
      "año": 2024,
      "cif": "A12345678",
      "base_imponible": "-10",
    }

    response = self._post(payload)

    self.assertEqual(response.status_code, 400)
    body = response.json()
    self.assertFalse(body["ok"])
    self.assertIn("negativa", body.get("error", ""))

