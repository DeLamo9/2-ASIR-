from django.shortcuts import render, redirect
from .forms import Modelo576Form

def formulario_576(request):
    if request.method == 'POST':
        form = Modelo576Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('confirmacion')
        else:
            print(form.errors)
    else:
        form = Modelo576Form()
    return render(request, 'formulario_576.html', {'form': form})

def confirmacion(request):
    return render(request, 'confirmacion.html')

