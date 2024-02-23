from rest_framework import serializers
from Conexion.models import Gastos,TiposGastos,CategoriaGastos,Egresos
from django.db.models import Q

class GastosSerializers(serializers.ModelSerializer):
    DescripcionTipoGasto=serializers.SerializerMethodField()
    DescripcionCategoriaGasto=serializers.SerializerMethodField()
    TotalEgresos=serializers.SerializerMethodField()
    CantidadRegistros=serializers.SerializerMethodField()
    class Meta:
        model=Gastos
        fields= ['id'
                 , 'tipogasto'
                 ,'DescripcionTipoGasto'
                 ,'categoria'
                 ,'DescripcionCategoriaGasto'
                 ,'user'
                 ,'nombre_gasto'
                ,'fecha_registro'
                ,'TotalEgresos'
                ,'CantidadRegistros'
                ]
        
    fecha_registro = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    def get_DescripcionTipoGasto(self, obj):
        
        tipo_gasto = obj.retorno_tipo_gasto_id()
        try:
            tipo_operacion_obj = TiposGastos.objects.get(id=tipo_gasto)
            return tipo_operacion_obj.nombre_tipo_gasto
        except TiposGastos.DoesNotExist:
            return None
        
    def get_DescripcionCategoriaGasto(self, obj):
        cat_gasto = obj.retorno_categoria_gasto_id()
        try:
            tipo_operacion_obj = CategoriaGastos.objects.get(id=cat_gasto)
            return tipo_operacion_obj.nombre_categoria
        except CategoriaGastos.DoesNotExist:
            return None
        
    def get_CantidadRegistros(self, obj):

        
        condicion1 = Q(user_id__exact=obj.user_id)
        condicion2 = Q(gasto=obj.id)
        mov=list(Egresos.objects.filter(condicion1 & condicion2 ).values())
        if mov:
            return len(mov)
        else:
            return 0
        
    def get_TotalEgresos(self, obj):

        condicion1 = Q(user_id__exact=obj.user_id)
        condicion2 = Q(gasto=obj.id)
        mov=list(Egresos.objects.filter(condicion1 & condicion2 ).values())
        if mov:
            suma_total = sum(registro['monto_gasto'] for registro in mov)
        else:
            suma_total=0
        
        return suma_total