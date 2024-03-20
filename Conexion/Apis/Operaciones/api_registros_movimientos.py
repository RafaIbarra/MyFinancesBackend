from rest_framework.response import Response
from rest_framework import status  
from rest_framework.decorators import api_view
from django.db.models import Q

from Conexion.Serializadores.EgresosSerializers import *
from Conexion.Serializadores.IngresosSerializers import *
from Conexion.models import Egresos,Ingresos
from Conexion.Seguridad.obtener_datos_token import obtener_datos_token
from Conexion.Seguridad.validaciones import validacionpeticion

import time
from django.utils import timezone
import ast
from datetime import datetime
from Conexion.Apis.api_generacion_datos import datos_resumen
@api_view(['POST'])
def registroegreso(request):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        data_list = []
        data_errores=''
        id_gasto=request.data['codgasto']
        datasave={
            "id":request.data['codgasto'],
            "gasto":  request.data['gasto'],
            "monto_gasto": request.data['monto'],
            "user": id_user,
            "fecha_gasto": request.data['fecha'],
            "anotacion": request.data['anotacion'],
            "fecha_registro": datetime.now()
            
        }
        
        if validaciones_registros(request.data,'fecha_operacion'):
            fecha_obj = datetime.strptime(datasave['fecha_gasto'], '%Y-%m-%d')
            anno=fecha_obj.year
            mes=fecha_obj.month
        else: 
            mensaje='Seleccione una fecha'
            data_errores = data_errores + mensaje if len(data_errores) == 0 else data_errores + '; ' + mensaje
        
        
            
        if validaciones_registros(datasave['monto_gasto'],'monto')==False:
            mensaje='El monto no puede ser menor a 1'
            data_errores = data_errores + mensaje if len(data_errores) == 0 else data_errores + '; ' + mensaje


        if validaciones_registros(request.data['gasto'],'gastos')==False:
            mensaje='Selecione el concepto de egreso'
            data_errores = data_errores + mensaje if len(data_errores) == 0 else data_errores + '; ' + mensaje

        
        if len(data_errores)==0:

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
            return Response({'error':data_errores},status= status.HTTP_400_BAD_REQUEST)
    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)
    

@api_view(['POST'])
def eliminaregreso(request):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
         

        anno=datetime.now().year
        mes=datetime.now().month
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
            "fecha_registro": datetime.now()
            
        }
        data_errores=''
        
        

        if validaciones_registros(request.data,'fecha_operacion'):
            fecha_obj = datetime.strptime(datasave['fecha_ingreso'], '%Y-%m-%d')
            anno=fecha_obj.year
            mes=fecha_obj.month
        else: 
            mensaje='Seleccione una fecha'
            data_errores = data_errores + mensaje if len(data_errores) == 0 else data_errores + '; ' + mensaje
        
        
            
        if validaciones_registros(datasave['monto_ingreso'],'monto')==False:
            mensaje='El monto no puede ser menor a 1'
            data_errores = data_errores + mensaje if len(data_errores) == 0 else data_errores + '; ' + mensaje


        if validaciones_registros(request.data['producto'],'productos')==False:
            mensaje='Selecione el concepto de ingreso'
            data_errores = data_errores + mensaje if len(data_errores) == 0 else data_errores + '; ' + mensaje

        
        if len(data_errores)==0:
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
            return Response({'error':data_errores},status= status.HTTP_400_BAD_REQUEST)
    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)
    

@api_view(['POST'])
def eliminaringreso(request):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
         
     
        anno=datetime.now().year
        mes=datetime.now().month
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
    

def validaciones_registros(valor,tipo):
    if tipo=='monto':
        if valor is None or valor<1:
            return False
        else:
            return True
        
    if tipo=='fecha_operacion':
        
        if valor is None:
            return False
        else:
            fecha = valor.get('fecha')
            if 'fecha' in valor and bool(fecha):
                return True
            else:
                return False
        
        
    if tipo=='productos':
        consultaproducto=ProductosFinancieros.objects.filter(id__exact=valor).values()
        if not consultaproducto:
            return False
        else:
            return True
        
    if tipo=='gastos':
        consultagasto=Gastos.objects.filter(id__exact=valor).values()
        if not consultagasto:
            return False
        else:
            return True




