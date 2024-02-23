from rest_framework import serializers
from Conexion.models import TiposGastos
class TiposGastosSerializers(serializers.ModelSerializer):
    class Meta:
        model=TiposGastos
        fields= '__all__'