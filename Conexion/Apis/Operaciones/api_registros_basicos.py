from rest_framework.response import Response
from rest_framework import status  
from rest_framework.decorators import api_view
from django.db.models import Q
# from Conexion.Serializers import GastosSerializers,ProductosFinancierosSerializers,MesesSerializers
from Conexion.Serializadores.GastosSerializers import *
from Conexion.Serializadores.ProductosFinancierosSerializers import *
from Conexion.Serializadores.MesesSerializers import *
from Conexion.models import Gastos,ProductosFinancieros,Meses
from Conexion.Seguridad.obtener_datos_token import obtener_datos_token
from Conexion.Seguridad.validaciones import validacionpeticion
import time
import ast
from django.utils import timezone
@api_view(['POST'])
def registrogasto(request):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        data_list = []
                    
        id_gasto=request.data['codigogasto']
        datasave={
            "id":  request.data['codigogasto'],
            "tipogasto":  request.data['tipogasto'],
            "categoria": request.data['categoria'],
            "user": id_user,
            "nombre_gasto": request.data['nombre'],
            "fecha_registro": timezone.now()
            
        }
        data_list.append(datasave)

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
        
        datasave={
            "id":  request.data['codigoproducto'],
            "tipoproducto":  request.data['tipoproducto'],
            "user": id_user,
            "nombre_producto": request.data['nombre'],
            "fecha_registro": timezone.now()
            
        }
        print(datasave)
        data_list.append(datasave)

        if id_producto >0:
            condicion1 = Q(id__exact=id_producto)
            dato_existente=ProductosFinancieros.objects.filter(condicion1 )
            if dato_existente:
                
                existente=ProductosFinancieros.objects.get(condicion1)
                
                producto_serializer=ProductosFinancierosSerializers(existente,data=datasave)

            else:
                return Response({'message':'El registro a actualizar no existe'},status= status.HTTP_400_BAD_REQUEST)
        else:
            print('guardara uno nuevo')
            producto_serializer=ProductosFinancierosSerializers(data=datasave)

            

        if producto_serializer.is_valid():
            print('es valido')
            producto_serializer.save()
            condicion1 = Q(user_id__exact=id_user)
            lista=ProductosFinancieros.objects.filter(condicion1)
            result_serializer=ProductosFinancierosSerializers(lista,many=True)
            return Response(result_serializer.data,status= status.HTTP_200_OK)
        
        else:
            print('No es valido')
            print(producto_serializer.errors)
            return Response({'message':producto_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
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





