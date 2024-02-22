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
from Conexion.Apis.listados.datos import datos_egresos,datos_ingresos,datos_balance,datos_resumen
@api_view(['POST'])
def registroegreso(request):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        data_list = []
                    
        id_gasto=request.data['codgasto']
        datasave={
            "id":request.data['codgasto'],
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
        if id_gasto>0:
            condicion1 = Q(id__exact=id_gasto)
            dato_existente=Egresos.objects.filter(condicion1 )
            

            if dato_existente:
                
                existente=Egresos.objects.get(condicion1)
                
                egreso_serializer=EgresosSerializers(existente,data=datasave)

            else:
                return Response({'message':'El registro a actualizar no existe'},status= status.HTTP_400_BAD_REQUEST)
            

        else:

            egreso_serializer=EgresosSerializers(data=datasave)

        if egreso_serializer.is_valid():
            egreso_serializer.save()
            data=datos_resumen(id_user,anno,mes)
            return Response(data,status= status.HTTP_200_OK)

        return Response({'message':egreso_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)
    

@api_view(['POST'])
def eliminaregreso(request):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
         
        # fecha_obj = datetime.strptime(timezone.now(), '%Y-%m-%d')
        anno=timezone.now().year
        mes=timezone.now().month
        gastosdel=request.data['gastos']

        if type(gastosdel)==str:
            gastosdel=ast.literal_eval(gastosdel)

        if len(gastosdel)>0:
            for item in gastosdel:
                condicion1 = Q(id__exact=item)
                lista=Egresos.objects.filter(condicion1).values()
                if lista:
                
                    anno=lista[0]['fecha_gasto'].year
                    mes=lista[0]['fecha_gasto'].month
                    
                    gasto = Egresos.objects.get(pk=item)
                    gasto.delete()


            data=datos_resumen(id_user,anno,mes)
            return Response(data,status= status.HTTP_200_OK)
            
        else:
            return Response({'message':'No hay registros que eliminar'},status= status.HTTP_200_OK)
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
def registroingreso(request):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        data_list = []
                    
        id_ingreso=request.data['codingreso']
        datasave={
            "id":request.data['codingreso'],
            "producto_financiero":  request.data['producto'],
            "monto_ingreso": request.data['monto'],
            "user": id_user,
            "fecha_ingreso": request.data['fecha'],
            "anotacion": request.data['anotacion'],
            "fecha_registro": timezone.now()
            
        }
        fecha_obj = datetime.strptime(datasave['fecha_ingreso'], '%Y-%m-%d')
        anno=fecha_obj.year
        mes=fecha_obj.month
        if datasave['monto_ingreso']>0:
            data_list.append(datasave)
            if id_ingreso>0:
                condicion1 = Q(id__exact=id_ingreso)
                dato_existente=Ingresos.objects.filter(condicion1 )
                

                if dato_existente:
                    
                    existente=Ingresos.objects.get(condicion1)
                    
                    ingreso_serializer=IngresosSerializers(existente,data=datasave)

                else:
                    return Response({'message':'El registro a actualizar no existe'},status= status.HTTP_400_BAD_REQUEST)
                

            else:

                ingreso_serializer=IngresosSerializers(data=datasave)


            if ingreso_serializer.is_valid():
                ingreso_serializer.save()
                data=datos_resumen(id_user,anno,mes)
                return Response(data,status= status.HTTP_200_OK)

            return Response({'message':ingreso_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error':'El monto no puede ser menor a 1'},status= status.HTTP_400_BAD_REQUEST)
    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)
    

@api_view(['POST'])
def eliminaringreso(request):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
         
        # fecha_obj = datetime.strptime(timezone.now(), '%Y-%m-%d')
        anno=timezone.now().year
        mes=timezone.now().month
        ingresosdel=request.data['ingresos']

        if type(ingresosdel)==str:
            ingresosdel=ast.literal_eval(ingresosdel)

        if len(ingresosdel)>0:
            for item in ingresosdel:
                condicion1 = Q(id__exact=item)
                lista=Ingresos.objects.filter(condicion1).values()
                if lista:
                
                    anno=lista[0]['fecha_ingreso'].year
                    mes=lista[0]['fecha_ingreso'].month
                    
                    ingreso = Ingresos.objects.get(pk=item)
                    ingreso.delete()


            data=datos_resumen(id_user,anno,mes)
            return Response(data,status= status.HTTP_200_OK)
            
        else:
            return Response({'message':'No hay registros que eliminar'},status= status.HTTP_200_OK)
    else:
         return Response(resp,status= status.HTTP_403_FORBIDDEN)
    
    


@api_view(['POST'])
def misingresos(request,anno,mes):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        lista_ingresos=datos_ingresos(id_user,anno,mes)
        if lista_ingresos:
            lista_ingresos=sorted(lista_ingresos, key=lambda x: x['fecha_registro'], reverse=False)
            
        return Response(lista_ingresos,status= status.HTTP_200_OK)      
        
    else:
            return Response(resp,status= status.HTTP_403_FORBIDDEN)