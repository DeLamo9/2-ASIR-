from django import forms
from django.forms import inlineformset_factory
from .models import SujetoPasivo, Declaracion349, OperadorIntracomunitario

class SujetoForm(forms.ModelForm):
    class Meta:
        model = SujetoPasivo
        fields = ['nif','nombre','direccion','pueblo','codigo_postal','pais']

class DeclaracionForm(forms.ModelForm):
    class Meta:
        model = Declaracion349
        fields = ['ejercicio','periodo','presentado_por']

OperadorFormSet = inlineformset_factory(Declaracion349, OperadorIntracomunitario,
                                        fields=['nif_operador','nombre','pais','clave','base_imponible','observaciones'],
                                        extra=1, can_delete=True)
