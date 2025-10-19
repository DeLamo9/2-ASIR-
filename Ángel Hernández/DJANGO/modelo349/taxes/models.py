from django.db import models
from django.utils import timezone
from decimal import Decimal

CLAVE_CHOICES = [
    ('A', 'Entrega de bienes'),
    ('B', 'Prestación de servicios'),
    ('C', 'Operación triangular'),
    # amplía según necesidad
]

class SujetoPasivo(models.Model):
    nif = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=300, blank=True, null=True)
    pueblo = models.CharField(max_length=100, blank=True, null=True)
    codigo_postal = models.CharField(max_length=10, blank=True, null=True)
    pais = models.CharField(max_length=3, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.nif})"

class Declaracion349(models.Model):
    sujeto = models.ForeignKey(SujetoPasivo, on_delete=models.CASCADE, related_name='declaraciones')
    ejercicio = models.PositiveIntegerField()
    periodo = models.CharField(max_length=20)  # ejemplo: 'T1', 'M01', etc.
    presentado_por = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    total_operadores = models.PositiveIntegerField(default=0)
    total_base_imponible = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return f"349 {self.sujeto.nif} - {self.ejercicio}/{self.periodo}"

class OperadorIntracomunitario(models.Model):
    declaracion = models.ForeignKey(Declaracion349, on_delete=models.CASCADE, related_name='operadores')
    nif_operador = models.CharField(max_length=60)
    nombre = models.CharField(max_length=200)
    pais = models.CharField(max_length=3)
    clave = models.CharField(max_length=2, choices=CLAVE_CHOICES)
    base_imponible = models.DecimalField(max_digits=18, decimal_places=2)
    observaciones = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return f"{self.nif_operador} - {self.base_imponible}"
