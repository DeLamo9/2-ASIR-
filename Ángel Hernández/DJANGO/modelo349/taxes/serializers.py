from rest_framework import serializers
from .models import SujetoPasivo, Declaracion349, OperadorIntracomunitario

class SujetoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SujetoPasivo
        fields = ['id','nif','nombre','direccion','pueblo','codigo_postal','pais']

class OperadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperadorIntracomunitario
        fields = ['id','nif_operador','nombre','pais','clave','base_imponible','observaciones']

class DeclaracionSerializer(serializers.ModelSerializer):
    operadores = OperadorSerializer(many=True)
    sujeto = SujetoSerializer()  # permite enviar sujeto anidado o manejaremos por nif

    class Meta:
        model = Declaracion349
        fields = ['id','sujeto','ejercicio','periodo','presentado_por','total_operadores','total_base_imponible','operadores']

    def create(self, validated_data):
        sujeto_data = validated_data.pop('sujeto')
        operadores_data = validated_data.pop('operadores', [])

        # buscar o crear sujeto por NIF
        nif = sujeto_data.get('nif')
        sujeto, _ = SujetoPasivo.objects.get_or_create(nif=nif, defaults=sujeto_data)

        decl = Declaracion349.objects.create(sujeto=sujeto, **validated_data)

        total = 0
        for op_data in operadores_data:
            OperadorIntracomunitario.objects.create(declaracion=decl, **op_data)
            total += float(op_data.get('base_imponible', 0))

        decl.total_operadores = len(operadores_data)
        decl.total_base_imponible = round(total, 2)
        decl.save()
        return decl
