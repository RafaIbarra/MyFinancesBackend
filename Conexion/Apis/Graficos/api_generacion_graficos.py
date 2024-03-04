from django.db.models import Q


import pandas as pd

from io import BytesIO

import matplotlib 
matplotlib.use('Agg')
from matplotlib import  patches as mpatches
from matplotlib import colors as mcolors
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

import base64
from Conexion.Seguridad.obtener_datos_token import obtener_datos_token
from Conexion.Seguridad.validaciones import validacionpeticion
from tempfile import NamedTemporaryFile
from  Conexion.models import Egresos, Ingresos
# from  Conexion.Serializers import EgresosSerializers, IngresosSerializers,BalanceSerializers
from Conexion.Serializadores.EgresosSerializers import *
from Conexion.Serializadores.IngresosSerializers import *
from Conexion.Serializadores.BalanceSerializers import *


def generar_graf_barra_resumen(id_user,anno,mes):
    
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
        

        df_egresos_agrupado['total_ingresos'] = totalingresos 
        df_egresos_agrupado['porcentaje'] = df_egresos_agrupado['monto_gasto'] / df_egresos_agrupado['total_ingresos'] * 100

        df_ingresos_total = pd.DataFrame( 

            {   'Concepto': ['Total Ingreso'],
                'TotalIngreso':[df_ingresos['monto_ingreso'].sum()]
            }
            )
        
        df_total_egresos=pd.DataFrame(
            {   'Concepto': ['Total Egresos'],
                'TotalEgreso':[df_egresos['monto_gasto'].sum()]
            }
        )

        df_total_egresos['porcentaje']= df_total_egresos['TotalEgreso'] /totalingresos * 100

        print(df_total_egresos)

        ingresos = df_ingresos_total['TotalIngreso'].tolist()
        conceptos = df_ingresos_total['Concepto'].tolist()
        
        # gastos = df_egresos_agrupado['monto_gasto'].tolist()
        # porcentajes = df_egresos_agrupado['porcentaje'].tolist()
        # nombres_gastos = df_egresos_agrupado['NombreGasto'].tolist()

        gastos = df_total_egresos['TotalEgreso'].tolist()
        porcentajes = df_total_egresos['porcentaje'].tolist()
        nombres_gastos = df_total_egresos['Concepto'].tolist()
        
        # Gráfico
        fig, ax = plt.subplots(figsize=(5, 7))
        plt.gcf().subplots_adjust(bottom=0.5)
        # Ancho de barras 
        bar_width = 0.3

        # Espaciado entre barras
        bar_spacing = 0.00 
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
            label = nombres_gastos[i]
            gastos_bar = ax.bar(gastos_bar_positions[i], gasto, bar_width,label=label)

        # ax.legend()
        # ax.legend(loc='upper right', bbox_to_anchor=(1, 1), fontsize=8)
            


        for i, porcentaje in enumerate(porcentajes):

        
            # Agregar texto con porcentaje
            ax.text(
                gastos_bar_positions[i], # Posición x de la barra
                gasto + 5000, # Posición y ligeramente arriba de la barra
                f"{porcentaje:.1f}%", # Texto con el porcentaje
                ha="center" # Alineación horizontal centrada
            )

        # Etiqueta solo para ingreso
        # bar_positions_una=[]
        # bar_positions_una.append(bar_positions[0])
        # ax.set_xticks(bar_positions_una)
        # ax.set_xticklabels(conceptos )

        # Todas las etiquetas
        ax.set_xticks(bar_positions)
        ax.set_xticklabels(conceptos + nombres_gastos)

        for label in ax.get_xmajorticklabels():
            label.set_rotation(0) 
            label.set_ha("right")
            label.set_rotation_mode("anchor")
            label.set_fontsize(10)


        # Otros detalles gráfico 
        ax.set_ylabel('Monto')
        # ax.set_title('Ingresos vs Egresos')
        
                    
        buffer = BytesIO()
        fig.savefig(buffer, format='png')
        buffer.seek(0)
        imagen_resumen_bytes = buffer.getvalue()

        
        imagen_resumen_b64 = base64.b64encode(imagen_resumen_bytes).decode('utf-8') 
        plt.close('all')
        return imagen_resumen_b64
        # return Response({'message':'sin datos'},status= status.HTTP_200_OK)
    else:
        return[]
        
        # return Response({'message':'sin datos'},status= status.HTTP_200_OK)
    
def generar_graf_torta_egresos(id_user,anno,mes):
    
    # Obtener datos de la base de datos
    
    condicion1 = Q(user_id__exact=id_user)
    condicion2 = Q(fecha_gasto__year=anno)
    condicion3 = Q(fecha_gasto__month=mes)
    egresos=Egresos.objects.filter(condicion1 & condicion2 & condicion3)

    if egresos :
        df_egresos = pd.DataFrame(EgresosSerializers(egresos, many=True).data)
        total_egreso=df_egresos['monto_gasto'].sum()
        # fig, ax = plt.subplots(figsize=(8,7))
        fig, ax = plt.subplots()

        df_egresos_agrupado = df_egresos.groupby(['NombreGasto'])['monto_gasto'].sum().reset_index()
        df_egresos_agrupado['total_egreso'] = total_egreso 
        df_egresos_agrupado['porcentaje'] = df_egresos_agrupado['monto_gasto'] / df_egresos_agrupado['total_egreso'] * 100
        
        
        #Para que solo muestre en el grafico aquellos que hayan superado el 5%
        labels = []
        valores_si=[]
        labels_no=[]
        for label, valor in zip(df_egresos_agrupado['NombreGasto'].tolist() , df_egresos_agrupado['porcentaje'].tolist()):
            if valor > 5:
                labels.append(label)
                valores_si.append(valor)
                
            else:
                
                labels_no.append(label)

        
        
        valores = df_egresos_agrupado['monto_gasto'].tolist()

        cmap = cm.get_cmap('viridis')
        num_categorias = len(df_egresos_agrupado) # determinar el tamaño del arreglo    
        colores = [cmap(i / num_categorias) for i in range(num_categorias)]
        mapeo_colores = dict(zip(df_egresos_agrupado['NombreGasto'].tolist(), colores))
        


        colores_torta = [mapeo_colores[label] for label in df_egresos_agrupado['NombreGasto'].tolist()] # Obtener los colores despues de la asignacion
       

        ax.pie(valores_si,
                labels=labels ,
                colors=colores_torta,
                autopct=lambda p: '{:.1f}%'.format(p) if p > 5 else '',
                startangle=90
                )
        
        handles = [mpatches.Patch(color=mapeo_colores[label]) for label in labels_no] # obtener los colores de los valores que no cumplen con el 5 %
        if len(labels_no) >0:
            ax.legend(handles=handles,
                        labels=labels_no,
                        loc="lower center", 
                        bbox_to_anchor=(0.5, -0.3),
                        ncol=len(mapeo_colores),
                        fontsize="small"
                    )
            
            plt.subplots_adjust(bottom=0.2)
        buffer = BytesIO()
        fig.savefig(buffer, format='png')
        imagen_egresos_bytes = buffer.getvalue()

        
        imagen_egresos_b64 = base64.b64encode(imagen_egresos_bytes).decode('utf-8') 
    
        return  imagen_egresos_b64
        
    else:
        return []


def generar_graf_torta_ingresos(id_user,anno,mes):
    
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
        ax.legend(
                    labels=labels,
                    loc="lower center", 
                    bbox_to_anchor=(0.5, -0.3),
                    ncol=len(labels),
                    fontsize="small"
                )
        
        plt.subplots_adjust(bottom=0.2)
        buffer = BytesIO()
        fig.savefig(buffer, format='png')
        imagen_ingresos_bytes = buffer.getvalue()

        
        imagen_ingresos_b64 = base64.b64encode(imagen_ingresos_bytes).decode('utf-8') 
    
        return imagen_ingresos_b64
    else:
        return[]
    
    