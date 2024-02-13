from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status  
from rest_framework.decorators import api_view
import pandas as pd

from io import BytesIO
from django.http import HttpResponse
import matplotlib 
matplotlib.use('Agg')

import matplotlib.pyplot as plt

import base64
from Conexion.obtener_datos_token import obtener_datos_token
from Conexion.validaciones import validacionpeticion
from tempfile import NamedTemporaryFile
from  Conexion.models import Egresos, Ingresos
from  Conexion.Serializers import EgresosSerializers, IngresosSerializers,BalanceSerializers
@api_view(['POST'])
def graf_balance(request,anno,mes):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True: 
        # Obtener datos de la base de datos
        
        condicion1 = Q(user_id__exact=id_user)
        condicion2 = Q(fecha_gasto__year=anno)
        condicion3 = Q(fecha_gasto__month=mes)
        egresos=Egresos.objects.filter(condicion1 & condicion2 & condicion3)


        ingresos = Ingresos.objects.all()
        condicion1 = Q(user_id__exact=id_user)
        condicion2 = Q(fecha_ingreso__year=anno)
        condicion3 = Q(fecha_ingreso__month=mes)
        ingresos=Ingresos.objects.filter(condicion1 & condicion2 & condicion3)

        # Convertir a DataFrames de Pandas
        df_egresos = pd.DataFrame(EgresosSerializers(egresos, many=True).data)
        df_ingresos = pd.DataFrame(IngresosSerializers(ingresos, many=True).data)

        # Realizar operaciones y cálculos necesarios en los DataFrames

        # Generar gráfico HTML con Plotly
        # print(df_egresos)
        df_egresos_agrupado = df_egresos.groupby(['NombreGasto','TipoGasto'])['monto_gasto'].sum().reset_index()
        
        
        df_ingresos_total = df_ingresos['monto_ingreso'].sum()
        
        
        valores = [df_ingresos_total, df_egresos_agrupado['monto_gasto'].sum()] 
        labels = ['Ingresos', 'Egresos']

        # Crear gráfico
        fig, ax = plt.subplots()
        ax.pie(valores, labels=labels)

        # Guardar como imagen PNG
        buffer = BytesIO()
        fig.savefig(buffer, format='png')
        imagen_bytes = buffer.getvalue()

        # b64_string = "data:image/png;base64," + base64.b64encode(cadena_base64).decode('utf-8') 
        imagen_b64 = base64.b64encode(imagen_bytes).decode('utf-8') 
        
        try:
            base64.b64decode(imagen_b64)
            print("Cadena base64 válida")
        except Exception as e:
            print("Cadena base64 inválida")
        return Response({
            'imagen_grafico': imagen_b64
        })

    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)