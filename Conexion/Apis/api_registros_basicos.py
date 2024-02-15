from rest_framework.response import Response
from rest_framework import status  
from rest_framework.decorators import api_view
from django.db.models import Q
from Conexion.Serializers import GastosSerializers,ProductosFinancierosSerializers,MesesSerializers
from Conexion.models import Gastos,ProductosFinancieros,Meses
from Conexion.obtener_datos_token import obtener_datos_token
from Conexion.validaciones import validacionpeticion
import time
from django.utils import timezone
@api_view(['POST'])
def registrogasto(request):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        data_list = []
                    
        
        datasave={
            
            "tipogasto":  request.data['tipogasto'],
            "categoria": request.data['categoria'],
            "user": id_user,
            "nombre_gasto": request.data['nombre'],
            
            "fecha_registro": timezone.now()
            
        }
        data_list.append(datasave)

        gasto_serializer=GastosSerializers(data=datasave)
        if gasto_serializer.is_valid():
            gasto_serializer.save()
            return Response(gasto_serializer.data,status= status.HTTP_200_OK)

        return Response({'message':gasto_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
    else:
            return Response(resp,status= status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def misgastos(request):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:           
        condicion1 = Q(user_id__exact=id_user)
        # lista=Gastos.objects.filter(condicion1)
        lista = Gastos.objects.filter(condicion1).order_by('categoria', 'nombre_gasto')

                
        if lista:
            result_serializer=GastosSerializers(lista,many=True)

            if result_serializer.data:
                return Response(result_serializer.data,status= status.HTTP_200_OK)

            return Response({'message':result_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response([],status= status.HTTP_200_OK)
    else:
            return Response(resp,status= status.HTTP_403_FORBIDDEN)
    
@api_view(['POST'])
def registroproductofinanciero(request):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        data_list = []
        datasave={
            "tipoproducto":  request.data['tipoproducto'],
            "user": id_user,
            "nombre_producto": request.data['nombre'],
            "fecha_registro": timezone.now()
            
        }
        data_list.append(datasave)

        producto_serializer=ProductosFinancierosSerializers(data=datasave)
        if producto_serializer.is_valid():
            producto_serializer.save()
            return Response(producto_serializer.data,status= status.HTTP_200_OK)

        return Response({'message':producto_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
    else:
            return Response(resp,status= status.HTTP_403_FORBIDDEN)
    


@api_view(['POST'])
def misproductosfinancieros(request):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:           
        condicion1 = Q(user_id__exact=id_user)
        lista=ProductosFinancieros.objects.filter(condicion1)
                
        if lista:
            result_serializer=ProductosFinancierosSerializers(lista,many=True)

            if result_serializer.data:
                return Response(result_serializer.data,status= status.HTTP_200_OK)

            return Response({'message':result_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response([],status= status.HTTP_200_OK)
    else:
            return Response(resp,status= status.HTTP_403_FORBIDDEN)
    


@api_view(['POST'])
def meses(request):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:           
        
        
        lista = Meses.objects.order_by('numero_mes')

                
        if lista:
            result_serializer=MesesSerializers(lista,many=True)

            if result_serializer.data:
                return Response(result_serializer.data,status= status.HTTP_200_OK)

            return Response({'message':result_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response([],status= status.HTTP_200_OK)
    else:
            return Response(resp,status= status.HTTP_403_FORBIDDEN)