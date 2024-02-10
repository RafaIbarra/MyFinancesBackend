from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from Conexion.models import *
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','first_name','email','is_active')


class UsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model=Usuarios
        fields= '__all__'


class SesionesActivasSerializers(serializers.ModelSerializer):
    class Meta:
        model=SesionesActivas
        fields= '__all__'


class TiposGastosSerializers(serializers.ModelSerializer):
    class Meta:
        model=TiposGastos
        fields= '__all__'


class CategoriaGastosSerializers(serializers.ModelSerializer):
    
    class Meta:
        model=CategoriaGastos
        fields= '__all__'


class GastosSerializers(serializers.ModelSerializer):
    DescripcionTipoGasto=serializers.SerializerMethodField()
    DescripcionCategoriaGasto=serializers.SerializerMethodField()
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
                ]
        

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


class EgresosSerializers(serializers.ModelSerializer):
    NombreGasto=serializers.SerializerMethodField()
    TipoGasto=serializers.SerializerMethodField()
    CategoriaGasto=serializers.SerializerMethodField()
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
                ]
        
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
        


class TiposProductosFinancierosSerializers(serializers.ModelSerializer):
    class Meta:
        model=TiposProductosFinancieros
        fields= '__all__'



class ProductosFinancierosSerializers(serializers.ModelSerializer):
    DescripcionTipoProducto=serializers.SerializerMethodField()
    
    class Meta:
        model=ProductosFinancieros
        fields= ['id'
                 , 'tipoproducto'
                 ,'DescripcionTipoProducto'
                 ,'user'
                 ,'nombre_producto'
                ,'fecha_registro'
                ]
        

    def get_DescripcionTipoProducto(self, obj):
        
        tipo_producto = obj.retorno_tipo_producto_id()
        try:
            tipo_producto_obj = TiposProductosFinancieros.objects.get(id=tipo_producto)
            return tipo_producto_obj.nombre_tipo_producto
        except TiposProductosFinancieros.DoesNotExist:
            return None
        
    

class IngresosSerializers(serializers.ModelSerializer):
    NombreIngreso=serializers.SerializerMethodField()
    TipoIngreso=serializers.SerializerMethodField()
    
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
                ]
        
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
        
 