from decimal import Decimal, InvalidOperation
from django import forms
from .models import Modelo146, EntidadPagadora

class Modelo146Form(forms.ModelForm):
    class Meta:
        model = Modelo146
        fields = '__all__'
        widgets = {
            # Campos principales (adapta o añade más según prefieras)
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'border rounded-lg p-2 w-full'}),
            'tipo_irpf': forms.NumberInput(attrs={'step': '0.01', 'class': 'border rounded-lg p-2 w-full'}),
            'importe_bruto': forms.NumberInput(attrs={'step': '0.01', 'class': 'border rounded-lg p-2 w-full'}),
            'nombre': forms.TextInput(attrs={'class': 'border rounded-lg p-2 w-full'}),
            'primer_apellido': forms.TextInput(attrs={'class': 'border rounded-lg p-2 w-full'}),
            'segundo_apellido': forms.TextInput(attrs={'class': 'border rounded-lg p-2 w-full'}),
            'municipio': forms.TextInput(attrs={'class': 'border rounded-lg p-2 w-full'}),
            'provincia': forms.TextInput(attrs={'class': 'border rounded-lg p-2 w-full'}),
            'via_publica': forms.TextInput(attrs={'class': 'border rounded-lg p-2 w-full'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'border rounded-lg p-2 w-full'}),
            'telefono1': forms.TextInput(attrs={'class': 'border rounded-lg p-2 w-full'}),
            'telefono2': forms.TextInput(attrs={'class': 'border rounded-lg p-2 w-full'}),
        }

    def clean(self):
        """
        Validaciones y cálculo en limpio (antes de guardar).
        Calcula importe_retencion e importe_neto y los añade a cleaned_data.
        """
        cleaned = super().clean()

        importe_bruto = cleaned.get('importe_bruto')
        tipo_irpf = cleaned.get('tipo_irpf')

        # Valores por defecto si vienen vacíos
        if importe_bruto in (None, ''):
            # No forzamos valor; dejamos que el modelo maneje default o campo requerido si corresponde.
            return cleaned

        # Protegemos contra tipos inválidos
        try:
            importe_bruto = Decimal(importe_bruto)
        except (InvalidOperation, TypeError):
            self.add_error('importe_bruto', 'Importe bruto no válido.')
            return cleaned

        try:
            tipo_irpf = Decimal(tipo_irpf) if tipo_irpf not in (None, '') else Decimal('19.00')
        except (InvalidOperation, TypeError):
            self.add_error('tipo_irpf', 'Tipo IRPF no válido.')
            return cleaned

        # Cálculo
        importe_retencion = (importe_bruto * tipo_irpf) / Decimal('100')
        importe_neto = importe_bruto - importe_retencion

        # Guardamos en cleaned_data para que esté disponible en save()
        cleaned['importe_retencion'] = round(importe_retencion, 2)
        cleaned['importe_neto'] = round(importe_neto, 2)

        return cleaned

    def save(self, commit=True):
        """
        Nos aseguramos de aplicar los valores calculados al instance antes de guardar.
        """
        instance = super().save(commit=False)

        cleaned = getattr(self, 'cleaned_data', {})

        # Si el clean() calculó retención/neto, los aplicamos; si no, calculamos aquí como redundancia.
        importe_bruto = cleaned.get('importe_bruto') or getattr(instance, 'importe_bruto', None)
        tipo_irpf = cleaned.get('tipo_irpf') or getattr(instance, 'tipo_irpf', Decimal('19.00'))

        if importe_bruto is not None:
            try:
                importe_bruto = Decimal(importe_bruto)
                tipo_irpf = Decimal(tipo_irpf)
                instance.importe_retencion = (importe_bruto * tipo_irpf) / Decimal('100')
                instance.importe_neto = importe_bruto - instance.importe_retencion
            except (InvalidOperation, TypeError):
                # Si algo falla, no sobreescribimos los valores existentes; opcional: podríamos añadir errores.
                pass

        if commit:
            instance.save()
            # si hay campos ManyToMany se deberían guardar aquí con self.save_m2m()
        return instance


class EntidadPagadoraForm(forms.ModelForm):
    class Meta:
        model = EntidadPagadora
        fields = '__all__'
        widgets = {
            'nif_pagador': forms.TextInput(attrs={'class': 'border rounded-lg p-2 w-full'}),
            'razon_social': forms.TextInput(attrs={'class': 'border rounded-lg p-2 w-full'}),
            'importe_anual': forms.NumberInput(attrs={'step': '0.01', 'class': 'border rounded-lg p-2 w-full'}),
        }
