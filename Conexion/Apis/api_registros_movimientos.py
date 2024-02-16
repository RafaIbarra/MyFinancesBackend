from rest_framework.response import Response
from rest_framework import status  
from rest_framework.decorators import api_view
from django.db.models import Q
from Conexion.Serializers import EgresosSerializers,IngresosSerializers
from Conexion.models import Egresos,Ingresos
from Conexion.obtener_datos_token import obtener_datos_token
from Conexion.validaciones import validacionpeticion
from Conexion.Apis.listados.datos import datos_balance
import time
from django.utils import timezone
import ast
from datetime import datetime

@api_view(['POST'])
def registroegreso(request):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        data_list = []
                    
        
        datasave={
            
            "gasto":  request.data['gasto'],
            "monto_gasto": request.data['monto'],
            "user": id_user,
            "fecha_gasto": request.data['fecha'],
            "anotacion": request.data['anotacion'],
            "fecha_registro": timezone.now()
            
        }
        

        fecha_obj = datetime.strptime(datasave['fecha_gasto'], '%Y-%m-%d')

        anno=fecha_obj.year
        mes=fecha_obj.month
        data_list.append(datasave)
        
        egreso_serializer=EgresosSerializers(data=datasave)
        if egreso_serializer.is_valid():
            egreso_serializer.save()
            data=datos_balance(id_user,anno,mes)
            return Response(data,status= status.HTTP_200_OK)

        return Response({'message':egreso_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)
    

@api_view(['POST'])
def eliminaregreso(request):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
            
        gastosdel=request.data['gastos']
        
        if len(gastosdel)>0:
            for item in gastosdel:
                condicion1 = Q(id__exact=item)
                lista=Egresos.objects.filter(condicion1).values()
                if lista:
                    gasto = Egresos.objects.get(pk=item)
                    gasto.delete()

            return Response({'message':'ok'},status= status.HTTP_200_OK)
        else:
            return Response({'message':'No hay registros que eliminar'},status= status.HTTP_200_OK)
    else:
         return Response(resp,status= status.HTTP_403_FORBIDDEN)
    

@api_view(['POST'])
def misegresos(request,anno,mes):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:           
        condicion1 = Q(user_id__exact=id_user)
        condicion2 = Q(fecha_gasto__year=anno)
        condicion3 = Q(fecha_gasto__month=mes)
        lista=Egresos.objects.filter(condicion1 & condicion2 & condicion3)
                
        if lista:
            result_serializer=EgresosSerializers(lista,many=True)

            if result_serializer.data:
                return Response(result_serializer.data,status= status.HTTP_200_OK)

            return Response({'message':result_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response([],status= status.HTTP_200_OK)
    else:
            return Response(resp,status= status.HTTP_403_FORBIDDEN)
    


@api_view(['POST'])
def registroingreso(request):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        data_list = []
                    
        
        datasave={
            
            "producto_financiero":  request.data['producto'],
            "monto_ingreso": request.data['monto'],
            "user": id_user,
            "fecha_ingreso": request.data['fecha'],
            "anotacion": request.data['anotacion'],
            "fecha_registro": timezone.now()
            
        }
        data_list.append(datasave)

        ingreso_serializer=IngresosSerializers(data=datasave)
        if ingreso_serializer.is_valid():
            ingreso_serializer.save()
            return Response(ingreso_serializer.data,status= status.HTTP_200_OK)

        return Response({'message':ingreso_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
    else:
            return Response(resp,status= status.HTTP_403_FORBIDDEN)
    


@api_view(['POST'])
def misingresos(request,anno,mes):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:           
        condicion1 = Q(user_id__exact=id_user)
        condicion2 = Q(fecha_ingreso__year=anno)
        condicion3 = Q(fecha_ingreso__month=mes)
        lista=Ingresos.objects.filter(condicion1 & condicion2 & condicion3)
                
        if lista:
            result_serializer=IngresosSerializers(lista,many=True)

            if result_serializer.data:
                return Response(result_serializer.data,status= status.HTTP_200_OK)

            return Response({'message':result_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response([],status= status.HTTP_200_OK)
    else:
            return Response(resp,status= status.HTTP_403_FORBIDDEN)