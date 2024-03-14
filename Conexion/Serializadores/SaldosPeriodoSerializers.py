from rest_framework import serializers

class SaldosPeriodoSerializers(serializers.Serializer):
    AnnoOperacion=serializers.IntegerField()
    NombreMesOperacion=serializers.CharField(max_length=200,allow_blank=True)
    Periodo=serializers.CharField(max_length=200,allow_blank=True)
    TotalIngreso=serializers.IntegerField()
    TotalEgreso=serializers.IntegerField()
    Saldo=serializers.IntegerField()
    PorcentajeEgreso=serializers.DecimalField(max_digits=5, decimal_places=2)
    PorcentajeSaldo=serializers.DecimalField(max_digits=5, decimal_places=2)
    

    def validate(self,data):
        return data