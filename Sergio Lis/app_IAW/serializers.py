from rest_framework import serializers
from .models import Modelo146, EntidadPagadora

class EntidadPagadoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntidadPagadora
        fields = '__all__'

class Modelo146Serializer(serializers.ModelSerializer):
    pagadores = EntidadPagadoraSerializer(many=True, read_only=True)

    class Meta:
        model = Modelo146
        fields = '__all__'
