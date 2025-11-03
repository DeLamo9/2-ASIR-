# Impuesto_411/models.py
from django.db import models

class Formulario411(models.Model):
    # Identificación
    nif = models.CharField(max_length=15)
    iban = models.CharField(max_length=34)
    cif = models.CharField(max_length=15)
    año = models.IntegerField()  # ← renombrado (ASCII) y tipo entero

    # Liquidación
    base_imponible = models.DecimalField(max_digits=15, decimal_places=2)
    cuota_tributaria = models.DecimalField(max_digits=15, decimal_places=2, default=0)   # ← nuevo
    importe_ingresar = models.DecimalField(max_digits=15, decimal_places=2, default=0)   # ← nuevo

    # Territorio
    territorio = models.CharField(max_length=50, default="No presencial")

    # Fecha de registro
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nif} ({self.año})"
