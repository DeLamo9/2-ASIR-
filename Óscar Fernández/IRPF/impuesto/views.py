from django.shortcuts import render, redirect, get_object_or_404
from .models import DeclaracionIRPF
from decimal import Decimal

def declarar_irpf(request):
    if request.method == "POST":
        declaracion = DeclaracionIRPF(
            cif_cliente=request.POST.get("cif_cliente"),
            nif_empresa=request.POST.get("nif_empresa"),
            numero_impuesto=request.POST.get("numero_impuesto"),
            sueldo_bruto=Decimal(request.POST.get("sueldo_bruto") or 0),
            ingresos_alquileres=Decimal(request.POST.get("ingresos_alquileres") or 0),
            ingresos_capital=Decimal(request.POST.get("ingresos_capital") or 0),
            ganancias_patrimoniales=Decimal(request.POST.get("ganancias_patrimoniales") or 0),
            cotizaciones_ss=Decimal(request.POST.get("cotizaciones_ss") or 0),
            otros_gastos=Decimal(request.POST.get("otros_gastos") or 0),
        )

        declaracion.calcular_irpf()
        declaracion.save()

        return redirect("resultado_irpf", pk=declaracion.pk)

    return render(request, "modelo100.html")

def resultado_irpf(request, pk):
    declaracion = get_object_or_404(DeclaracionIRPF, pk=pk)
    return render(request, "resultado_irpf.html", {"declaracion": declaracion})