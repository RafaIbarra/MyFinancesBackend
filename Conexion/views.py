from datetime import  timedelta
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView


from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


from rest_framework.response import Response
from rest_framework.views import APIView

from django.core.mail import send_mail
from django.db.models import Q

from Conexion.Serializers import CustomTokenObtainPairSerializer,UsuariosSerializer,SesionesActivasSerializers,CustomUserSerializer
from Conexion.models import Usuarios,SesionesActivas
from MyFinancesBackend.settings import TIEMPO_SESION_HORAS
from Conexion.validaciones import resgistrosesion
import re


class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    

    def post(self, request, *args, **kwargs):
        user_name = request.data.get('username', '')
        
        password = request.data.get('password', '')
        registro_sesion=resgistrosesion(user_name)
        print(registro_sesion)
        if registro_sesion:
            
            SesionesActivas.objects.filter(user_name__exact=user_name).update(Estado=0)
            

        condicion1=Q(user_name__exact=user_name)  
        tokenusuario=SesionesActivas.objects.filter(condicion1).values()
        
        for item in tokenusuario:
            datotoken=(item['token_session'])
            condticiontoken=Q(key__exact=datotoken)
            existetoken=Token.objects.filter(condticiontoken).values()
            if existetoken:
                t=Token.objects.get(key=datotoken)
                t.delete()

        user = authenticate(username=user_name,password=password)
        print("el autenticate")
        print(user)
        if user:
            user_agent = request.META.get('HTTP_USER_AGENT', 'Desconocido')
            
            token,created=Token.objects.get_or_create(user=user)
            print('EL token: ', token)
            
            try:
                

                
                datasesion=({
                    'user_name':user_name,
                    'fecha_conexion':timezone.now(),
                    'expiracion_conexion':timezone.now() + timedelta(hours=TIEMPO_SESION_HORAS),
                    'token_session':token.key,
                    'dispositivo':user_agent,
                    
                    'Estado':1
                })
               
                sesion_serializers=SesionesActivasSerializers(data=datasesion)
                if sesion_serializers.is_valid():
                    
                    sesion_serializers.save()
                else:
                    print(sesion_serializers.errors)
                
                login_serializer = self.serializer_class(data=request.data)
                if login_serializer.is_valid():
                    
                    return Response({
                        'token': login_serializer.validated_data.get('access'),
                        'refresh': login_serializer.validated_data.get('refresh'),
                        'sesion':token.key,
                        
                        'message': 'Inicio de Sesion Existoso'
                    }, status=status.HTTP_200_OK)
                return Response({'error': 'Contraseña o nombre de usuario incorrectos'}, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                
                return Response({'message':e.args},status= status.HTTP_406_NOT_ACCEPTABLE)
                

        return Response({'error': 'Contraseña o nombre de usuario incorrectos'}, status=status.HTTP_400_BAD_REQUEST)
    
class Registro(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    

    def post(self, request, *args, **kwargs):
        nombre = request.data.get('nombre', '')
        apellido = request.data.get('apellido', '')
        nacimiento = request.data.get('nacimiento', '')
        user = request.data.get('user', '')
        correo = request.data.get('correo', '')
        password = request.data.get('password', '')
        password=password.replace(" ", "")
        user_reg=formato_user(user)
        try:
            data_user=(
                {
                    'nombre_usuario':nombre,
                    'apellido_usuario':apellido,
                    'fecha_nacimiento':nacimiento,
                    'user_name':user_reg,
                    'correo':correo,
                    'ultima_conexion':timezone.now(),
                    'fecha_registro':timezone.now()
                }
            )
            print(data_user)
            user_serializer=UsuariosSerializer(data=data_user)
            if user_serializer.is_valid():
                user_serializer.save()
                user_registrar = User.objects.create_user(user_reg, password=password)
                user_registrar.save()
                user_agent = request.META.get('HTTP_USER_AGENT', 'Desconocido')
                print('debe crear el token')
                
                # datos_usuario=User.objects.filter(username__exact=user_reg).values()
                # datos_usuario=list(datos_usuario)
                
                # id_user_reg=datos_usuario[0]['id']
                
                token,created=Token.objects.get_or_create(user=user_registrar)
                print('el token')
                print(token)
                datasesion=({
                    'user_name':user_reg,
                    'fecha_conexion':timezone.now(),
                    'expiracion_conexion':timezone.now() + timedelta(hours=TIEMPO_SESION_HORAS),
                    'token_session':token.key,
                    'dispositivo':user_agent,
                    'Estado':1
                })

                sesion_serializers=SesionesActivasSerializers(data=datasesion)
                if sesion_serializers.is_valid():
                    
                    sesion_serializers.save()
                else:
                    print(sesion_serializers.errors)
                
                datalogin={
                    'username':user_reg,
                    'password':password
                
                }
                print('datalogin')
                print(datalogin)
                login_serializer = self.serializer_class(data=datalogin)
                if login_serializer.is_valid():
                    
                    return Response({
                        'token': login_serializer.validated_data.get('access'),
                        'refresh': login_serializer.validated_data.get('refresh'),
                        'sesion':token.key,
                        
                        'message': 'Inicio de Sesion Existoso'
                    }, status=status.HTTP_200_OK)
                return Response({'error': 'Contraseña o nombre de usuario incorrectos'}, status=status.HTTP_400_BAD_REQUEST)
                

             
        except IntegrityError:
             return Response({'message':'Error de creacion'},status= status.HTTP_400_BAD_REQUEST)

class NotFoundView(APIView):
    """
    Tipo notificacion: 

    - Descripcion: Retorna error cuando se ingresa un endpoint que no existe
    
    
    """
    def get(self, request, *args, **kwargs):
        return Response({"message": "La ruta solicitada no se encuentra"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        return Response({"message": "La ruta solicitada no se encuentra"}, status=status.HTTP_404_NOT_FOUND)


def formato_user(data):
    
    data = data.replace(" ", "")
    
    # Poner en minúsculas
    data = data.lower()
    
    # Quitar caracteres especiales utilizando expresiones regulares
    data = re.sub(r'[^a-zA-Z0-9]', '', data)
    return data