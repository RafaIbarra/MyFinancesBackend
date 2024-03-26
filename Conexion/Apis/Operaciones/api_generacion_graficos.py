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
import seaborn as sns

import base64

from  Conexion.models import Egresos, Ingresos
from Conexion.Serializadores.EgresosSerializers import *
from Conexion.Serializadores.IngresosSerializers import *
from Conexion.Serializadores.BalanceSerializers import *


def generar_graf_torta_resumen(ingresos,egresos):
 
    data_egresos=egresos

  
    data_ingresos=ingresos

    if data_ingresos and data_egresos:
        

        df_data_egresos=pd.DataFrame(data_egresos)
        df_data_egresos['Periodo']=df_data_egresos['NombreMesEgreso'] + '-' + df_data_egresos['AnnoEgreso'].astype(str)
        df_data_egresos=df_data_egresos.reset_index()

        df_data_egreso_agrupado = df_data_egresos.groupby(['AnnoEgreso', 'MesEgreso','NombreMesEgreso','Periodo']).agg({'monto_gasto': ['sum']})
        df_data_egreso_agrupado.columns = ['SumaMontoEgreso']
        df_data_egreso_agrupado = df_data_egreso_agrupado.sort_values(by=['AnnoEgreso', 'MesEgreso'], ascending=[True, True])
        df_data_egreso_agrupado = df_data_egreso_agrupado.reset_index()


        df_data_ingresos=pd.DataFrame(data_ingresos)
        df_data_ingresos['Periodo']=df_data_ingresos['NombreMesIngreso'] + '-' + df_data_ingresos['AnnoIngreso'].astype(str)
        df_data_ingresos=df_data_ingresos.reset_index()

        df_data_ingresos_agrupado = df_data_ingresos.groupby(['AnnoIngreso', 'MesIngreso','NombreMesIngreso','Periodo']).agg({'monto_ingreso': ['sum']})
        df_data_ingresos_agrupado.columns = ['SumaMontoIngreso']
        df_data_ingresos_agrupado = df_data_ingresos_agrupado.sort_values(by=['AnnoIngreso', 'MesIngreso'], ascending=[True, True])
        df_data_ingresos_agrupado = df_data_ingresos_agrupado.reset_index()

        df_resultado = pd.merge(df_data_ingresos_agrupado, df_data_egreso_agrupado, on='Periodo', how='inner')
        df_resultado=df_resultado.rename(columns={'AnnoIngreso':'AnnoOperacion','MesIngreso':'MesOperacion', 'NombreMesIngreso':'NombreMesOperacion'})
        columns_to_drop = ['AnnoEgreso', 'MesEgreso','NombreMesEgreso']
        df_resultado = df_resultado.drop(columns=columns_to_drop)

        df_resultado['Saldo']=df_resultado['SumaMontoIngreso'] - df_resultado['SumaMontoEgreso']
        df_resultado['PorcentajeEgreso']= round( df_resultado['SumaMontoEgreso']/df_resultado['SumaMontoIngreso'] * 100 , 2)
        df_resultado['PorcentajeSaldo']=round(df_resultado['Saldo'] / df_resultado['SumaMontoIngreso'] * 100 , 2)
        
        fila1=pd.DataFrame({'Concepto': 'Saldo Disponible', 'Monto': df_resultado['Saldo'].to_list()})
        fila2=pd.DataFrame({'Concepto': 'Total Egreso', 'Monto': df_resultado['SumaMontoEgreso'].to_list()})
        
        df_nuevo = pd.concat([ fila1, fila2], ignore_index=True)
        labels =df_nuevo['Concepto'].tolist()
        valores = df_nuevo['Monto'].tolist()
        colors = ['skyblue', 'lightcoral']
        fig, ax = plt.subplots()
        ax.pie(valores, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)

        centre_circle = plt.Circle((0,0),0.7,fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        ax.axis('equal') 
        
        buffer = BytesIO()
        fig.savefig(buffer, format='png')
        imagen_resumen_bytes = buffer.getvalue()

        
        imagen_resumen_bytes_b64 = base64.b64encode(imagen_resumen_bytes).decode('utf-8') 
        plt.close('all')
        return  imagen_resumen_bytes_b64
        

def generar_graf_barra_resumen(id_user,anno,mes):
    
  
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

        

        ingresos = df_ingresos_total['TotalIngreso'].tolist()
        conceptos = df_ingresos_total['Concepto'].tolist()
        

        gastos = df_total_egresos['TotalEgreso'].tolist()
        porcentajes = df_total_egresos['porcentaje'].tolist()
        nombres_gastos = df_total_egresos['Concepto'].tolist()
        
 
        fig, ax = plt.subplots(figsize=(5, 7))
        plt.gcf().subplots_adjust(bottom=0.5)
   
        bar_width = 0.3


        bar_spacing = 0.00 
        x = 0 

        bar_positions = [x + i * (bar_width + bar_spacing) for i in range(len(gastos) + 1)]
        
    
        x = bar_positions[0]

   
        gastos_bar_positions = bar_positions[1:]

     
        ingresos_bar = ax.bar(x, ingresos, bar_width)
        
        for i, gasto in enumerate(gastos):
            label = nombres_gastos[i]
            gastos_bar = ax.bar(gastos_bar_positions[i], gasto, bar_width,label=label)


        for i, porcentaje in enumerate(porcentajes):

        

            ax.text(
                gastos_bar_positions[i],
                gasto + 5000,
                f"{porcentaje:.1f}%", 
                ha="center" 
            )

        ax.set_xticks(bar_positions)
        ax.set_xticklabels(conceptos + nombres_gastos)

        for label in ax.get_xmajorticklabels():
            label.set_rotation(0) 
            label.set_ha("right")
            label.set_rotation_mode("anchor")
            label.set_fontsize(10)


 
        ax.set_ylabel('Monto')
    
        
                    
        buffer = BytesIO()
        fig.savefig(buffer, format='png')
        buffer.seek(0)
        imagen_resumen_bytes = buffer.getvalue()

        
        imagen_resumen_b64 = base64.b64encode(imagen_resumen_bytes).decode('utf-8') 
        plt.close('all')
        return imagen_resumen_b64
        

    else:
        return[]
        

    
def generar_graf_torta_egresos(id_user,anno,mes):
    

    condicion1 = Q(user_id__exact=id_user)
    condicion2 = Q(fecha_gasto__year=anno)
    condicion3 = Q(fecha_gasto__month=mes)
    egresos=Egresos.objects.filter(condicion1 & condicion2 & condicion3)

    if egresos :
        df_egresos = pd.DataFrame(EgresosSerializers(egresos, many=True).data)
        total_egreso=df_egresos['monto_gasto'].sum()
    
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
        num_categorias = len(df_egresos_agrupado) # determinar el tamaño del arreglo    

     
        colores = sns.color_palette("viridis", num_categorias)
        colores = colores[::-1]

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
        plt.close('all')
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
        plt.close('all')
        return imagen_ingresos_b64
    else:
        return[]
    
    