from rest_framework import serializers
from Conexion.models import CategoriaGastos
class CategoriaGastosSerializers(serializers.ModelSerializer):
    
    class Meta:
        model=CategoriaGastos
        fields= '__all__'