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
def estadistica_grafico_linas(data,titulo,promedio_periodo):
    
    periodos=data['Periodo'].to_list()
    montos=data['SumaMonto'].to_list()
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.plot(periodos, montos, color = 'tab:purple', marker = 'o')
    ax.grid(axis = 'y', color = 'gray', linestyle = 'dashed')
    ax.set_xlabel("Periodos", fontdict = {'fontsize':12, 'fontweight':'bold', 'color':'tab:blue'})
    ax.set_ylabel("Montos Gastos")
    ax.set_title(titulo, loc = "left", fontdict = {'fontsize':14, 'fontweight':'bold', 'color':'tab:blue'})
    ax.axhline(y=promedio_periodo, color='r', linestyle='-',label='Promedio')
    ax.legend()
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    imagen_grafico_lineas_bytes = buffer.getvalue()
    imagen_grafico_lineas_b64 = base64.b64encode(imagen_grafico_lineas_bytes).decode('utf-8') 
    plt.close('all')
    return imagen_grafico_lineas_b64
    
def estadistica_grafico_15_dias(data):
    
    labels =data['CategoriaGasto'].tolist()
    valores = data['CantidadVeces'].tolist()
    fig, ax = plt.subplots()
    ax.pie(valores,labels=labels,
                   autopct='%1.1f%%',
                   startangle=90)
    
    # ax.legend(labels=labels,loc="lower center", 
    #           bbox_to_anchor=(0.5, -0.3),ncol=len(labels),
    #           fontsize="small")
            
    plt.subplots_adjust(bottom=0.2)
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    imagen_15dias_bytes = buffer.getvalue()
    
    imagen_15dias_b64 = base64.b64encode(imagen_15dias_bytes).decode('utf-8')
    plt.close('all')
    return imagen_15dias_b64