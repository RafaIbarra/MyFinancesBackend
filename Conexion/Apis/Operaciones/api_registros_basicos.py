from rest_framework.response import Response
from rest_framework import status  
from rest_framework.decorators import api_view
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.models import User
# from Conexion.Serializers import GastosSerializers,ProductosFinancierosSerializers,MesesSerializers
from Conexion.Serializadores.GastosSerializers import *
from Conexion.Serializadores.ProductosFinancierosSerializers import *
from Conexion.Serializadores.MesesSerializers import *
from Conexion.Serializadores.CategoriasGastosSerializers import *
from Conexion.Serializadores.UsuariosSerializers import *
from Conexion.Serializadores.SolicitudPasswordSerializers import *
from Conexion.models import Gastos,ProductosFinancieros,CategoriaGastos,Usuarios,SolicitudPassword
from Conexion.Seguridad.obtener_datos_token import obtener_datos_token
from Conexion.Seguridad.validaciones import validacionpeticion
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
def registrogasto(request):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        data_list = []
        data_errores=''
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
    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)
    

@api_view(['POST'])
def eliminarcategorias(request):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        gatosdel=request.data['categorias']
        if type(gatosdel)==str:
            gatosdel=ast.literal_eval(gatosdel)

        if len(gatosdel):
            for item in gatosdel:
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
            
            return Response(usuario_serializer.data,status= status.HTTP_200_OK)
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
            return Response({'mensaje': 'Correo enviado a ' + correo_user},status=status.HTTP_200_OK)
            # try:
            #     email.send()
            #     return Response({'mensaje': 'Correo enviado a ' + correo_user},status=status.HTTP_200_OK)
            # except Exception as e:
            #     return Response({'mensaje': f'Error al enviar el correo: {str(e)}'},status=status.HTTP_400_BAD_REQUEST)
        

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
                return Response({'mensaje': 'Las contraseñas no coinciden' },status=status.HTTP_400_BAD_REQUEST)
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
    


