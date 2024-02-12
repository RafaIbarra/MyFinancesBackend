from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status  
from rest_framework.decorators import api_view
import pandas as pd
import plotly.express as px
import plotly.offline as opy
from io import BytesIO
from django.http import HttpResponse

from Conexion.obtener_datos_token import obtener_datos_token
from Conexion.validaciones import validacionpeticion

from  Conexion.models import Egresos, Ingresos
from  Conexion.Serializers import EgresosSerializers, IngresosSerializers,BalanceSerializers

@api_view(['POST'])
def balance(request,anno,mes):
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
        # print(df_egresos_agrupado)
        # print(df_ingresos)
        df_ingresos_agrupado = df_ingresos.groupby(['NombreIngreso','TipoIngreso'])['monto_ingreso'].sum().reset_index()
        # print(df_ingresos_agrupado)
        

        # df_egresos_agrupado['NombreGasto_TipoGasto'] = df_egresos_agrupado['NombreGasto'] + '_' + df_egresos_agrupado['TipoGasto']
        # df_ingresos_agrupado['NombreIngreso_TipoIngreso'] = df_ingresos_agrupado['NombreIngreso'] + '_' + df_ingresos_agrupado['TipoIngreso']

        # df_final = pd.merge(df_egresos_agrupado, df_ingresos_agrupado, left_on='NombreGasto_TipoGasto', right_on='NombreIngreso_TipoIngreso', how='outer')

        # df_final = df_final.drop(['NombreGasto_TipoGasto', 'NombreIngreso_TipoIngreso'], axis=1)
        df_egresos_agrupado['Codigo'] = 2
        df_egresos_agrupado = df_egresos_agrupado.rename(columns={'NombreGasto': 'Descripcion', 'TipoGasto': 'Tipo', 'monto_gasto': 'MontoEgreso'})
        df_ingresos_agrupado['Codigo'] = 1
        df_ingresos_agrupado = df_ingresos_agrupado.rename(columns={'NombreIngreso': 'Descripcion', 'TipoIngreso': 'Tipo', 'monto_ingreso': 'MontoIngreso'})
        df_final = pd.merge(df_ingresos_agrupado,df_egresos_agrupado,  on=['Codigo','Descripcion', 'Tipo'], how='outer', suffixes=('_Ingreso','_Egreso' ))
        df_final = df_final.fillna(0)
        
        sumaingresos=df_final['MontoIngreso'].sum()
        sumaegresos=df_final['MontoEgreso'].sum()
        saldo=sumaingresos- sumaegresos
        
        list_saldos={'Codigo':3,'Descripcion':'Totales','Tipo':'Resumen','MontoIngreso':sumaingresos,'MontoEgreso':sumaegresos}
        df_final = df_final.sort_values(by='MontoIngreso',ascending=False) 
        
        
        df_saldos = pd.DataFrame([list_saldos])
        df_result_final = pd.concat([df_final, df_saldos], ignore_index=True, sort=False)
        df_result_final = df_result_final.fillna(0)
        df_result_final['Saldo']=saldo
        print(df_result_final)
        data_list = df_result_final.to_dict(orient='records')
        resultado=BalanceSerializers(data=data_list,many=True)
        
        if resultado.is_valid():
            
            return Response(resultado.data,status= status.HTTP_200_OK)
    
        return Response({'message':resultado.errors},status= status.HTTP_400_BAD_REQUEST)

        # Enviar el HTML del gráfico como respuesta
        # fig = px.bar(df_egresos, x='NombreGasto', y='monto_gasto', title='Egresos por Concepto')
        # plot_html = opy.plot(fig, auto_open=False, output_type='div')
        # return Response({'plot_html': plot_html})
    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)