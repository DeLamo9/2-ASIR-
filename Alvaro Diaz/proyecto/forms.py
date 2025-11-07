from django import forms
from .models import Modelo576

class Modelo576Form(forms.ModelForm):
    class Meta:
        model = Modelo576
        fields = '__all__'
        widgets = {
            'fecha_prueba_servicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hecho_imponible': forms.Select(attrs={'class': 'form-select'}),
            'motor': forms.Select(attrs={'class': 'form-select'}),
        }
