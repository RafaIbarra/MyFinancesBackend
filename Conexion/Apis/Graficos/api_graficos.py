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
import numpy as np
import matplotlib.pyplot as plt

import base64
from Conexion.Seguridad.obtener_datos_token import obtener_datos_token
from Conexion.Seguridad.validaciones import validacionpeticion
from tempfile import NamedTemporaryFile
from  Conexion.models import Egresos, Ingresos
# from  Conexion.Serializers import EgresosSerializers, IngresosSerializers,BalanceSerializers
from Conexion.Serializadores.EgresosSerializers import *
from Conexion.Serializadores.IngresosSerializers import *
from Conexion.Serializadores.BalanceSerializers import *
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

        if egresos and ingresos:
            df_egresos = pd.DataFrame(EgresosSerializers(egresos, many=True).data)
            df_ingresos = pd.DataFrame(IngresosSerializers(ingresos, many=True).data)

            
            df_egresos_agrupado = df_egresos.groupby(['NombreGasto','TipoGasto'])['monto_gasto'].sum().reset_index()
            print(df_egresos_agrupado)
            
            
            df_ingresos_total = df_ingresos['monto_ingreso'].sum()
            
            
            valores = [df_ingresos_total, df_egresos_agrupado['monto_gasto'].sum()] 
            labels = ['Ingresos', 'Egresos']
            print('valores')
            print(valores)
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
             return Response({'message':'sin datos'},status= status.HTTP_200_OK)

    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)
    

@api_view(['POST'])
def graf_balance_prueba(request,anno,mes):
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

        if egresos and ingresos:
            df_egresos = pd.DataFrame(EgresosSerializers(egresos, many=True).data)
            df_ingresos = pd.DataFrame(IngresosSerializers(ingresos, many=True).data)

            df_egresos_agrupado = df_egresos.groupby(['NombreGasto'])['monto_gasto'].sum().reset_index()

            df_ingresos_total = pd.DataFrame( 

                {   'Concepto': ['TotalSalario'],
                    'TotalIngreso':[df_ingresos['monto_ingreso'].sum()]
                }
                )
            
            df_combinado = pd.concat([df_ingresos_total, df_egresos_agrupado], axis=1)
            df_combinado = df_combinado.fillna(0)
            labels = []
            valores = []
            for label, valor in zip(df_combinado['Concepto'].tolist() + df_combinado['NombreGasto'].tolist(),
                        df_combinado['TotalIngreso'].tolist() + df_combinado['monto_gasto'].tolist()):
                if valor != 0:
                    labels.append(label)
                    valores.append(valor)
            
            fig, ax = plt.subplots()
            ax.pie(valores,labels=labels,
                #    autopct='%1.1f%%',
                   startangle=90)
            buffer = BytesIO()
            fig.savefig(buffer, format='png')
            imagen_bytes = buffer.getvalue()

            
            imagen_b64 = base64.b64encode(imagen_bytes).decode('utf-8') 
        
            return Response({
                'imagen_grafico': imagen_b64
            })
        else:
             return Response({'message':'sin datos'},status= status.HTTP_200_OK)

    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)
    


@api_view(['POST'])
def graf_barra_agrupada(request,anno,mes):
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

        if egresos and ingresos:

            df_egresos = pd.DataFrame(EgresosSerializers(egresos, many=True).data)
            df_ingresos = pd.DataFrame(IngresosSerializers(ingresos, many=True).data)

            df_egresos_agrupado = df_egresos.groupby(['NombreGasto'])['monto_gasto'].sum().reset_index()
            totalingresos=df_ingresos['monto_ingreso'].sum()
            
            # print(totalingresos)
            df_egresos_agrupado['total_ingresos'] = totalingresos 
            df_egresos_agrupado['porcentaje'] = df_egresos_agrupado['monto_gasto'] / df_egresos_agrupado['total_ingresos'] * 100

            df_ingresos_total = pd.DataFrame( 

                {   'Concepto': ['TotalSalario'],
                    'TotalIngreso':[df_ingresos['monto_ingreso'].sum()]
                }
                )
            # print(df_egresos_agrupado)
            ###################################################################################################################
            
            # ingresos_data = {'Concepto': ['TotalSalario'], 'TotalIngreso': [7250000]}
            # egresos_data = {'NombreGasto': ['Compra Cerveza', 'Compra Lomito Arabe', 'Pago Agua', 'Pago Ande', 'Pago WiFI'],
            #                 'monto_gasto': [70000, 66000, 25000, 85000, 262500]}
            
            
            ingresos = df_ingresos_total['TotalIngreso'].tolist()
            conceptos = df_ingresos_total['Concepto'].tolist()
            
            gastos = df_egresos_agrupado['monto_gasto'].tolist()
            porcentajes = df_egresos_agrupado['porcentaje'].tolist()
            nombres_gastos = df_egresos_agrupado['NombreGasto'].tolist()
            print(nombres_gastos)
            # Gráfico
            fig, ax = plt.subplots(figsize=(6, 7))
            plt.gcf().subplots_adjust(bottom=0.5)
            # Ancho de barras 
            bar_width = 0.2

            # Espaciado entre barras
            bar_spacing = 0.1 
            x = 0 
            # Posicion  es de barras con espaciado
            bar_positions = [x + i * (bar_width + bar_spacing) for i in range(len(gastos) + 1)]

            # Posición barra ingresos
            x = bar_positions[0]

            # Posiciones barras gastos
            gastos_bar_positions = bar_positions[1:]

            # Barras 
            ingresos_bar = ax.bar(x, ingresos, bar_width)
            for i, gasto in enumerate(gastos):
                gastos_bar = ax.bar(gastos_bar_positions[i], gasto, bar_width)

            for i, porcentaje in enumerate(porcentajes):
    
            
                # Agregar texto con porcentaje
                ax.text(
                    gastos_bar_positions[i], # Posición x de la barra
                    gasto + 5000, # Posición y ligeramente arriba de la barra
                    f"{porcentaje:.1f}%", # Texto con el porcentaje
                    ha="center" # Alineación horizontal centrada
                )

            # Etiquetas
            
            ax.set_xticks(bar_positions)
            ax.set_xticklabels(conceptos + nombres_gastos)

            for label in ax.get_xmajorticklabels():
                label.set_rotation(15) 
                label.set_ha("right")
                label.set_rotation_mode("anchor")
                label.set_fontsize(7)


            # Otros detalles gráfico 
            ax.set_ylabel('Monto')
            ax.set_title('Ingresos vs Egresos')
            ax.legend()
                        
            buffer = BytesIO()
            fig.savefig(buffer, format='png')
            buffer.seek(0)
            imagen_bytes = buffer.getvalue()

            
            imagen_b64 = base64.b64encode(imagen_bytes).decode('utf-8') 
        
            return Response({
                'imagen_grafico': imagen_b64
            })
            # return Response({'message':'sin datos'},status= status.HTTP_200_OK)
        else:
             return Response({'message':'sin datos'},status= status.HTTP_200_OK)
        
        # return Response({'message':'sin datos'},status= status.HTTP_200_OK)

    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)
    



@api_view(['POST'])
def graf_torta_egresos(request,anno,mes):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True: 
        # Obtener datos de la base de datos
        
        condicion1 = Q(user_id__exact=id_user)
        condicion2 = Q(fecha_gasto__year=anno)
        condicion3 = Q(fecha_gasto__month=mes)
        egresos=Egresos.objects.filter(condicion1 & condicion2 & condicion3)

        if egresos :
            df_egresos = pd.DataFrame(EgresosSerializers(egresos, many=True).data)
            

            df_egresos_agrupado = df_egresos.groupby(['NombreGasto'])['monto_gasto'].sum().reset_index()
            labels =df_egresos_agrupado['NombreGasto'].tolist()
            valores = df_egresos_agrupado['monto_gasto'].tolist()
        
            fig, ax = plt.subplots()
            ax.pie(valores,labels=labels,
                   autopct='%1.1f%%',
                   startangle=90)
            buffer = BytesIO()
            fig.savefig(buffer, format='png')
            imagen_bytes = buffer.getvalue()

            
            imagen_b64 = base64.b64encode(imagen_bytes).decode('utf-8') 
        
            return Response({
                'imagen_grafico': imagen_b64
            })
        else:
             return Response({'message':'sin datos'},status= status.HTTP_200_OK)

    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)
    

@api_view(['POST'])
def graf_torta_ingresos(request,anno,mes):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True: 
        # Obtener datos de la base de datos
        
        ingresos = Ingresos.objects.all()
        condicion1 = Q(user_id__exact=id_user)
        condicion2 = Q(fecha_ingreso__year=anno)
        condicion3 = Q(fecha_ingreso__month=mes)
        ingresos=Ingresos.objects.filter(condicion1 & condicion2 & condicion3)

        if ingresos :
            ingresos = pd.DataFrame(IngresosSerializers(ingresos, many=True).data)
            

            df_ingresos_agrupado = ingresos.groupby(['NombreIngreso'])['monto_ingreso'].sum().reset_index()
            labels =df_ingresos_agrupado['NombreIngreso'].tolist()
            valores = df_ingresos_agrupado['monto_ingreso'].tolist()
        
            fig, ax = plt.subplots()
            ax.pie(valores,labels=labels,
                   autopct='%1.1f%%',
                   startangle=90)
            buffer = BytesIO()
            fig.savefig(buffer, format='png')
            imagen_bytes = buffer.getvalue()

            
            imagen_b64 = base64.b64encode(imagen_bytes).decode('utf-8') 
        
            return Response({
                'imagen_grafico': imagen_b64
            })
        else:
             return Response({'message':'sin datos'},status= status.HTTP_200_OK)

    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)