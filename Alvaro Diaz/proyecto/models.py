from django.db import models

# Create your models here.

class Modelo576(models.Model):
    # Datos generales
    nif = models.CharField(max_length=15)
    matricula= models.PositiveIntegerField()
    periodo = models.CharField(max_length=5)
    
    HECHO_IMPONIBLE_CHOICES = [
        ('1', 'Primera matriculación definitiva'),
        ('2', 'Circulación o utilización en España'),
        ('3', 'Modificación de características técnicas'),
        ('4', 'Introducción desde Canarias/Baleares'),
        ('5', 'Renuncia a beneficios fiscales'),
    ]
    hecho_imponible = models.CharField(max_length=2, choices=HECHO_IMPONIBLE_CHOICES)

    # Datos del vehículo
    medio_transporte_nuevo = models.BooleanField(default=False)
    medio_transporte_usado = models.BooleanField(default=False)
    fecha_prueba_servicio = models.DateField(null=True, blank=True)
    kilometros = models.IntegerField(null=True, blank=True)
    marca = models.CharField(max_length=50)
    modelo_tipo = models.CharField(max_length=50)
    numero_serie = models.CharField(max_length=50)
    MOTOR_CHOICES = [
        ('gasolina', 'Gasolina'),
        ('diesel', 'Diésel'),
        ('electrico', 'Electrico'),
        ('otros', 'Otros'),
    ]
    motor = models.CharField(max_length=10, choices=MOTOR_CHOICES)
    cilindrada = models.IntegerField(null=True, blank=True)
    emisiones_co2 = models.IntegerField(null=True, blank=True)

    # Liquidación
    base_imponible = models.DecimalField(max_digits=12, decimal_places=2)
    tipo = models.DecimalField(max_digits=5, decimal_places=2)
    cuota = models.DecimalField(max_digits=12, decimal_places=2)
    deduccion_lineal = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=True, blank= True)
    cuota_ingresar = models.DecimalField(max_digits=12, decimal_places=2)

    # Control
    fecha_presentacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Modelo 576 - {self.nif} ({self.matricula})"
