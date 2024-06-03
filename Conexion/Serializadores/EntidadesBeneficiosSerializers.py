from rest_framework import serializers
from Conexion.models import EntidadesBeneficios

class EntidadesBeneficiosSerializers(serializers.ModelSerializer):
    class Meta:
        model=EntidadesBeneficios
        fields= '__all__'
