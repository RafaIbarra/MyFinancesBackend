from rest_framework import serializers
from Conexion.models import Gastos,TiposGastos,CategoriaGastos,Egresos,Meses
from django.db.models import Q

class EgresosSerializers(serializers.ModelSerializer):
    NombreGasto=serializers.SerializerMethodField()
    TipoGasto=serializers.SerializerMethodField()
    CategoriaGasto=serializers.SerializerMethodField()
    MesEgreso=serializers.SerializerMethodField()
    NombreMesEgreso=serializers.SerializerMethodField()
    AnnoEgreso=serializers.SerializerMethodField()
    class Meta:
        model=Egresos
        fields= ['id'
                 , 'gasto'
                 ,'NombreGasto'
                 ,'TipoGasto'
                 ,'CategoriaGasto'
                 ,'monto_gasto'
                 ,'user'
                 ,'fecha_gasto'
                 ,'anotacion'
                ,'fecha_registro'
                ,'MesEgreso'
                ,'NombreMesEgreso'
                ,'AnnoEgreso'
                ]
    fecha_registro = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    def get_NombreGasto(self, obj):
        
        cod_gasto = obj.retorno_gasto_id()
        try:
            tipo_operacion_obj = Gastos.objects.get(id=cod_gasto)
            return tipo_operacion_obj.nombre_gasto
        except Gastos.DoesNotExist:
            return None
        
    def get_TipoGasto(self, obj):
        cod_gasto = obj.retorno_gasto_id()
        
        try:
            gastos_obj = Gastos.objects.get(id=cod_gasto)
            id_tipo_gasto=gastos_obj.tipogasto_id
            tipo_operacion_obj = TiposGastos.objects.get(id=id_tipo_gasto)
            return tipo_operacion_obj.nombre_tipo_gasto
        except TiposGastos.DoesNotExist:
            return None
        
    def get_CategoriaGasto(self, obj):
        cod_gasto = obj.retorno_gasto_id()
        
        try:
            gastos_obj = Gastos.objects.get(id=cod_gasto)
            id_categoria_gasto=gastos_obj.categoria_id
            tipo_operacion_obj = CategoriaGastos.objects.get(id=id_categoria_gasto)
            return tipo_operacion_obj.nombre_categoria
        except CategoriaGastos.DoesNotExist:
            return None
        
    def get_MesEgreso(self, obj):
        return obj.fecha_gasto.month
    
    def get_NombreMesEgreso(self, obj):
        numeromes= obj.fecha_gasto.month
        try:
            mes_obj = Meses.objects.get(numero_mes=numeromes)
            return mes_obj.nombre_mes
        except TiposGastos.DoesNotExist:
            return None
    
    def get_AnnoEgreso(self, obj):
        return obj.fecha_gasto.year