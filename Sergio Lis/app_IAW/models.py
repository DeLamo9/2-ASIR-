from django.db import models

class Modelo146(models.Model):
    # Datos del contribuyente
    nif = models.CharField(max_length=9, blank=True, null=True)
    primer_apellido = models.CharField(max_length=100, default=" ")
    segundo_apellido = models.CharField(max_length=100, blank=True, null=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    via_publica = models.CharField(max_length=150, blank=True, null=True)
    numero = models.CharField(max_length=10, blank=True, null=True)
    municipio = models.CharField(max_length=100, blank=True, null=True)
    telefono1 = models.CharField(max_length=15, blank=True, null=True)


    # Campos económicos
    importe_bruto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tipo_irpf = models.DecimalField(max_digits=5, decimal_places=2, default=19.00)
    importe_retencion = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    importe_neto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Representante
    representante_nif = models.CharField(max_length=9, blank=True, null=True)
    representante_nombre = models.CharField(max_length=150, blank=True, null=True)
    representante_via_publica = models.CharField(max_length=150, blank=True, null=True)
    representante_numero = models.CharField(max_length=10, blank=True, null=True)
    representante_municipio = models.CharField(max_length=100, blank=True, null=True)
    representante_provincia = models.CharField(max_length=100, blank=True, null=True)
    representante_codigo_postal = models.CharField(max_length=10, blank=True, null=True)

    # Firma
    lugar = models.CharField(max_length=100, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        """Calcula retención y neto automáticamente antes de guardar"""
        if self.importe_bruto and self.tipo_irpf is not None:
            self.importe_retencion = (self.importe_bruto * self.tipo_irpf) / 100
            self.importe_neto = self.importe_bruto - self.importe_retencion
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nif or ''} - {self.nombre or ''} {self.primer_apellido or ''}".strip()


class EntidadPagadora(models.Model):
    modelo146 = models.ForeignKey(Modelo146, related_name="pagadores", on_delete=models.CASCADE)
    nif_pagador = models.CharField(max_length=9)
    razon_social = models.CharField(max_length=200)
    importe_anual = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.razon_social} - {self.importe_anual}€"
