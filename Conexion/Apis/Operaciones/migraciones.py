from rest_framework.response import Response
from rest_framework import status  
from rest_framework.decorators import api_view
from django.db.models import Q
from django.contrib.auth.models import User
from Conexion.Serializadores.UsersSerializers import *
from Conexion.Seguridad.obtener_datos_token import obtener_datos_token
from Conexion.Seguridad.validaciones import validacionpeticion

@api_view(['POST'])
def migracionusers(request):

     token_sesion,usuario,id_user =obtener_datos_token(request)
     resp=validacionpeticion(token_sesion)
     if resp==True:           
        
        
        lista = User.objects.order_by('id')
        
                
        if lista:
            result_serializer=UsersSerializers(lista,many=True)

            if result_serializer.data:
                return Response(result_serializer.data,status= status.HTTP_200_OK)

            return Response({'message':result_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response([],status= status.HTTP_200_OK)
     else:
             return Response(resp,status= status.HTTP_403_FORBIDDEN)
