from django.db.models import Q


from rest_framework.response import Response
from rest_framework import status  
from rest_framework.decorators import api_view
import pandas as pd


from Conexion.obtener_datos_token import obtener_datos_token
from Conexion.validaciones import validacionpeticion

from Conexion.models import Egresos, Ingresos
from Conexion.Serializers import EgresosSerializers, IngresosSerializers,BalanceSerializers,ResumenSerializers
from Conexion.Apis.listados.datos import registros_egresos,registros_ingresos,datos_resumen,datos_balance

@api_view(['POST'])
def resumen(request,anno,mes):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True: 
        # Obtener datos de la base de datos
        
        datosresumen=datos_resumen(id_user,anno,mes)
        return Response(datosresumen, status=status.HTTP_200_OK)
        
        
    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)
    


@api_view(['POST'])
def balance(request,anno,mes):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True: 
        # Obtener datos de la base de datos
        
        datosbalance=datos_balance(id_user,anno,mes)
        return Response(datosbalance, status=status.HTTP_200_OK)
       
        
    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)