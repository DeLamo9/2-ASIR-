from django.test import TestCase
from .models import Modelo146

class Modelo146TestCase(TestCase):
    def test_creacion_modelo(self):
        modelo = Modelo146.objects.create(
            nif="",
            primer_apellido="García",
            nombre="Sergio"
        )
        self.assertEqual(modelo.primer_apellido, "García")
