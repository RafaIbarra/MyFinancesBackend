from rest_framework import serializers
from Conexion.models import Ingresos,ProductosFinancieros,Gastos,TiposProductosFinancieros,TiposGastos,Meses

class IngresosSerializers(serializers.ModelSerializer):
    NombreIngreso=serializers.SerializerMethodField()
    TipoIngreso=serializers.SerializerMethodField()
    MesIngreso=serializers.SerializerMethodField()
    NombreMesIngreso=serializers.SerializerMethodField()
    AnnoIngreso=serializers.SerializerMethodField()
    
    class Meta:
        model=Ingresos
        fields= ['id'
                 , 'producto_financiero'
                 ,'NombreIngreso'
                 ,'TipoIngreso'
                 ,'monto_ingreso'
                 ,'user'
                 ,'fecha_ingreso'
                 ,'anotacion'
                ,'fecha_registro'
                ,'MesIngreso'
                ,'NombreMesIngreso'
                ,'AnnoIngreso'
                ]
    fecha_registro = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')  
    def get_NombreIngreso(self, obj):
        
        cod_producto = obj.retorno_producto_financiero_id()
        try:
            tipo_producto_obj = ProductosFinancieros.objects.get(id=cod_producto)
            return tipo_producto_obj.nombre_producto
        except Gastos.DoesNotExist:
            return None
        
    def get_TipoIngreso(self, obj):
        cod_producto = obj.retorno_producto_financiero_id()
        
        try:
            tipo_producto_obj = ProductosFinancieros.objects.get(id=cod_producto)
            id_tipo_producto=tipo_producto_obj.tipoproducto_id
            tipo_operacion_obj = TiposProductosFinancieros.objects.get(id=id_tipo_producto)
            return tipo_operacion_obj.nombre_tipo_producto
        except TiposGastos.DoesNotExist:
            return None
        
    def get_MesIngreso(self, obj):
        return obj.fecha_ingreso.month
    
    def get_NombreMesIngreso(self, obj):
        numeromes= obj.fecha_ingreso.month
        try:
            mes_obj = Meses.objects.get(numero_mes=numeromes)
            return mes_obj.nombre_mes
        except TiposGastos.DoesNotExist:
            return None

    
    def get_AnnoIngreso(self, obj):
        return obj.fecha_ingreso.year