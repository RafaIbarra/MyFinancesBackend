from rest_framework.response import Response
from rest_framework import status  
from rest_framework.decorators import api_view
from django.db.models import Q
from django.contrib.auth.models import User
from Conexion.models import *
from Conexion.Serializadores.MigracionesSerializers import *
from Conexion.Serializadores.CategoriasGastosSerializers import *
from Conexion.Serializadores.EntidadesBeneficiosSerializers import *
from Conexion.Serializadores.GastosSerializers import *
from Conexion.Serializadores.MedioPagoSerializers import *
from Conexion.Serializadores.MesesSerializers import *
from Conexion.Serializadores.MovimientosBeneficiosSerializers import *
from Conexion.Serializadores.TiposGastosSerializers import *
from Conexion.Serializadores.TiposProductosFinancierosSerializers import *
from Conexion.Serializadores.UsuariosSerializers import *
from Conexion.Seguridad.obtener_datos_token import obtener_datos_token
from Conexion.Seguridad.validaciones import validacionpeticion

@api_view(['POST'])
def migracionusers(request):

     token_sesion,usuario,id_user =obtener_datos_token(request)
     resp=validacionpeticion(token_sesion)
     if resp==True:           
        
        
        lista = User.objects.order_by('id')
        
                
        if lista:
            result_serializer=UsersSerializers(lista,many=True)

            if result_serializer.data:
                return Response(result_serializer.data,status= status.HTTP_200_OK)

            return Response({'message':result_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response([],status= status.HTTP_200_OK)
     else:
             return Response(resp,status= status.HTTP_403_FORBIDDEN)

@api_view(['POST'])
def migracioncategoriagastos(request):

     token_sesion,usuario,id_user =obtener_datos_token(request)
     resp=validacionpeticion(token_sesion)
     if resp==True:           
        
        
        lista = CategoriaGastos.objects.order_by('id')
        
                
        if lista:
            result_serializer=MigracionCategoriaGastosSerializers(lista,many=True)

            if result_serializer.data:
                return Response(result_serializer.data,status= status.HTTP_200_OK)

            return Response({'message':result_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response([],status= status.HTTP_200_OK)
     else:
             return Response(resp,status= status.HTTP_403_FORBIDDEN)
     
@api_view(['POST'])
def migracionegresos(request):

     token_sesion,usuario,id_user =obtener_datos_token(request)
     resp=validacionpeticion(token_sesion)
     if resp==True:           
        
        
        lista = Egresos.objects.order_by('id')
        
                
        if lista:
            result_serializer=MigracionEgresosSerializers(lista,many=True)

            if result_serializer.data:
                return Response(result_serializer.data,status= status.HTTP_200_OK)

            return Response({'message':result_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response([],status= status.HTTP_200_OK)
     else:
             return Response(resp,status= status.HTTP_403_FORBIDDEN)
     
@api_view(['POST'])
def migracionegresosdistribucion(request):

     token_sesion,usuario,id_user =obtener_datos_token(request)
     resp=validacionpeticion(token_sesion)
     if resp==True:           
        
        
        lista = EgresosDistribucion.objects.order_by('id')
        
                
        if lista:
            result_serializer=MigracionEgresosDistribucionSerializers(lista,many=True)

            if result_serializer.data:
                return Response(result_serializer.data,status= status.HTTP_200_OK)

            return Response({'message':result_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response([],status= status.HTTP_200_OK)
     else:
             return Response(resp,status= status.HTTP_403_FORBIDDEN)

@api_view(['POST'])
def migracionentidadesbeneficiones(request):

     token_sesion,usuario,id_user =obtener_datos_token(request)
     resp=validacionpeticion(token_sesion)
     if resp==True:           
        
        
        lista = EntidadesBeneficios.objects.order_by('id')
        
                
        if lista:
            result_serializer=EntidadesBeneficiosSerializers(lista,many=True)

            if result_serializer.data:
                return Response(result_serializer.data,status= status.HTTP_200_OK)

            return Response({'message':result_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response([],status= status.HTTP_200_OK)
     else:
             return Response(resp,status= status.HTTP_403_FORBIDDEN)

@api_view(['POST'])
def migraciongastos(request):

     token_sesion,usuario,id_user =obtener_datos_token(request)
     resp=validacionpeticion(token_sesion)
     if resp==True:           
        
        
        lista = Gastos.objects.order_by('id')
        
                
        if lista:
            result_serializer=MigracionGastosSerializers(lista,many=True)

            if result_serializer.data:
                return Response(result_serializer.data,status= status.HTTP_200_OK)

            return Response({'message':result_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response([],status= status.HTTP_200_OK)
     else:
             return Response(resp,status= status.HTTP_403_FORBIDDEN)
     
@api_view(['POST'])
def migracioningresos(request):

     token_sesion,usuario,id_user =obtener_datos_token(request)
     resp=validacionpeticion(token_sesion)
     if resp==True:           
        
        
        lista = Ingresos.objects.order_by('id')
        
                
        if lista:
            result_serializer=MigracionIngresosSerializers(lista,many=True)

            if result_serializer.data:
                return Response(result_serializer.data,status= status.HTTP_200_OK)

            return Response({'message':result_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response([],status= status.HTTP_200_OK)
     else:
             return Response(resp,status= status.HTTP_403_FORBIDDEN)
     
@api_view(['POST'])
def migracionmediopago(request):

     token_sesion,usuario,id_user =obtener_datos_token(request)
     resp=validacionpeticion(token_sesion)
     if resp==True:           
        
        
        lista = MedioPago.objects.order_by('id')
        
                
        if lista:
            result_serializer=MedioPagoSerializers(lista,many=True)

            if result_serializer.data:
                return Response(result_serializer.data,status= status.HTTP_200_OK)

            return Response({'message':result_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response([],status= status.HTTP_200_OK)
     else:
             return Response(resp,status= status.HTTP_403_FORBIDDEN)
     
@api_view(['POST'])
def migracionmeses(request):

     token_sesion,usuario,id_user =obtener_datos_token(request)
     resp=validacionpeticion(token_sesion)
     if resp==True:           
        
        
        lista = Meses.objects.order_by('id')
        
                
        if lista:
            result_serializer=MesesSerializers(lista,many=True)

            if result_serializer.data:
                return Response(result_serializer.data,status= status.HTTP_200_OK)

            return Response({'message':result_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response([],status= status.HTTP_200_OK)
     else:
             return Response(resp,status= status.HTTP_403_FORBIDDEN)
     
@api_view(['POST'])
def migracionmovimientosbeneficios(request):

     token_sesion,usuario,id_user =obtener_datos_token(request)
     resp=validacionpeticion(token_sesion)
     if resp==True:           
        
        
        lista = MovimientosBeneficios.objects.order_by('id')
        
                
        if lista:
            result_serializer=MigracionMovimientosBeneficiosSerializers(lista,many=True)

            if result_serializer.data:
                return Response(result_serializer.data,status= status.HTTP_200_OK)

            return Response({'message':result_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response([],status= status.HTTP_200_OK)
     else:
             return Response(resp,status= status.HTTP_403_FORBIDDEN)
     

@api_view(['POST'])
def migracionproductosfinancieros(request):

     token_sesion,usuario,id_user =obtener_datos_token(request)
     resp=validacionpeticion(token_sesion)
     if resp==True:           
        
        
        lista = ProductosFinancieros.objects.order_by('id')
        
                
        if lista:
            result_serializer=MigracionProductosFinancierosSerializers(lista,many=True)

            if result_serializer.data:
                return Response(result_serializer.data,status= status.HTTP_200_OK)

            return Response({'message':result_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response([],status= status.HTTP_200_OK)
     else:
             return Response(resp,status= status.HTTP_403_FORBIDDEN)
     
@api_view(['POST'])
def migraciontiposgastos(request):

     token_sesion,usuario,id_user =obtener_datos_token(request)
     resp=validacionpeticion(token_sesion)
     if resp==True:           
        
        
        lista = TiposGastos.objects.order_by('id')
        
                
        if lista:
            result_serializer=TiposGastosSerializers(lista,many=True)

            if result_serializer.data:
                return Response(result_serializer.data,status= status.HTTP_200_OK)

            return Response({'message':result_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response([],status= status.HTTP_200_OK)
     else:
             return Response(resp,status= status.HTTP_403_FORBIDDEN)
     
@api_view(['POST'])
def migraciontiposproductosfinancieros(request):

     token_sesion,usuario,id_user =obtener_datos_token(request)
     resp=validacionpeticion(token_sesion)
     if resp==True:           
        
        
        lista = TiposProductosFinancieros.objects.order_by('id')
        
                
        if lista:
            result_serializer=TiposProductosFinancierosSerializers(lista,many=True)

            if result_serializer.data:
                return Response(result_serializer.data,status= status.HTTP_200_OK)

            return Response({'message':result_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response([],status= status.HTTP_200_OK)
     else:
             return Response(resp,status= status.HTTP_403_FORBIDDEN)
     
@api_view(['POST'])
def migracionusuarios(request):

     token_sesion,usuario,id_user =obtener_datos_token(request)
     resp=validacionpeticion(token_sesion)
     if resp==True:           
        
        
        lista = Usuarios.objects.order_by('id')
        
                
        if lista:
            result_serializer=UsuariosSerializer(lista,many=True)

            if result_serializer.data:
                return Response(result_serializer.data,status= status.HTTP_200_OK)

            return Response({'message':result_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response([],status= status.HTTP_200_OK)
     else:
             return Response(resp,status= status.HTTP_403_FORBIDDEN)