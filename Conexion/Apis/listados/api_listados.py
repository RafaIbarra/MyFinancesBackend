from django.db.models import Q


from rest_framework.response import Response
from rest_framework import status  
from rest_framework.decorators import api_view
import pandas as pd


from Conexion.Seguridad.obtener_datos_token import obtener_datos_token
from Conexion.Seguridad.validaciones import validacionpeticion

from Conexion.models import Gastos,Meses,ProductosFinancieros
# from Conexion.Serializers import GastosSerializers,MesesSerializers,ProductosFinancierosSerializers
from Conexion.Serializadores.GastosSerializers import *
from Conexion.Serializadores.MesesSerializers import *
from Conexion.Serializadores.ProductosFinancierosSerializers import *
from Conexion.Apis.api_generacion_datos import *


@api_view(['POST'])
def misingresos(request,anno,mes):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        lista_ingresos=datos_ingresos(id_user,anno,mes)
        if lista_ingresos:
            # lista_ingresos=sorted(lista_ingresos, key=lambda x: x['fecha_registro'], reverse=False)
             def custom_key(item):
                fecha_ingreso = item.get('fecha_ingreso', '')
                fecha_registro = item.get('fecha_registro', '')
                return (fecha_ingreso, fecha_registro)
             
             lista_ingresos = sorted(lista_ingresos, key=custom_key, reverse=False)
             agrupados=agrupar_periodos_ingresos(lista_ingresos)
            
        return Response(
                {'detalles':lista_ingresos,
                 'agrupados':agrupados
                 }
                ,status= status.HTTP_200_OK)      
        
    else:
            return Response(resp,status= status.HTTP_403_FORBIDDEN)
    
@api_view(['POST'])
def misegresos(request,anno,mes):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        lista_egresos=datos_egresos(id_user,anno,mes)
        if lista_egresos:
            lista_egresos=sorted(lista_egresos, key=lambda x: x['fecha_registro'], reverse=False)
            
        return Response(lista_egresos,status= status.HTTP_200_OK)
        
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
def resumen(request,anno,mes):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True: 
        # Obtener datos de la base de datos
        
        datosresumen=datos_resumen(id_user,anno,mes)
        return Response(datosresumen, status=status.HTTP_200_OK)
        
        
    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)
    


@api_view(['POST'])
def balance(request,anno,mes):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True: 
        # Obtener datos de la base de datos
        
        datosbalance=datos_balance(id_user,anno,mes)
        return Response(datosbalance, status=status.HTTP_200_OK)
       
        
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