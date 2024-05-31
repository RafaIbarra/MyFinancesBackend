from rest_framework import serializers
from Conexion.models import EgresosDistribucion

class EgresosDistribucionSerializers(serializers.ModelSerializer):
    class Meta:
        model=EgresosDistribucion
        fields= '__all__'

    
