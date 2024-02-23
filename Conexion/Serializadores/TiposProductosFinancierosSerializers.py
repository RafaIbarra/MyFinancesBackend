from rest_framework import serializers
from Conexion.models import TiposProductosFinancieros
class TiposProductosFinancierosSerializers(serializers.ModelSerializer):
    class Meta:
        model=TiposProductosFinancieros
        fields= '__all__'