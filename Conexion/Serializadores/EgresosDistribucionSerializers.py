from rest_framework import serializers
from Conexion.models import EgresosDistribucion

class EgresosDistribucionSerializers(serializers.ModelSerializer):
    class Meta:
        model=EgresosDistribucion
        fields= '__all__'

    # def create(self, validated_data):
    #     # Permitir la creación de múltiples registros
    #     if isinstance(validated_data, list):
    #         return EgresosDistribucion.objects.bulk_create([EgresosDistribucion(**item) for item in validated_data])
    #     return super().create(validated_data)
