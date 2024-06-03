from rest_framework import serializers
from Conexion.models import MovimientosBeneficios,Meses,EntidadesBeneficios

class MovimientosBeneficiosSerializers(serializers.ModelSerializer):
    NombreEntidad=serializers.SerializerMethodField()
    MesBeneficio=serializers.SerializerMethodField()
    NombreMesBeneficio=serializers.SerializerMethodField()
    AnnoBeneficio=serializers.SerializerMethodField()
    class Meta:
        model= MovimientosBeneficios
        # fields= '__all__'
        fields= ['id'
                 , 'entidad'
                 ,'NombreEntidad'
                 ,'monto'
                 ,'user'
                 ,'fecha_beneficio'
                 ,'anotacion'
                ,'fecha_registro'
                ,'MesBeneficio'
                ,'NombreMesBeneficio'
                ,'AnnoBeneficio'
                
                ]
    fecha_registro = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    def get_NombreEntidad(self, obj):
    
        cod_entidad = obj.retorno_endtidad_id()
        try:
            entidad_obj = EntidadesBeneficios.objects.get(id=cod_entidad)
            return entidad_obj.nombre_entidad
        except EntidadesBeneficios.DoesNotExist:
            return None
        

    def get_MesBeneficio(self, obj):
        return obj.fecha_beneficio.month
    
    def get_NombreMesBeneficio(self, obj):
        numeromes= obj.fecha_beneficio.month
        try:
            mes_obj = Meses.objects.get(numero_mes=numeromes)
            return mes_obj.nombre_mes
        except Meses.DoesNotExist:
            return None
        
    def get_AnnoBeneficio(self, obj):
        return obj.fecha_beneficio.year
