from rest_framework.response import Response
from rest_framework import status  
from rest_framework.decorators import api_view
from django.db.models import Q

from Conexion.Seguridad.obtener_datos_token import obtener_datos_token
from Conexion.Seguridad.validaciones import validacionpeticion
from Conexion.models import Usuarios,SesionesActivas
from Conexion.Serializadores.UsuariosSerializers import *
from Conexion.Serializadores.SesionesActivasSerializers import *
@api_view(['POST'])
def seguimiento_usuarios(request):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:           
        condicion1 = Q(id__gt=0)
        lista=Usuarios.objects.filter(condicion1)
        
        if lista:
            result_serializer=UsuariosSerializer(lista,many=True)

            if result_serializer.data:
                return Response(result_serializer.data,status= status.HTTP_200_OK)

            return Response({'message':result_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response([],status= status.HTTP_200_OK)
    else:
            return Response(resp,status= status.HTTP_403_FORBIDDEN)
    

@api_view(['POST'])
def seguimiento_sesiones(request):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:           
        condicion1 = Q(id__gt=0)
        lista=SesionesActivas.objects.filter(condicion1)
        
        if lista:
            result_serializer=SesionesActivasSerializers(lista,many=True)

            if result_serializer.data:
                return Response(result_serializer.data,status= status.HTTP_200_OK)

            return Response({'message':result_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response([],status= status.HTTP_200_OK)
    else:
            return Response(resp,status= status.HTTP_403_FORBIDDEN)