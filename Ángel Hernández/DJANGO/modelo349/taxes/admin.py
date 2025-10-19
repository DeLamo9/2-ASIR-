from django.contrib import admin
from .models import SujetoPasivo, Declaracion349, OperadorIntracomunitario

@admin.register(SujetoPasivo)
class SujetoAdmin(admin.ModelAdmin):
    list_display = ('nif','nombre')

@admin.register(Declaracion349)
class DeclaracionAdmin(admin.ModelAdmin):
    list_display = ('sujeto','ejercicio','periodo','total_operadores','total_base_imponible','created_at')
    search_fields = ('sujeto__nif','sujeto__nombre')

@admin.register(OperadorIntracomunitario)
class OperadorAdmin(admin.ModelAdmin):
    list_display = ('nif_operador','nombre','pais','clave','base_imponible','declaracion')

