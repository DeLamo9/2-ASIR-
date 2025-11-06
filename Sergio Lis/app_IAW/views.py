from django.shortcuts import render, redirect
from rest_framework import viewsets
from .models import Modelo146, EntidadPagadora
from .serializers import Modelo146Serializer, EntidadPagadoraSerializer
from .forms import Modelo146Form, EntidadPagadoraForm


class Modelo146ViewSet(viewsets.ModelViewSet):
    queryset = Modelo146.objects.all().order_by('-id')
    serializer_class = Modelo146Serializer


class EntidadPagadoraViewSet(viewsets.ModelViewSet):
    queryset = EntidadPagadora.objects.all().order_by('-id')
    serializer_class = EntidadPagadoraSerializer



def home(request):
    """Página principal."""
    return render(request, "home.html")


def formulario_146(request):
    """Vista para crear un nuevo Modelo 146."""
    if request.method == "POST":
        form = Modelo146Form(request.POST)
        if form.is_valid():
            modelo = form.save()  # guarda el formulario y ejecuta los cálculos del IRPF
            return redirect("home")
        else:
            # Muestra los errores si el formulario no es válido
            return render(request, "formulario146.html", {"form": form, "errores": form.errors})
    else:
        form = Modelo146Form()

    return render(request, "formulario146.html", {"form": form})
