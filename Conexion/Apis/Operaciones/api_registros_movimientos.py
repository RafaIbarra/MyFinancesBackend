from rest_framework.response import Response
from rest_framework import status  
from rest_framework.decorators import api_view
from django.db.models import Q

from Conexion.Serializadores.EgresosSerializers import *
from Conexion.Serializadores.IngresosSerializers import *
from Conexion.Serializadores.EgresosDistribucionSerializers import *
from Conexion.Serializadores.MovimientosBeneficiosSerializers import *

from Conexion.models import Egresos,Ingresos,EgresosDistribucion,MovimientosBeneficios
from Conexion.Seguridad.obtener_datos_token import obtener_datos_token
from Conexion.Seguridad.validaciones import validacionpeticion
import json
import time
from django.utils import timezone
import ast
from datetime import datetime
from Conexion.Apis.api_generacion_datos import datos_resumen,imagenes_mes,datos_egresos,movile_imagenes_mes_saldo,movile_imagenes_mes_egreso,movile_imagenes_mes_ingreso
@api_view(['POST'])
def registroegreso(request):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        data_list = []
        data_errores=''
        campos_requeridos = ["mediopago", "monto"]
        
        datos_distribucion=json.loads(request.data['distribucion'])
        id_gasto=int(request.data['codgasto'])
        # suma_montos = sum(item['monto'] for item in datos_distribucion)
        # datasave={
        #     "id":request.data['codgasto'],
        #     "gasto":  request.data['gasto'],
        #     "monto_gasto":suma_montos,
        #     "user": id_user,
        #     "fecha_gasto": request.data['fecha'],
        #     "anotacion": request.data['anotacion'],
        #     "fecha_registro": datetime.now()
            
        # }
        
        controlcampos=True
        for item in datos_distribucion:
            for campo in campos_requeridos:
                if campo not in item:
                    controlcampos=False
                    
        if controlcampos!=True:
            suma_montos=0
            mensaje='Falta de campos en medio de pagos'
            data_errores = data_errores + mensaje if len(data_errores) == 0 else data_errores + '; ' + mensaje
        
        if controlcampos:
             suma_montos = sum(item['monto'] for item in datos_distribucion)

        if suma_montos<1:
            mensaje='El monto no puede ser menor a 1'
            data_errores = data_errores + mensaje if len(data_errores) == 0 else data_errores + '; ' + mensaje
        
        if validaciones_registros(request.data,'fecha_operacion'):
            fecha_obj = datetime.strptime(request.data['fecha'], '%Y-%m-%d')
            anno=fecha_obj.year
            mes=fecha_obj.month
        else: 
            mensaje='Seleccione una fecha'
            data_errores = data_errores + mensaje if len(data_errores) == 0 else data_errores + '; ' + mensaje
        

        if validaciones_registros(request.data['gasto'],'gastos')==False:
            mensaje='Selecione el concepto de egreso'
            data_errores = data_errores + mensaje if len(data_errores) == 0 else data_errores + '; ' + mensaje

        
        if len(data_errores)==0:
            datasave={
                "id":request.data['codgasto'],
                "gasto":  request.data['gasto'],
                "monto_gasto":suma_montos,
                "user": id_user,
                "fecha_gasto": request.data['fecha'],
                "anotacion": request.data['anotacion'],
                "fecha_registro": datetime.now()
            
            }
            data_list.append(datasave)
            if id_gasto>0:
                
                condicion1 = Q(id__exact=id_gasto)
                dato_existente=Egresos.objects.filter(condicion1)
                if dato_existente:
                    
                    existente=Egresos.objects.get(condicion1)
                    
                    egreso_serializer=EgresosSerializers(existente,data=datasave)

                else:
                    return Response({'message':'El registro a actualizar no existe'},status= status.HTTP_400_BAD_REQUEST)
                

            else:

                egreso_serializer=EgresosSerializers(data=datasave)

            if egreso_serializer.is_valid():
                
                egreso_instance =egreso_serializer.save()
                if id_gasto == 0:
                    id_gasto_gen=egreso_instance.id
                    for item in datos_distribucion:
                        item['egresos'] = id_gasto_gen
                    
                    EgresosDistribucion.objects.filter(egresos_id=id_gasto_gen).delete()
                    serializer = EgresosDistribucionSerializers(data=datos_distribucion, many=True)
                    if serializer.is_valid():
                        serializer.save()
                        data=datos_resumen(id_user,anno,mes)
                        return Response(data,status= status.HTTP_200_OK)
                    else:
                        
                        t=Egresos.objects.get(id=id_gasto_gen)
                        t.delete()
                        return Response({'error':'Error en almacenado de medios pagos'},status= status.HTTP_400_BAD_REQUEST)
                else:
                    
                    registros_existentes = EgresosDistribucion.objects.filter(egresos_id=id_gasto)
                    registros_existentes_dict = [
                        {"egresos": registro.egresos_id, "mediopago": registro.mediopago_id, "monto": registro.monto}
                        for registro in registros_existentes
                    ]
  
                    for item in datos_distribucion:
                        item['egresos'] = id_gasto
                    
                    # registros_coincidentes = [registro for registro in datos_distribucion if registro in registros_existentes_dict]
                    registros_no_enviados = [registro for registro in registros_existentes_dict if registro not in datos_distribucion]
                    registros_nuevos = [registro for registro in datos_distribucion if registro not in registros_existentes_dict]
                    

                    if len(registros_no_enviados) >0 or len(registros_nuevos)>0:
                        
                        EgresosDistribucion.objects.filter(egresos_id=id_gasto).delete()
                        
                        serializer = EgresosDistribucionSerializers(data=datos_distribucion, many=True)
                        if serializer.is_valid():
                            serializer.save()
                            data=datos_resumen(id_user,anno,mes)
                            return Response(data,status= status.HTTP_200_OK)
                        else:
                            
                            return Response({'error':'Error en almacenado de medios pagos'},status= status.HTTP_400_BAD_REQUEST)

                    
                    return Response([],status= status.HTTP_200_OK)

                
            else:
                
                return Response({'message':egreso_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error':data_errores},status= status.HTTP_400_BAD_REQUEST)

        # return Response([],status= status.HTTP_200_OK)

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
    

@api_view(['POST'])
def registromovimientobeneficio(request):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        data_list = []
              
        id_beneficion=int(request.data['codbeneficio'])
        
        datasave={
            "id":request.data['codbeneficio'],
            "entidad":  request.data['entidad'],
            "monto": request.data['monto'],
            "user": id_user,
            "fecha_beneficio": request.data['fecha'],
            "anotacion": request.data['anotacion'],
            "fecha_registro": datetime.now()
            
        }
        data_errores=''
        
        

        if validaciones_registros(request.data,'fecha_operacion'):
            fecha_obj = datetime.strptime(datasave['fecha_beneficio'], '%Y-%m-%d')
            anno=fecha_obj.year
            mes=fecha_obj.month
        else: 
            mensaje='Seleccione una fecha'
            data_errores = data_errores + mensaje if len(data_errores) == 0 else data_errores + '; ' + mensaje
        
        
            
        if validaciones_registros(datasave['monto'],'monto')==False:
            mensaje='El monto no puede ser menor a 1'
            data_errores = data_errores + mensaje if len(data_errores) == 0 else data_errores + '; ' + mensaje


        if validaciones_registros(request.data['entidad'],'entidad')==False:
            mensaje='Seleccione la entidad'
            data_errores = data_errores + mensaje if len(data_errores) == 0 else data_errores + '; ' + mensaje

        
        if len(data_errores)==0:
            data_list.append(datasave)
            if id_beneficion>0:
                condicion1 = Q(id__exact=id_beneficion)
                dato_existente=MovimientosBeneficios.objects.filter(condicion1 )
                

                if dato_existente:
                    
                    existente=MovimientosBeneficios.objects.get(condicion1)
                    
                    movimiento_serializer=MovimientosBeneficiosSerializers(existente,data=datasave)

                else:
                    return Response({'message':'El registro a actualizar no existe'},status= status.HTTP_400_BAD_REQUEST)
                

            else:

                movimiento_serializer=MovimientosBeneficiosSerializers(data=datasave)


            if movimiento_serializer.is_valid():
                movimiento_serializer.save()
                
                return Response(movimiento_serializer.data,status= status.HTTP_200_OK)
            


            return Response({'message':movimiento_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error':data_errores},status= status.HTTP_400_BAD_REQUEST)
    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)
    
@api_view(['POST'])
def eliminarmovimientobeneficio(request):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
         
     
        anno=datetime.now().year
        mes=datetime.now().month
        movimientodel=request.data['movimientos']

        if type(movimientodel)==str:
            movimientodel=ast.literal_eval(movimientodel)

        if len(movimientodel)>0:
            for item in movimientodel:
                condicion1 = Q(id__exact=item)
                lista=MovimientosBeneficios.objects.filter(condicion1).values()
                if lista:
                    
                    movimiento = MovimientosBeneficios.objects.get(pk=item)
                    movimiento.delete()


            
            return Response({'message':'OK'},status= status.HTTP_200_OK)
            
        else:
            return Response({'message':'No hay registros que eliminar'},status= status.HTTP_200_OK)
    else:
         return Response(resp,status= status.HTTP_403_FORBIDDEN)
    

@api_view(['POST'])
def estadisticas_mes(request,anno,mes):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        datos_imagenes=imagenes_mes(id_user,anno,mes)
        if datos_imagenes:
            return Response(datos_imagenes,status= status.HTTP_200_OK)
        
        else:
            return Response({[]},status= status.HTTP_200_OK)
        
    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)
    

@api_view(['POST'])
def estadisticas_mes_saldo(request,anno,mes):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        datos_imagenes=movile_imagenes_mes_saldo(id_user,anno,mes)
        if datos_imagenes:
            return Response(datos_imagenes,status= status.HTTP_200_OK)
        
        else:
            return Response({[]},status= status.HTTP_200_OK)
        
    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)
    
@api_view(['POST'])
def estadisticas_mes_ingreso(request,anno,mes):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        datos_imagenes=movile_imagenes_mes_ingreso(id_user,anno,mes)
        if datos_imagenes:
            return Response(datos_imagenes,status= status.HTTP_200_OK)
        
        else:
            return Response({[]},status= status.HTTP_200_OK)
        
    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)

@api_view(['POST'])
def estadisticas_mes_egreso(request,anno,mes):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        datos_imagenes=movile_imagenes_mes_egreso(id_user,anno,mes)
        if datos_imagenes:
            return Response(datos_imagenes,status= status.HTTP_200_OK)
        
        else:
            return Response({[]},status= status.HTTP_200_OK)
        
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
        
    if tipo=='entidad':
        consultagasto=EntidadesBeneficios.objects.filter(id__exact=valor).values()
        if not consultagasto:
            return False
        else:
            return True
        
@api_view(['POST'])
def CargarDistribucionEgresos(request):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        lista_egresos = Egresos.objects.order_by('id').values()
        
        for elemento in lista_egresos:
            id_elemento = elemento['id']
            id_user = elemento['user_id']
            monto_gasto = elemento['monto_gasto']
            fecha_gasto = elemento['fecha_gasto']
            
            condicion1 = Q(user_id__exact=id_user)
            lista_medios = MedioPago.objects.filter(condicion1).order_by('nombre_medio').values()
            
            op_medio=lista_medios[0]['id']
            
            data_list = []
            datasave={
                
                "egresos": id_elemento,
                "mediopago":op_medio,
                "monto":monto_gasto,
                
                
            }
            data_list.append(datasave)
            
            serializer_distri=EgresosDistribucionSerializers(data=datasave)
            if serializer_distri.is_valid():
                serializer_distri.save()
            else:
                return Response({'error':serializer_distri.errors},status= status.HTTP_400_BAD_REQUEST)

        return Response([],status= status.HTTP_200_OK)
        
    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)

        





