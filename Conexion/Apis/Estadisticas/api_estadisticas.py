from django.db.models import Q
import pandas as pd
import numpy as np


from Conexion.Apis.api_generacion_datos import *


from Conexion.Seguridad.obtener_datos_token import obtener_datos_token
from Conexion.Seguridad.validaciones import validacionpeticion
from Conexion.Apis.Estadisticas.EstadisticasEgresos.generacion_datos_egresos import *

from rest_framework.response import Response
from rest_framework import status  
from rest_framework.decorators import api_view



    

@api_view(['POST'])
def estadisticas_egresos(request,anno,mes):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        data_periodo=estadistica_egresos_periodo(id_user,anno,mes)
        data_concepto=estadistica_egresos_conceptos(id_user,anno,mes)
        data_categoria=estadistica_egresos_categoria(id_user,anno,mes)
        data_comportamiento_gasto=estadistica_egresos_quince_dias(id_user,anno,mes)
        data_detalle_por_categoria=estadistica_egresos_por_categoria(id_user,anno,mes)
        return Response({
            'DatosPeriodoGasto':data_periodo,
            'DatosConceptoGasto':data_concepto,
            'DatosCategoriaGasto':data_categoria,
            'DataComportamientoGasto':data_comportamiento_gasto,
            'DataDetallePorCategotria':data_detalle_por_categoria
        }
            
                        ,status= status.HTTP_200_OK) 
    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)