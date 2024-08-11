from django.contrib.auth.models import User
from rest_framework import serializers
from Conexion.models import Egresos,EgresosDistribucion,Gastos,Ingresos,Usuarios,CategoriaGastos,MovimientosBeneficios,ProductosFinancieros

class UsersSerializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields= '__all__'


class MigracionCategoriaGastosSerializers(serializers.ModelSerializer):
    Identificacionuser=serializers.SerializerMethodField()
    class Meta:
        model=CategoriaGastos
        fields= ['id','user','nombre_categoria','fecha_registro','Identificacionuser']

    def get_Identificacionuser(self, obj):
        try:
           nombre_usuario = obj.user.user_name
           return nombre_usuario
        except Usuarios.DoesNotExist:
            return None

class MigracionEgresosSerializers(serializers.ModelSerializer):
    Identificacionuser=serializers.SerializerMethodField()
    NombreGasto=serializers.SerializerMethodField()
    class Meta:
        model=Egresos
        fields= ['id','gasto','monto_gasto','user','fecha_gasto','anotacion','fecha_registro','Identificacionuser','NombreGasto']

    def get_Identificacionuser(self, obj):
        try:
           nombre_usuario = obj.user.user_name
           return nombre_usuario
        except Usuarios.DoesNotExist:
            return None
        
    def get_NombreGasto(self, obj):
        try:
           nombre_gasto = obj.gasto.nombre_gasto
           return nombre_gasto
        except Gastos.DoesNotExist:
            return None



class MigracionEgresosDistribucionSerializers(serializers.ModelSerializer):
    class Meta:
        model=EgresosDistribucion
        fields= '__all__'
        
class MigracionGastosSerializers(serializers.ModelSerializer):
    class Meta:
        model=Gastos
        fields= '__all__'

class MigracionIngresosSerializers(serializers.ModelSerializer):
    class Meta:
        model=Ingresos
        fields= '__all__'

class MigracionMovimientosBeneficiosSerializers(serializers.ModelSerializer):
    class Meta:
        model=MovimientosBeneficios
        fields= '__all__'

class MigracionProductosFinancierosSerializers(serializers.ModelSerializer):
    class Meta:
        model=ProductosFinancieros
        fields= '__all__'