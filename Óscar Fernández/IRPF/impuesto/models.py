from django.db import models
from decimal import Decimal

class DeclaracionIRPF(models.Model):
    # Datos identificativos
    cif_cliente = models.CharField(max_length=20)
    nif_empresa = models.CharField(max_length=20)
    numero_impuesto = models.CharField(max_length=50)

    # Ingresos
    sueldo_bruto = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    ingresos_alquileres = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    ingresos_capital = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    ganancias_patrimoniales = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Gastos deducibles
    cotizaciones_ss = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    otros_gastos = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Resultado
    total_a_recaudar = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    renta_neta = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def calcular_irpf(self):
        ingresos = (
            self.sueldo_bruto +
            self.ingresos_alquileres +
            self.ingresos_capital +
            self.ganancias_patrimoniales
        )

        gastos = self.cotizaciones_ss + self.otros_gastos
        base_imponible = ingresos - gastos

        cuota = Decimal('0')

        # Tramo 1
        if base_imponible > 0:
            tramo = min(base_imponible, Decimal('12450'))
            cuota += tramo * Decimal('0.19')

        # Tramo 2
        if base_imponible > Decimal('12450'):
            tramo = min(base_imponible, Decimal('20200')) - Decimal('12450')
            cuota += tramo * Decimal('0.24')

        # Tramo 3
        if base_imponible > Decimal('20200'):
            tramo = min(base_imponible, Decimal('35200')) - Decimal('20200')
            cuota += tramo * Decimal('0.30')

        # Tramo 4
        if base_imponible > Decimal('35200'):
            tramo = min(base_imponible, Decimal('60000')) - Decimal('35200')
            cuota += tramo * Decimal('0.37')

        # Tramo 5
        if base_imponible > Decimal('60000'):
            tramo = base_imponible - Decimal('60000')
            cuota += tramo * Decimal('0.45')

        # Guardamos resultados
        self.total_a_recaudar = cuota
        self.renta_neta = base_imponible - cuota

        return cuota

    def __str__(self):
        return f"Declaración {self.numero_impuesto} - Cliente {self.cif_cliente}"
