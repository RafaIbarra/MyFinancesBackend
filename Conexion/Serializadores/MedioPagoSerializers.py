from rest_framework import serializers
from Conexion.models import MedioPago

class MedioPagoSerializers(serializers.ModelSerializer):
    class Meta:
        model=MedioPago
        fields= '__all__'
