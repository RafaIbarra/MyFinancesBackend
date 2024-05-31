from rest_framework.response import Response
from rest_framework import status  
from rest_framework.decorators import api_view
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.models import User
from Conexion.Serializadores.GastosSerializers import *
from Conexion.Serializadores.ProductosFinancierosSerializers import *
from Conexion.Serializadores.MesesSerializers import *
from Conexion.Serializadores.CategoriasGastosSerializers import *
from Conexion.Serializadores.UsuariosSerializers import *
from Conexion.Serializadores.SolicitudPasswordSerializers import *
from Conexion.Serializadores.TiposGastosSerializers import *
from Conexion.Serializadores.TiposProductosFinancierosSerializers import *
from Conexion.Serializadores.MedioPagoSerializers import *
from Conexion.Serializadores.EgresosDistribucionSerializers import *

from Conexion.models import Gastos,ProductosFinancieros,CategoriaGastos,Usuarios,SolicitudPassword
from Conexion.models import TiposGastos,TiposProductosFinancieros,Meses,MedioPago,EgresosDistribucion
from Conexion.Seguridad.obtener_datos_token import obtener_datos_token
from Conexion.Seguridad.validaciones import validacionpeticion
from Conexion.Apis.api_generacion_datos import *
import time
import ast
from django.utils import timezone
from datetime import  timedelta
import random
import pytz

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@api_view(['POST'])
def registrotipogasto(request):

    data_list = []
    data_errores=''
    id=request.data['id']
    datasave={
        "id":  request.data['id'],
        "nombre_tipo_gasto":  request.data['nombre'],
        "fecha_registro": datetime.now()
        }
    data_list.append(datasave)
    
    if len(datasave['nombre_tipo_gasto']) < 1:
        mensaje='Ingrese el nombre para el concepto del gasto'
        data_errores = data_errores + mensaje if len(data_errores) == 0 else data_errores + '; ' + mensaje

    if len(data_errores)==0:
        if int(id)>0:
            condicion1 = Q(id__exact=id)
            dato_existente=TiposGastos.objects.filter(condicion1 )
            if dato_existente:
                
                existente=TiposGastos.objects.get(condicion1)
                
                tipo_gasto_serializer=TiposGastosSerializers(existente,data=datasave)

            else:
                return Response({'message':'El registro a actualizar no existe'},status= status.HTTP_400_BAD_REQUEST)
        
        else:
            tipo_gasto_serializer=TiposGastosSerializers(data=datasave)

        if tipo_gasto_serializer.is_valid():
            tipo_gasto_serializer.save()
            
            return Response(tipo_gasto_serializer.data,status= status.HTTP_200_OK)

        return Response({'message':tipo_gasto_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
    else:
        
        return Response({'error':data_errores},status= status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def obtenertipogasto(request):

    
    condicion1 = Q(id__gt=0)
        
    lista_categorias = TiposGastos.objects.filter(condicion1)
    
    if lista_categorias:
        
        result_categoria_serializer=TiposGastosSerializers(lista_categorias,many=True)

        if result_categoria_serializer.data:
                return Response(result_categoria_serializer.data,
                            status= status.HTTP_200_OK)
        else:

            return Response({'message':result_categoria_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
            
    else:
        return Response({'mensaje dato vacio':'sin datos'},status= status.HTTP_200_OK)
    
@api_view(['POST'])
def registrotipoproduto(request):

    data_list = []
    data_errores=''
    id=request.data['id']
    datasave={
        "id":  request.data['id'],
        "nombre_tipo_producto":  request.data['nombre'],
        "fecha_registro": datetime.now()
        
    }
    data_list.append(datasave)
    
    if len(datasave['nombre_tipo_producto']) < 1:
        mensaje='Ingrese el nombre para el concepto del gasto'
        data_errores = data_errores + mensaje if len(data_errores) == 0 else data_errores + '; ' + mensaje

    if len(data_errores)==0:
        if int(id)>0:
            condicion1 = Q(id__exact=id)
            dato_existente=TiposProductosFinancieros.objects.filter(condicion1 )
            if dato_existente:
                
                existente=TiposProductosFinancieros.objects.get(condicion1)
                
                tipo_producto_serializer=TiposProductosFinancierosSerializers(existente,data=datasave)

            else:
                return Response({'message':'El registro a actualizar no existe'},status= status.HTTP_400_BAD_REQUEST)
        
        else:
            tipo_producto_serializer=TiposProductosFinancierosSerializers(data=datasave)

        if tipo_producto_serializer.is_valid():
            tipo_producto_serializer.save()
            
            return Response(tipo_producto_serializer.data,status= status.HTTP_200_OK)

        return Response({'message':tipo_producto_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
    else:
        
        return Response({'error':data_errores},status= status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def obtenertipoproducto(request):

    
    condicion1 = Q(id__gt=0)
        
    lista_categorias = TiposProductosFinancieros.objects.filter(condicion1)
    
    if lista_categorias:
        
        result_categoria_serializer=TiposProductosFinancierosSerializers(lista_categorias,many=True)

        if result_categoria_serializer.data:
                return Response(result_categoria_serializer.data,
                            status= status.HTTP_200_OK)
        else:

            return Response({'message':result_categoria_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
            
    else:
        return Response({'mensaje dato vacio':'sin datos'},status= status.HTTP_200_OK)
    

@api_view(['POST'])
def registromeses(request):

    data_list = []
    data_errores=''
    n=1
    while n < 13:
        if n==1: nombremes='Enero'
        if n==2: nombremes='Febrero'
        if n==3: nombremes='Marzo'
        if n==4: nombremes='Abril'
        if n==5: nombremes='Mayo'
        if n==6: nombremes='Junio'
        if n==7: nombremes= 'Julio'
        if n==8: nombremes='Agosto'
        if n==9: nombremes='Septiembre'
        if n==10: nombremes='Octubre'
        if n==11: nombremes='Noviembre'
        if n==12: nombremes='Diciembre'

        datasave={
            "id":  0,
            "numero_mes": n,
            "nombre_mes":nombremes,
            "fecha_registro": datetime.now()
            
        }
        data_list.append(datasave)
        
        meses_serializer=MesesSerializers(data=datasave)
        n=n+1
        if meses_serializer.is_valid():
            meses_serializer.save()
        else:
            return Response({'error':meses_serializer.errors},status= status.HTTP_400_BAD_REQUEST)

        
                

####################################################################################################################################
@api_view(['POST'])
def registrogasto(request):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        data_list = []
        data_errores=''
        try:
            id_gasto=request.data['codigogasto']
            datasave={
                "id":  request.data['codigogasto'],
                "tipogasto":  request.data['tipogasto'],
                "categoria": request.data['categoria'],
                "user": id_user,
                "nombre_gasto": request.data['nombre'],
                "fecha_registro": datetime.now()
                
            }
            data_list.append(datasave)
            consultatipogasto=TiposGastos.objects.filter(id__exact=request.data['tipogasto']).values()
            if not consultatipogasto:
                mensaje='Selecione el tipo de gasto'
                data_errores = data_errores + mensaje if len(data_errores) == 0 else data_errores + '; ' + mensaje


            consultacategoria=CategoriaGastos.objects.filter(id__exact=request.data['categoria']).values()
            if not consultacategoria:
                mensaje='Selecione La categoria'
                data_errores = data_errores + mensaje if len(data_errores) == 0 else data_errores + '; ' + mensaje

            if len(datasave['nombre_gasto']) < 1:
                mensaje='Ingrese el nombre para el concepto del gasto'
                data_errores = data_errores + mensaje if len(data_errores) == 0 else data_errores + '; ' + mensaje


            existeregistro=False
            condicion1 = Q(user_id__exact=id_user)
            consulta_gastos= list(Gastos.objects.filter(condicion1).values())
            
            for item in consulta_gastos:
                if item['nombre_gasto'].replace(' ','').lower()==datasave['nombre_gasto'].replace(' ','').lower() and item['id'] != id_gasto:
                    existeregistro=True

            if existeregistro:
                mensaje='Ya se registro un concepto de gasto con este nombre'
                data_errores = data_errores + mensaje if len(data_errores) == 0 else data_errores + '; ' + mensaje

            if len(data_errores)==0:
                if id_gasto>0:
                    condicion1 = Q(id__exact=id_gasto)
                    dato_existente=Gastos.objects.filter(condicion1 )
                    if dato_existente:
                        
                        existente=Gastos.objects.get(condicion1)
                        
                        gasto_serializer=GastosSerializers(existente,data=datasave)

                    else:
                        return Response({'message':'El registro a actualizar no existe'},status= status.HTTP_400_BAD_REQUEST)
                
                else:
                    gasto_serializer=GastosSerializers(data=datasave)

                if gasto_serializer.is_valid():
                    gasto_serializer.save()
                    condicion1 = Q(user_id__exact=id_user)
                    lista = Gastos.objects.filter(condicion1).order_by('categoria', 'nombre_gasto')
                    result_serializer=GastosSerializers(lista,many=True)
                    return Response(result_serializer.data,status= status.HTTP_200_OK)

                return Response({'message':gasto_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
            else:
                
                return Response({'error':data_errores},status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
                return Response({'error': {str(e)}},status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)
    

@api_view(['POST'])
def eliminargastos(request):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        gatosdel=request.data['gastos']
        if type(gatosdel)==str:
            gatosdel=ast.literal_eval(gatosdel)

        if len(gatosdel):
            for item in gatosdel:
                condicion1 = Q(id__exact=item)
                lista=Gastos.objects.filter(condicion1).values()

                if lista:
                                    
                    gasto = Gastos.objects.get(pk=item)
                    gasto.delete()

            condicion1 = Q(user_id__exact=id_user)
            lista_gastos=Gastos.objects.filter(condicion1)
            result_serializer=GastosSerializers(lista_gastos,many=True)
            return Response(result_serializer.data,status= status.HTTP_200_OK)
        else:
            return Response({'message':'No hay registros que eliminar'},status= status.HTTP_200_OK)
             

        

    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def registroproductofinanciero(request):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        data_list = []
        id_producto=request.data['codigoproducto']
        data_errores=''
        datasave={
            "id":  request.data['codigoproducto'],
            "tipoproducto":  request.data['tipoproducto'],
            "user": id_user,
            "nombre_producto": request.data['nombre'],
            "fecha_registro": datetime.now()
            
        }
        
        data_list.append(datasave)
        consultatipogasto=TiposProductosFinancieros.objects.filter(id__exact=request.data['tipoproducto']).values()
        if not consultatipogasto:
            mensaje='Selecione el tipo ingreso'
            data_errores = data_errores + mensaje if len(data_errores) == 0 else data_errores + '; ' + mensaje


        if len(datasave['nombre_producto']) < 1:
            mensaje='Ingrese el nombre para el concepto del ingreso'
            data_errores = data_errores + mensaje if len(data_errores) == 0 else data_errores + '; ' + mensaje


        existeregistro=False
        condicion1 = Q(user_id__exact=id_user)
        consulta_gastos= list(ProductosFinancieros.objects.filter(condicion1).values())

        for item in consulta_gastos:
            if item['nombre_producto'].replace(' ','').lower()==datasave['nombre_producto'].replace(' ','').lower():
                existeregistro=True

        if existeregistro:
            mensaje='Ya se registro un concepto de ingreso con este nombre'
            data_errores = data_errores + mensaje if len(data_errores) == 0 else data_errores + '; ' + mensaje
        if len(data_errores)==0:
            if id_producto >0:
                condicion1 = Q(id__exact=id_producto)
                dato_existente=ProductosFinancieros.objects.filter(condicion1 )
                if dato_existente:
                    
                    existente=ProductosFinancieros.objects.get(condicion1)
                    
                    producto_serializer=ProductosFinancierosSerializers(existente,data=datasave)

                else:
                    return Response({'message':'El registro a actualizar no existe'},status= status.HTTP_400_BAD_REQUEST)
            else:
                
                producto_serializer=ProductosFinancierosSerializers(data=datasave)

                

            if producto_serializer.is_valid():
                
                producto_serializer.save()
                condicion1 = Q(user_id__exact=id_user)
                lista=ProductosFinancieros.objects.filter(condicion1)
                result_serializer=ProductosFinancierosSerializers(lista,many=True)
                return Response(result_serializer.data,status= status.HTTP_200_OK)
            
            else:
                
                return Response({'message':producto_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
        else:
            
            return Response({'error':data_errores},status= status.HTTP_400_BAD_REQUEST)
    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)
    

@api_view(['POST'])
def eliminarproductos(request):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        productosdel=request.data['productos']
        if type(productosdel)==str:
            productosdel=ast.literal_eval(productosdel)

        if len(productosdel):
            for item in productosdel:
                condicion1 = Q(id__exact=item)
                lista=ProductosFinancieros.objects.filter(condicion1).values()

                if lista:
                                    
                    producto = ProductosFinancieros.objects.get(pk=item)
                    producto.delete()

            condicion1 = Q(user_id__exact=id_user)
            lista_prod=ProductosFinancieros.objects.filter(condicion1)
            result_serializer=ProductosFinancierosSerializers(lista_prod,many=True)
            return Response(result_serializer.data,status= status.HTTP_200_OK)
        else:
            return Response({'message':'No hay registros que eliminar'},status= status.HTTP_200_OK)
             

        

    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)
    


@api_view(['POST'])
def registrocategoria(request):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        try:
            data_list = []
            data_errores=''
            id_categoria=request.data['codigocategoria']
            

                
            datasave={
                "id":  request.data['codigocategoria'],
                "user": id_user,
                "nombre_categoria": request.data['nombre'],
                "fecha_registro": datetime.now()
                
            }
            data_list.append(datasave)
            

            if len(datasave['nombre_categoria']) < 1:
                mensaje='Ingrese el nombre para el concepto de la categoria'
                data_errores = data_errores + mensaje if len(data_errores) == 0 else data_errores + '; ' + mensaje


            existeregistro=False
            condicion1 = Q(user_id__exact=id_user)
            consulta_gastos= list(CategoriaGastos.objects.filter(condicion1).values())
            
            for item in consulta_gastos:
                if item['nombre_categoria'].replace(' ','').lower()==datasave['nombre_categoria'].replace(' ','').lower() and item['id'] != id_categoria:
                    existeregistro=True

            if existeregistro:
                mensaje='Ya se registro una categoria de gasto con este nombre'
                data_errores = data_errores + mensaje if len(data_errores) == 0 else data_errores + '; ' + mensaje

            if len(data_errores)==0:
                if id_categoria>0:
                    condicion1 = Q(id__exact=id_categoria)
                    dato_existente=CategoriaGastos.objects.filter(condicion1 )
                    if dato_existente:
                        
                        existente=CategoriaGastos.objects.get(condicion1)
                        
                        categoria_serializer=CategoriaGastosSerializers(existente,data=datasave)

                    else:
                        return Response({'message':'El registro a actualizar no existe'},status= status.HTTP_400_BAD_REQUEST)
                
                else:
                    categoria_serializer=CategoriaGastosSerializers(data=datasave)

                if categoria_serializer.is_valid():
                    categoria_serializer.save()
                    condicion1 = Q(user_id__exact=id_user)
                    lista = CategoriaGastos.objects.filter(condicion1).order_by( 'nombre_categoria')
                    result_serializer=CategoriaGastosSerializers(lista,many=True)
                    return Response(result_serializer.data,status= status.HTTP_200_OK)

                return Response({'message':categoria_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
            else:
                
                return Response({'error':data_errores},status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
                return Response({'error':  {str(e)}},status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)
    

@api_view(['POST'])
def eliminarcategorias(request):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        categoriadel=request.data['categorias']
        if type(categoriadel)==str:
            categoriadel=ast.literal_eval(categoriadel)

        if len(categoriadel):
            for item in categoriadel:
                condicion1 = Q(id__exact=item)
                lista=CategoriaGastos.objects.filter(condicion1).values()

                if lista:
                                    
                    gasto = CategoriaGastos.objects.get(pk=item)
                    gasto.delete()

            condicion1 = Q(user_id__exact=id_user)
            lista_gastos=CategoriaGastos.objects.filter(condicion1)
            result_serializer=CategoriaGastosSerializers(lista_gastos,many=True)
            return Response(result_serializer.data,status= status.HTTP_200_OK)
        else:
            return Response({'message':'No hay registros que eliminar'},status= status.HTTP_200_OK)
             

        

    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)
    

@api_view(['POST'])
def registromediopago(request):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        try:
            data_list = []
            data_errores=''
            id_medio_pago=int(request.data['codigomediopago'])
            
            
                
            datasave={
                "id":  request.data['codigomediopago'],
                "nombre_medio": request.data['nombre'],
                "anotacion": request.data['anotacion'],
                "estado":request.data['estado'],
                "user": id_user,
                "fecha_registro": datetime.now()
                
            }
            data_list.append(datasave)
            

            if len(datasave['nombre_medio']) < 1:
                mensaje='Ingrese el nombre para el medio de pago'
                data_errores = data_errores + mensaje if len(data_errores) == 0 else data_errores + '; ' + mensaje


            existeregistro=False
            condicion1 = Q(user_id__exact=id_user)
            consulta_medio= list(MedioPago.objects.filter(condicion1).values())
            
            for item in consulta_medio:
                if item['nombre_medio'].replace(' ','').lower()==datasave['nombre_medio'].replace(' ','').lower() and item['id'] != id_medio_pago:
                    existeregistro=True

            if existeregistro:
                mensaje='Ya se registro un medio de pago con este nombre'
                data_errores = data_errores + mensaje if len(data_errores) == 0 else data_errores + '; ' + mensaje

            if len(data_errores)==0:
                if id_medio_pago>0:
                    condicion1 = Q(id__exact=id_medio_pago)
                    dato_existente=MedioPago.objects.filter(condicion1 )
                    if dato_existente:
                        
                        existente=MedioPago.objects.get(condicion1)
                        
                        medio_serializer=MedioPagoSerializers(existente,data=datasave)

                    else:
                        return Response({'message':'El registro a actualizar no existe'},status= status.HTTP_400_BAD_REQUEST)
                
                else:
                    medio_serializer=MedioPagoSerializers(data=datasave)

                if medio_serializer.is_valid():
                    medio_serializer.save()
                    condicion1 = Q(user_id__exact=id_user)
                    lista = MedioPago.objects.filter(condicion1).order_by( 'nombre_medio')
                    result_serializer=MedioPagoSerializers(lista,many=True)
                    return Response(result_serializer.data,status= status.HTTP_200_OK)

                return Response({'message':medio_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
            else:
                
                return Response({'error':data_errores},status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
                return Response({'error':  {str(e)}},status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)
    

@api_view(['POST'])
def eliminarmediospagos(request):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        mediodel=request.data['medios']
        if type(mediodel)==str:
            mediodel=ast.literal_eval(mediodel)

        if len(mediodel):
            for item in mediodel:
                condicion1 = Q(id__exact=item)
                lista=MedioPago.objects.filter(condicion1).values()

                if lista:
                    pagosreg=EgresosDistribucion.objects.filter(mediopago_id__exact=item).values()
                    if pagosreg:
                        return Response({'error':'Se registraron gastos con este medio, no puede ser eliminado'},status= status.HTTP_400_BAD_REQUEST)
                    else:

                        gasto = MedioPago.objects.get(pk=item)
                        gasto.delete()

            condicion1 = Q(user_id__exact=id_user)
            lista_medios=MedioPago.objects.filter(condicion1)
            result_serializer=MedioPagoSerializers(lista_medios,many=True)
            return Response(result_serializer.data,status= status.HTTP_200_OK)
        else:
            return Response({'message':'No hay registros que eliminar'},status= status.HTTP_200_OK)
    


@api_view(['POST'])
def obtenerdatosusuario(request):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        

        condicion1 = Q(id__exact=id_user)
        datos_usuario=Usuarios.objects.filter(condicion1)
        result_serializer=UsuariosSerializer(datos_usuario,many=True)
        return Response(result_serializer.data,status= status.HTTP_200_OK)
        
    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def actualizardatosusuario(request):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        condicion1 = Q(id__exact=id_user)
        datos_usuario=list(Usuarios.objects.filter(condicion1).values())
        user=datos_usuario[0]['user_name']
        ultconex=datos_usuario[0]['ultima_conexion']
        fechareg=datos_usuario[0]['fecha_registro']
        datasave={
            "id":  id_user,
            "nombre_usuario":  request.data['nombre'],
            "apellido_usuario": request.data['apellido'],
            "fecha_nacimiento": request.data['fechanacimiento'],
            "correo": request.data['correo'],
            "user_name":user,
            "ultima_conexion":ultconex,
            "fecha_registro":fechareg,
        
        }
        
        
        existente=Usuarios.objects.get(condicion1)
        
        usuario_serializer=UsuariosSerializer(existente,data=datasave)
        if usuario_serializer.is_valid():
            usuario_serializer.save()
            consultausuarios=Usuarios.objects.filter(user_name__exact=user).values()
            fechareg=str(consultausuarios[0]['fecha_registro'])
            fecha_obj = datetime.fromisoformat(fechareg)
            fecha_formateada = fecha_obj.strftime("%d/%m/%Y %H:%M:%S")
            datauser=[{
                'username':consultausuarios[0]['user_name'].capitalize(),
                'nombre':consultausuarios[0]['nombre_usuario'],
                'apellido':consultausuarios[0]['apellido_usuario'],
                'fecha_registro':fecha_formateada,
                
            }

            ]
            return Response({'datauser':datauser},status= status.HTTP_200_OK)

        return Response({'message':usuario_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
        
    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)
    
@api_view(['POST'])
def enviocorreocontraseña(request):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        condicion1 = Q(id__exact=id_user)
        datos_usuario=list(Usuarios.objects.filter(condicion1).values())
        user=datos_usuario[0]['user_name']
        nombre_user=datos_usuario[0]['nombre_usuario']
        apellido_user=datos_usuario[0]['apellido_usuario']
        correo_user=datos_usuario[0]['correo']
        codigo=random.randint(100000, 999999)
        fecha_reg=datetime.now()
        fecha_venc=datetime.now() + timedelta(minutes=60)
        datasave={
            
            "user": id_user,
            "codigo_recuperacion": codigo,
            "fecha_creacion": fecha_reg,
            "fecha_vencimiento": fecha_venc,
            
        }
        
        solicitud_serializer=SolicitudPasswordSerializers(data=datasave)
        if solicitud_serializer.is_valid():
            solicitud_serializer.save()
            Nombre=nombre_user + '; ' +apellido_user
            user_name=user
            fecha=fecha_reg.strftime("%d/%m/%Y %H:%M:%S")
            fecha_validez=fecha_venc.strftime("%d/%m/%Y %H:%M:%S")
            html_content = render_to_string('correo.html', {'Nombre': Nombre, 'user_name': user_name, 'fecha_validez':fecha_validez,'codigo':codigo})
            text_content = strip_tags(html_content)
            subject = 'Cambio de Contraseña'
            from_email = 'myfinancesweb@gmail.com'
            to_email = correo_user
            

            email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
            email.attach_alternative(html_content, 'text/html')  # Adjuntar el contenido HTML
            # return Response({'mensaje': 'Correo enviado a ' + correo_user},status=status.HTTP_200_OK)
            try:
                email.send()
                return Response({'mensaje': 'Correo enviado a ' + correo_user},status=status.HTTP_200_OK)
                # return Response({'error': f'Error al enviar el correo: {str(e)}'},status=status.HTTP_400_BAD_REQUEST)
            
            except Exception as e:
                return Response({'error': f'Error al enviar el correo: {str(e)}'},status=status.HTTP_400_BAD_REQUEST)
        

        return Response({'message':solicitud_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
        
    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def comprobarcodigo(request):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        codigo_respuesta=request.data['codigo']
        result=resultado_codigo(id_user,codigo_respuesta)
        if result=='OK':
            return Response({'mensaje': 'OK' },status=status.HTTP_200_OK)
        else:
            return Response({'error':result},status= status.HTTP_400_BAD_REQUEST)
    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)

@api_view(['POST'])
def actualizarpassword(request):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        passwor1=request.data['password']
        passwor2=request.data['password2']
        codigo_respuesta=request.data['codigo']

        result=resultado_codigo(id_user,codigo_respuesta)
        if result=='OK':
            if passwor1==passwor2:
                try:
                    usuario=User.objects.get(username=usuario)
                    usuario.set_password(passwor1)
                    usuario.save()

                    condicion1 = Q(codigo_recuperacion__exact=codigo_respuesta)
                    condicion2= Q(user_id__exact=id_user)
                    datos_solicitud=list(SolicitudPassword.objects.filter(condicion1 & condicion2).values())

                    datasave={
                        "id":  datos_solicitud[0]['id'],
                        "user":  id_user,
                        "codigo_recuperacion": datos_solicitud[0]['codigo_recuperacion'],
                        "fecha_creacion": datos_solicitud[0]['fecha_creacion'],
                        "fecha_vencimiento": datos_solicitud[0]['fecha_vencimiento'],
                        "fecha_procesamiento":datetime.now()
                    }
        
                    condicion=Q(id__exact=datos_solicitud[0]['id'])
                    existente=SolicitudPassword.objects.get(condicion)
                    
                    sol_serializer=SolicitudPasswordSerializers(existente,data=datasave)
                    if sol_serializer.is_valid():
                        sol_serializer.save()
                        return Response({'mensaje': 'Contraseña Actualizada' },status=status.HTTP_200_OK)
                    else:
                        return Response({'error':sol_serializer.errors},status=status.HTTP_400_BAD_REQUEST)    

                except Exception as e:
                    error=str(e)
                    return Response({'error':error},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Las contraseñas no coinciden' },status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error':result},status= status.HTTP_400_BAD_REQUEST)
    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)

def resultado_codigo(id_user,codigo):
    condicion1 = Q(codigo_recuperacion__exact=codigo)
    condicion2= Q(user_id__exact=id_user)
    datos_solicitud=list(SolicitudPassword.objects.filter(condicion1 & condicion2).values())
    
    if len(datos_solicitud) >0:
        fecha_actual = datetime.now()
        
        fecha_vencimiento = datos_solicitud[0]['fecha_vencimiento']
        zona_horaria_correcta = pytz.timezone("America/Asuncion")  # Zona horaria correcta
        fecha_vencimiento = fecha_vencimiento.astimezone(zona_horaria_correcta)

        fecha_actual = fecha_actual.replace(tzinfo=fecha_vencimiento.tzinfo)
        
        fecha_procesamiento=datos_solicitud[0]['fecha_procesamiento']
        errores=''
        if fecha_procesamiento != None:
            errores=errores + 'El codigo ya fue utilizado'

        if fecha_actual> fecha_vencimiento:
            errores=errores + '. El codigo de seguridad ya vencio'
        
        if len(errores) ==0:
            
            return 'OK'
        else:
            return errores
    else:
        return 'El codigo no le pertence al usuario'
    


######################################### Listados ####################################
    

@api_view(['POST'])
def misingresos(request,anno,mes):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        lista_ingresos=datos_ingresos(id_user,anno,mes)
        if lista_ingresos:
          
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
def miscategorias(request,id):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        condicion1 = Q(user_id__exact=id_user)
        if id >0:
            condicion2 = Q(id__exact=id)
            lista_categorias = CategoriaGastos.objects.filter(condicion1 & condicion2).order_by('nombre_categoria')
        else:

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
def mismediospagos(request,id):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        condicion1 = Q(user_id__exact=id_user)
        if id >0:
            condicion2 = Q(id__exact=id)
            lista_medios= MedioPago.objects.filter(condicion1 & condicion2).order_by('nombre_medio')
        else:

            lista_medios = MedioPago.objects.filter(condicion1).order_by('nombre_medio')
        
        if lista_medios:
            
            result_medio_serializer=MedioPagoSerializers(lista_medios,many=True)

            if result_medio_serializer.data:
                 return Response(result_medio_serializer.data,
                                status= status.HTTP_200_OK)
            else:

                return Response({'message':result_medio_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
                
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
      
        lista = Gastos.objects.filter(condicion1).order_by('categoria', 'nombre_gasto')
        lista_Gastos = CategoriaGastos.objects.filter(condicion1).order_by('nombre_categoria')
        condicion2 = Q(estado__exact=1)
        lista_medios=MedioPago.objects.filter(condicion1 & condicion2 ).order_by('nombre_medio')

        datos_gastos=[]
        datos_categoria=[]
        datos_medios=[]

        datos_errores=[]
        if lista and lista_Gastos and lista_medios:
            result_gastos_serializer=GastosSerializers(lista,many=True)
            result_categoria_serializer=CategoriaGastosSerializers(lista_Gastos,many=True)
            result_medios_serializer=MedioPagoSerializers(lista_medios,many=True)

            if result_gastos_serializer.data:
                 datos_gastos.append(result_gastos_serializer.data)
            else:
                 datos_errores.append({'error gasto':result_gastos_serializer.errors})
            
            if result_categoria_serializer.data:
                 datos_categoria.append(result_categoria_serializer.data)
            else:
                 datos_errores.append({'error categoria':result_categoria_serializer.errors})

            if result_medios_serializer.data:
                 datos_medios.append(result_medios_serializer.data)
            else:
                 
                 datos_errores.append({'error medio pago':result_medios_serializer.errors})
                 

            if result_gastos_serializer.data and result_categoria_serializer:
                return Response({
                     'datosgastos':result_gastos_serializer.data,
                     'datoscategorias':result_categoria_serializer.data,
                     'datosmedios':result_medios_serializer.data,
                     },
                                status= status.HTTP_200_OK)
            
            else:

                return Response({'message':datos_errores},status= status.HTTP_400_BAD_REQUEST)
                
        else:
            if lista_Gastos:
                result_categoria_serializer=CategoriaGastosSerializers(lista_Gastos,many=True)
                if result_categoria_serializer.data:
                    datos_categoria.append(result_categoria_serializer.data)
                else:
                    
                    datos_errores.append({'error categoria':result_categoria_serializer.errors})


                if  result_categoria_serializer:
                    return Response({
                       
                        'datoscategorias':result_categoria_serializer.data},status= status.HTTP_200_OK)
                    
            else:
                return Response([],status= status.HTTP_200_OK)
    else:
            return Response(resp,status= status.HTTP_403_FORBIDDEN)
    
@api_view(['POST'])
def misgastos(request,id):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:           
        condicion1 = Q(user_id__exact=id_user)

        if id >0:
            condicion2 = Q(id__exact=id)
            lista = Gastos.objects.filter(condicion1 & condicion2).order_by('categoria', 'nombre_gasto')
            
        else:
   
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
def misproductosfinancieros(request,id):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:           
        condicion1 = Q(user_id__exact=id_user)
        if id > 0:
            condicion2 = Q(id__exact=id)
            lista=ProductosFinancieros.objects.filter(condicion1 & condicion2)
        else:
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
    
        
        datosresumen=datos_resumen(id_user,anno,mes)
        return Response(datosresumen, status=status.HTTP_200_OK)
        
        
    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)
    


@api_view(['POST'])
def balance(request,anno,mes):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True: 
        
        
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
    

####################################### Listados Movile ##################################
@api_view(['POST'])
def MovileMisIngresos(request,anno,mes):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        lista_ingresos=datos_ingresos(id_user,anno,mes)
        if lista_ingresos:
          
            # def custom_key(item):
            #     fecha_ingreso = item.get('fecha_ingreso', '')
            #     fecha_registro = item.get('fecha_registro', '')
            #     return (fecha_ingreso, fecha_registro)
             
            lista_ingresos = sorted(lista_ingresos,key=lambda x: x['id'], reverse=False)
            # agrupados=agrupar_periodos_ingresos(lista_ingresos)
            lista_meses = Meses.objects.order_by('numero_mes')
            result_meses_serializer=MesesSerializers(lista_meses,many=True)
            if result_meses_serializer.data:
             
                return Response(lista_ingresos,status= status.HTTP_200_OK)
        else:
            
            return Response([],status= status.HTTP_200_OK)    
        
    else:
            return Response(resp,status= status.HTTP_403_FORBIDDEN)
    
@api_view(['POST'])
def MovileDatoIngreso(request,anno,mes,id):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        lista_ingresos=datos_ingresos(id_user,anno,mes)
        if lista_ingresos:
          
            lista_egresos_unico = [elemento for elemento in lista_ingresos if elemento.get('id') == id]
            valor_retorno=lista_egresos_unico[0]
        
            return Response(valor_retorno,status= status.HTTP_200_OK)
        else:
            
            return Response([],status= status.HTTP_200_OK) 
        
    else:
            return Response(resp,status= status.HTTP_403_FORBIDDEN)
    
@api_view(['POST'])
def MovileMisEgresos(request,anno,mes):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        lista_egresos=datos_egresos(id_user,anno,mes)
        if lista_egresos:

            lista_egresos=sorted(lista_egresos, key=lambda x: x['id'], reverse=False)
            agrupados=agrupar_periodos_egresos(lista_egresos)
            lista_meses = Meses.objects.order_by('numero_mes')
            result_meses_serializer=MesesSerializers(lista_meses,many=True)
            if result_meses_serializer.data:
                
            
                return Response(lista_egresos,status= status.HTTP_200_OK)
        else:
            
            return Response([],status= status.HTTP_200_OK)
        
    else:
            return Response(resp,status= status.HTTP_403_FORBIDDEN)
    
@api_view(['POST'])
def MovileDatoEgreso(request,anno,mes,id):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        
        lista_egresos=datos_egresos(id_user,anno,mes)
        
        # lista_egresos_unico = [elemento for elemento in lista_egresos if elemento.get('id') == id]
        
        if lista_egresos:

            lista_egresos_unico = [elemento for elemento in lista_egresos if elemento.get('id') == id]
            valor_retorno=lista_egresos_unico[0]
        
            return Response(valor_retorno,status= status.HTTP_200_OK)
        else:
            return Response([],status= status.HTTP_200_OK)
        
    else:
            return Response(resp,status= status.HTTP_403_FORBIDDEN)
    



@api_view(['POST'])
def comprobarsesionusuario(request):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        
        consultausuarios=Usuarios.objects.filter(user_name__exact=usuario).values()
        fechareg=str(consultausuarios[0]['fecha_registro'])
        fecha_obj = datetime.fromisoformat(fechareg)
        fecha_formateada = fecha_obj.strftime("%d/%m/%Y %H:%M:%S")
        datauser=[{
                    'username':consultausuarios[0]['user_name'].capitalize(),
                    'nombre':consultausuarios[0]['nombre_usuario'],
                    'apellido':consultausuarios[0]['apellido_usuario'],
                    'fecha_registro':fecha_formateada,
                    
                }

                ]     
        return Response({'datauser':datauser},status= status.HTTP_200_OK)
    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)
    



@api_view(['POST'])
def MovileResumenMes(request,anno,mes):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        data_resumen=datos_resumen_movile(id_user,anno,mes)
        if data_resumen:

            # lista_egresos=sorted(lista_egresos, key=lambda x: x['id'], reverse=False)
            # agrupados=agrupar_periodos_egresos(lista_egresos)
            # lista_meses = Meses.objects.order_by('numero_mes')
            # result_meses_serializer=MesesSerializers(lista_meses,many=True)
            # if result_meses_serializer.data:
                
            
            return Response(data_resumen,status= status.HTTP_200_OK)
        
    else:
            return Response(resp,status= status.HTTP_403_FORBIDDEN)
    
@api_view(['POST'])
def MovileSaldos(request,anno):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        data_saldos=datos_saldos_periodos(id_user,anno)
        if data_saldos:            
            return Response(data_saldos,status= status.HTTP_200_OK)
        else:
            return Response([],status= status.HTTP_200_OK)
        
    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)
    

@api_view(['POST'])
def CargarMediosUsuarios(request):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        lista_usuarios = Usuarios.objects.order_by('id').values()
        
        for elemento in lista_usuarios:
            id_elemento = elemento['id']
            nombre = elemento['user_name']
            
            data_list = []
            datasave={
                "id":  0,
                "nombre_medio": 'Efectivo',
                "anotacion":'',
                "user":id_elemento,
                "fecha_registro": datetime.now()
                
            }
            data_list.append(datasave)
            
            medio_serializer=MedioPagoSerializers(data=datasave)
            if medio_serializer.is_valid():
                medio_serializer.save()
            else:
                return Response({'error':medio_serializer.errors},status= status.HTTP_400_BAD_REQUEST)

        return Response([],status= status.HTTP_200_OK)
        
    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)



    