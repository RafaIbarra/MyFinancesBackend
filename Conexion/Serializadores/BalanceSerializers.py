from rest_framework import serializers

class BalanceSerializers(serializers.Serializer):
    Descripcion=serializers.CharField(max_length=200,allow_blank=True)
    Tipo=serializers.CharField(max_length=200,allow_blank=True)
    MontoIngreso=serializers.IntegerField()
    Codigo=serializers.IntegerField()
    MontoEgreso=serializers.IntegerField()
    Saldo=serializers.IntegerField()

    def validate(self,data):
        return data
    
class MediosResumenSerializers(serializers.Serializer):
    MedioPago=serializers.CharField(max_length=200,allow_blank=True)
    MontoMedio=serializers.IntegerField()
    CantidadRegistros=serializers.IntegerField()
 
    def validate(self,data):
        return data
    

class ConceptosResumenSerializers(serializers.Serializer):
    NombreGasto=serializers.CharField(max_length=200,allow_blank=True)
    MontoConcepto=serializers.IntegerField()
    CantidadRegistros=serializers.IntegerField()
 
    def validate(self,data):
        return data