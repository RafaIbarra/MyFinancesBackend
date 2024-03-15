from rest_framework import serializers
from Conexion.models import SolicitudPassword
class SolicitudPasswordSerializers(serializers.ModelSerializer):
    class Meta:
        model=SolicitudPassword
        fields= '__all__'

    fecha_creacion = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    fecha_vencimiento = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    