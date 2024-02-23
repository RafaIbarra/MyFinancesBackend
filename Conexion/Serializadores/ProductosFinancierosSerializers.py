from rest_framework import serializers
from Conexion.models import ProductosFinancieros,TiposProductosFinancieros,Ingresos
from django.db.models import Q


class ProductosFinancierosSerializers(serializers.ModelSerializer):
    DescripcionTipoProducto=serializers.SerializerMethodField()
    TotalIngresos=serializers.SerializerMethodField()
    CantidadRegistros=serializers.SerializerMethodField()

    
    class Meta:
        model=ProductosFinancieros
        fields= ['id'
                 , 'tipoproducto'
                 ,'DescripcionTipoProducto'
                 ,'user'
                 ,'nombre_producto'
                ,'fecha_registro'
                ,'TotalIngresos'
                ,'CantidadRegistros'
                ]
        
    fecha_registro = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    def get_DescripcionTipoProducto(self, obj):
        
        tipo_producto = obj.retorno_tipo_producto_id()
        try:
            tipo_producto_obj = TiposProductosFinancieros.objects.get(id=tipo_producto)
            return tipo_producto_obj.nombre_tipo_producto
        except TiposProductosFinancieros.DoesNotExist:
            return None
        
    def get_CantidadRegistros(self, obj):

        
        condicion1 = Q(user_id__exact=obj.user_id)
        condicion2 = Q(producto_financiero_id=obj.id)
        mov=list(Ingresos.objects.filter(condicion1 & condicion2 ).values())
        if mov:
            return len(mov)
        else:
            return 0
        
    def get_TotalIngresos(self, obj):

        condicion1 = Q(user_id__exact=obj.user_id)
        condicion2 = Q(producto_financiero_id=obj.id)
        mov=list(Ingresos.objects.filter(condicion1 & condicion2 ).values())
        if mov:
            suma_total = sum(registro['monto_ingreso'] for registro in mov)
        else:
            suma_total=0
        
        return suma_total
        