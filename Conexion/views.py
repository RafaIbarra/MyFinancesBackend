from datetime import  timedelta
from datetime import datetime
from django.utils import timezone


from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError

from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.authtoken.models import Token


from rest_framework.response import Response
from rest_framework.views import APIView

from django.core.mail import send_mail
from django.db.models import Q


from Conexion.Serializadores.CustomsSerializers import *
from Conexion.Serializadores.SesionesActivasSerializers import *
from Conexion.Serializadores.UsuariosSerializers import *
from Conexion.Serializadores.CategoriasGastosSerializers import *
from Conexion.Serializadores.MesesSerializers import *
from Conexion.models import Usuarios,SesionesActivas,Meses
from MyFinancesBackend.settings import TIEMPO_SESION_HORAS
from Conexion.Seguridad.validaciones import resgistrosesion
import re


class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        user_name = request.data.get('username', '')
        
        password = request.data.get('password', '')
        registro_sesion=resgistrosesion(user_name)
        
        if registro_sesion:

            condicion1=Q(user_name__exact=user_name)  
            tokenusuario=SesionesActivas.objects.filter(condicion1).values()
            
            for item in tokenusuario:
                datotoken=(item['token_session'])
                condticiontoken=Q(key__exact=datotoken)
                existetoken=Token.objects.filter(condticiontoken).values()
                if existetoken:
                    t=Token.objects.get(key=datotoken)
                    t.delete()
            
            SesionesActivas.objects.filter(user_name__iexact=user_name).delete()
            
        user = authenticate(username=user_name,password=password)
        
        if user:
            user_agent = request.META.get('HTTP_USER_AGENT', 'Desconocido')
            
            token,created=Token.objects.get_or_create(user=user)
           
            consultausuarios=Usuarios.objects.filter(user_name__exact=user).values()
            
            fechareg=str(consultausuarios[0]['fecha_registro'])
            fecha_obj = datetime.fromisoformat(fechareg)
            fecha_formateada = fecha_obj.strftime("%d/%m/%Y %H:%M:%S")
            
            
            try:
        
                datasesion=({
                    'user_name':user_name,
                    'fecha_conexion':datetime.now(),
                    'token_session':token.key,
                    'dispositivo':user_agent
                })

                datauser=[{
                    'username':consultausuarios[0]['user_name'].capitalize(),
                    'nombre':consultausuarios[0]['nombre_usuario'],
                    'apellido':consultausuarios[0]['apellido_usuario'],
                    'fecha_registro':fecha_formateada,
                    
                }

                ]
            
               
                sesion_serializers=SesionesActivasSerializers(data=datasesion)
                if sesion_serializers.is_valid():
                    
                    sesion_serializers.save()
                
                
                    login_serializer = self.serializer_class(data=request.data)
                    if login_serializer.is_valid():

                        
                        
                        return Response({
                            'token': login_serializer.validated_data.get('access'),
                            'refresh': login_serializer.validated_data.get('refresh'),
                            'sesion':token.key,
                            'user_name':user_name.capitalize(),
                            'datauser':datauser,
                            'message': 'Inicio de Sesion Existoso'
                        }, status=status.HTTP_200_OK)
                    return Response({'error': 'Contraseña o nombre de usuario incorrectos'}, status=status.HTTP_400_BAD_REQUEST)
                else :
                    
                    return Response({'error': sesion_serializers.errors}, status=status.HTTP_400_BAD_REQUEST)
                

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
        condicion1 = Q(username__exact=user_reg)
        existente=User.objects.filter(condicion1).values()

        if not existente:
            
                
            user_registrar = User.objects.create_user(user_reg, password=password)
            user_registrar.save()
            condicion1 = Q(username__exact=user_reg)
            datosnuevo=list(User.objects.filter(condicion1).values())
            id_nuevo=datosnuevo[0]['id']
            data_user=(
                {
                    'id':id_nuevo,
                    'nombre_usuario':nombre,
                    'apellido_usuario':apellido,
                    'fecha_nacimiento':nacimiento,
                    'user_name':user_reg,
                    'correo':correo,
                    'ultima_conexion':datetime.now(),
                    'fecha_registro':datetime.now()
                }
            )
            
            user_serializer=UsuariosSerializer(data=data_user)
            if user_serializer.is_valid():

                user_serializer.save()
                n=1
                while n < 3:
                    
                    if n==1:
                        catnombre='Servicios'
                    else:
                        catnombre='Productos'
                    data_list_cat1 = []
                    datasavecat1={
                        "user": id_nuevo,
                        "nombre_categoria": catnombre,
                        "fecha_registro": datetime.now()
                        
                    }
                    data_list_cat1.append(datasavecat1)
                    categoria1_serializer=CategoriaGastosSerializers(data=datasavecat1)
                    if categoria1_serializer.is_valid():
                        categoria1_serializer.save()
                    
                    n=n+1
            
                user_agent = request.META.get('HTTP_USER_AGENT', 'Desconocido')
                
                token,created=Token.objects.get_or_create(user=user_registrar)
            
                datasesion=({
                    'user_name':user_reg,
                    'fecha_conexion':datetime.now(),
                    'token_session':token.key,
                    'dispositivo':user_agent,
                    
                })

                sesion_serializers=SesionesActivasSerializers(data=datasesion)
                if sesion_serializers.is_valid():
                    
                    sesion_serializers.save()
                
                
                datalogin={
                    'username':user_reg,
                    'password':password
                
                }
                
                login_serializer = self.serializer_class(data=datalogin)
                if login_serializer.is_valid():
                    
                    return Response({
                        'token': login_serializer.validated_data.get('access'),
                        'refresh': login_serializer.validated_data.get('refresh'),
                        'sesion':token.key,
                        'user_name':user_reg.capitalize(),
                        'message': 'Inicio de Sesion Existoso'
                    }, status=status.HTTP_200_OK)
                
                
            else :
                
                mensajes_error = {}

                for campo, detalles in user_serializer.errors.items():
                    mensaje = detalles[0]
                    if hasattr(mensaje, 'string'):
                        mensajes_error[campo] = mensaje.string
                    else:
                        mensajes_error[campo] = str(mensaje)

                user_registrar.delete()
                return Response({'error':mensajes_error},status= status.HTTP_400_BAD_REQUEST)   
    
        else:
            mensajes_error = {}
            mensajes_error['Username']='Ya se creo el usuario ' + user_reg
            return Response({'error':mensajes_error},status= status.HTTP_400_BAD_REQUEST) 

class NotFoundView(APIView):
    """
    Tipo notificacion: 

    - Descripcion: Retorna error cuando se ingresa un endpoint que no existe
    
    
    """
    def get(self, request, *args, **kwargs):
        return Response({"message": "La ruta solicitada no se encuentra"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        return Response({"message": "La ruta solicitada no se encuentra"}, status=status.HTTP_404_NOT_FOUND)
    



class ComprobarConexion(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def get(self, request, *args, **kwargs):
        lista = Meses.objects.order_by('numero_mes')
        
        if lista:
            result_serializer=MesesSerializers(lista,many=True)

            if result_serializer.data:
                return Response({'conexion':'OK'},status= status.HTTP_200_OK)
            
                
        else:
            return Response({'conexion':'NO'},status= status.HTTP_500_INTERNAL_SERVER_ERROR)
    



            
        





def formato_user(data):
    
    data = data.replace(" ", "")
    data = data.lower()
    data = re.sub(r'[^a-zA-Z0-9]', '', data)
    return data