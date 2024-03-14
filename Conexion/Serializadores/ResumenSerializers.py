from rest_framework import serializers
from Conexion.Serializadores.BalanceSerializers import *
from Conexion.Serializadores.SaldosPeriodoSerializers import *

class ResumenSerializers(serializers.Serializer):
    Resumen = BalanceSerializers(many=True)
    Ingresos = serializers.SerializerMethodField()
    Egresos = serializers.SerializerMethodField()
    Saldos=SaldosPeriodoSerializers(many=True)

    def get_Ingresos(self, obj):
        
        ingresos_data = obj['Ingresos']
        return ingresos_data
    
    def get_Egresos(self, obj):
        
        egresos_data = obj['Egresos']
        return egresos_data