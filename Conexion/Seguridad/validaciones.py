from Conexion.models import	SesionesActivas
from rest_framework.authtoken.models import Token
from datetime import timedelta
from django.utils import timezone
from MyFinancesBackend.settings import TOKEN_EXPIRED_AFTER_SECONDS,TOKEN_EXPIRED_AFTER_HOURS,TOKEN_SESION_TIEMPO
from Conexion.models import Usuarios
from django.db.models import Q

def resgistrosesion(nombreusuario):
    result=False
    condicion1=Q(user_name__exact=nombreusuario)
    condicion2=Q(Estado__exact=1)
    dato=SesionesActivas.objects.filter(condicion1 & condicion2)
    if dato.exists():
        result=True
    return result

def controlexpiraciontoken(tokenvalue):
    respuesta_expiracion_token='OK'
    time_elapsed=0
    left_time=0
    token=Token.objects.filter(key__exact=tokenvalue).values()
    
    
    
    if token.exists():
        tokenresult=token[0]
        tokencreacion=tokenresult['created']
        
        time_elapsed = timezone.now() - tokencreacion
        left_time = timedelta(hours=TOKEN_SESION_TIEMPO) - time_elapsed

        if left_time < timedelta(hours = 0):
            respuesta_expiracion_token='TOKEN EXPIRADO'

        
    else:
        respuesta_expiracion_token='TOKEN INVALIDO'

    return respuesta_expiracion_token

def controlexpiracionsesion(usuario):
    respuesta_expiracion_sesion='OK'
    condicion1=Q(user_name__exact=usuario)
    condicion2=Q(Estado__exact=1)
    sesionactiva=SesionesActivas.objects.filter(condicion1 & condicion2).values()

    if sesionactiva.exists():
        fechavencimientosesion=sesionactiva[0]['expiracion_conexion']
        
        if timezone.now() > fechavencimientosesion:
            respuesta_expiracion_sesion='Sesion expirada'

    else:
        respuesta_expiracion_sesion='El usuario no cuenta con sesion activa'

    # return timezone.now() > fechavencimientosesion
    return respuesta_expiracion_sesion

def validaciones( tokensesion):
    controltoken=controlexpiraciontoken(tokensesion)
    controlsesion=False
    comprobacionusuariotoken='OK'
    user_token=''
    datos_token=Token.objects.filter(key__exact=tokensesion).values()
    comprobacionidtoken='OK'
    if datos_token:
        user_id=datos_token[0]['user_id']
        if controltoken != 'TOKEN INVALIDO':
        
            datotoken=SesionesActivas.objects.filter(token_session__exact=tokensesion).values()
            
            if datotoken:
                user_token=datotoken[0]['user_name']
                estado=datotoken[0]['Estado']
                datos_user=Usuarios.objects.filter(user_name__exact=user_token).values()
                
                if  datos_user :
                    id=datos_user[0]['id']
                    
                    if estado==0:
                        comprobacionidtoken='La sesion ya vencio'
                    else:
                        if id==user_id:
                            controlsesion=controlexpiracionsesion(user_token)
                        else:
                            comprobacionidtoken='El id del usuario no coincide con el del TOKEN'
                else: 
                    comprobacionusuariotoken='La cedula no pertence a ningun usuario registrado'
            else:
                comprobacionusuariotoken='Ya no se encuentra la sesion del token'
        else:
            comprobacionusuariotoken='No se pudo realizar la verificacion de la cedula del Token'
    else:
        comprobacionidtoken='No se encontro in id para el  TOKEN'
        
    return controlsesion,controltoken,comprobacionusuariotoken,comprobacionidtoken





def validacionpeticion(tokensesion):
   
    
    token_sesion=tokensesion
    controlsesion,controltoken,controlvalidacionusurio,controlid=validaciones(token_sesion)
   
    if controlsesion=='OK' and controltoken=='OK' and controlvalidacionusurio=='OK' and controlid=='OK':
        
        return True
    else:
        return {
                'controlsesion':controlsesion,
                'controltoken':controltoken,
                'controlvalidacionusuario':controlvalidacionusurio,
                'controlid':controlid,
        }


