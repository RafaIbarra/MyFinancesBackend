from django.db.models import Q


from rest_framework.response import Response
from rest_framework import status  
from rest_framework.decorators import api_view
import pandas as pd


from Conexion.Seguridad.obtener_datos_token import obtener_datos_token
from Conexion.Seguridad.validaciones import validacionpeticion

from Conexion.models import Gastos,Meses,ProductosFinancieros,CategoriaGastos
# from Conexion.Serializers import GastosSerializers,MesesSerializers,ProductosFinancierosSerializers
from Conexion.Serializadores.GastosSerializers import *
from Conexion.Serializadores.CategoriasGastosSerializers import *
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
            lista_meses = Meses.objects.order_by('numero_mes')
            result_meses_serializer=MesesSerializers(lista_meses,many=True)
            if result_meses_serializer.data:
             
                return Response(
                        {'detalles':lista_ingresos,
                        'agrupados':agrupados,
                        'datosmeses':result_meses_serializer.data
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
            agrupados=agrupar_periodos_egresos(lista_egresos)
            lista_meses = Meses.objects.order_by('numero_mes')
            result_meses_serializer=MesesSerializers(lista_meses,many=True)
            if result_meses_serializer.data:
                
            
                return Response(
                     {
                          'detalles':lista_egresos,
                          'agrupados':agrupados,
                          'datosmeses':result_meses_serializer.data
                     },
                     
                     status= status.HTTP_200_OK)
        
    else:
            return Response(resp,status= status.HTTP_403_FORBIDDEN)
    
@api_view(['POST'])
def miscategorias(request):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        condicion1 = Q(user_id__exact=id_user)
        
        lista_categorias = CategoriaGastos.objects.filter(condicion1).order_by('nombre_categoria')
        
        if lista_categorias:
            
            result_categoria_serializer=CategoriaGastosSerializers(lista_categorias,many=True)

            if result_categoria_serializer.data:
                 return Response(result_categoria_serializer.data,
                                status= status.HTTP_200_OK)
            else:

                return Response({'message':result_categoria_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response([],status= status.HTTP_200_OK)
        
    else:
            return Response(resp,status= status.HTTP_403_FORBIDDEN)
    
@api_view(['POST'])
def  misdatosregistroegreso (request):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:           
        condicion1 = Q(user_id__exact=id_user)
        # lista=Gastos.objects.filter(condicion1)
        lista = Gastos.objects.filter(condicion1).order_by('categoria', 'nombre_gasto')
        lista_Gastos = CategoriaGastos.objects.filter(condicion1).order_by('nombre_categoria')
        datos_gastos=[]
        datos_categoria=[]
        datos_errores=[]
        if lista and lista_Gastos:
            result_gastos_serializer=GastosSerializers(lista,many=True)
            result_categoria_serializer=CategoriaGastosSerializers(lista_Gastos,many=True)

            if result_gastos_serializer.data:
                 datos_gastos.append(result_gastos_serializer.data)
            else:
                 datos_errores.append({'error gasto':result_gastos_serializer.errors})
            
            if result_categoria_serializer.data:
                 datos_categoria.append(result_categoria_serializer.data)
            else:
                 
                 datos_errores.append({'error categoria':result_categoria_serializer.errors})
                 

            if result_gastos_serializer.data and result_categoria_serializer:
                return Response({
                     'datosgastos':result_gastos_serializer.data,
                     'datoscategorias':result_categoria_serializer.data
                                },
                                status= status.HTTP_200_OK)
            
            else:

                return Response({'message':datos_errores},status= status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response([],status= status.HTTP_200_OK)
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