import pandas as pd

from io import BytesIO

import matplotlib 
matplotlib.use('Agg')
from matplotlib import  patches as mpatches
from matplotlib import colors as mcolors
from matplotlib.colors import to_rgba
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import base64
from matplotlib.ticker import FuncFormatter

def format_with_commas(value, pos):
    return '{:,}'.format(int(value))

def estadistica_grafico_linas(data,titulo,promedio_periodo):
    
    periodos=data['NombreMesEgreso'].to_list()
    montos=data['SumaMonto'].to_list()
    tamañoperiodos=len(periodos)
    fig, ax = plt.subplots(figsize=(tamañoperiodos, 4.5))

    ax.plot(periodos, montos, color = 'tab:purple', marker = 'o')

    
    ax.axhline(y=promedio_periodo, color='r', linestyle='-',label='Promedio')
    ax.legend()

    
    
    ax.get_yaxis().set_major_formatter(FuncFormatter(format_with_commas))
    # ax.get_yaxis().get_major_formatter().set_scientific(False)
    ax.grid(axis = 'y', color = 'gray', linestyle = 'dashed')
    ax.set_xlabel("Periodos", fontdict = {'fontsize':9, 'fontweight':'bold', 'color':'tab:blue'})
    ax.set_ylabel("Montos Gastos")
    
    
    ax.set_title(titulo, loc = "left", fontdict = {'fontsize':14, 'fontweight':'bold', 'color':'tab:blue'})
    
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

def estadistica_grafico_10_conceptos(data):
    
    colores = plt.cm.tab10.colors
    horizontal=data['SumaMonto'].tolist()
    vertical=data['NombreGasto'].tolist()
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(vertical,horizontal, color=colores )
    ax.grid(axis = 'x', color = 'gray', linestyle = 'dashed')
    ax.get_xaxis().set_major_formatter(FuncFormatter(format_with_commas))
    plt.yticks(fontsize=8)
    plt.xticks(fontsize=8)
    plt.subplots_adjust(bottom=0.2)
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    imagen_10conceptos_bytes = buffer.getvalue()
    
    imagen_10conceptos_b64 = base64.b64encode(imagen_10conceptos_bytes).decode('utf-8')
    plt.close('all')
    return imagen_10conceptos_b64

def estadistica_grafico_por_categoria(data):
    
    horizontal=data['CategoriaGasto'].tolist()
    vertical=data['SumaMonto'].tolist()
    num_barras = len(horizontal)
    print('numero de barras')
    print(num_barras)
    # colores_rgba = [colors.to_rgba(np.random.rand(), alpha=0.7) for _ in range(num_barras)]
    # colores_rgba = [colors.to_rgba(np.random.rand(), alpha=0.7) for _ in range(num_barras)]
    # colores_rgba = [to_rgba(np.random.rand(), np.random.rand(), np.random.rand()) for _ in range(len(horizontal))]
    # colores_rgba = [to_rgba(np.random.rand()) for _ in range(len(horizontal))]
    # colores_rgba = [to_rgba(np.random.rand(), alpha=1.0) for _ in range(len(horizontal))]
    colores_hex = ['#%06x' % np.random.randint(0, 0xFFFFFF) for _ in range(len(horizontal))]
    fig, ax = plt.subplots(figsize=(10, 6.5))
    ax.bar(horizontal,vertical,color=colores_hex)
    ax.grid(axis = 'y', color = 'gray', linestyle = 'dashed')
    ax.get_yaxis().set_major_formatter(FuncFormatter(format_with_commas))
    plt.yticks(fontsize=8)
    plt.xticks(fontsize=8)
    ax.set_xticklabels(horizontal, rotation=30, ha='right')
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    imagen_porcategoria_bytes = buffer.getvalue()
    
    imagen_porcategoria_b64 = base64.b64encode(imagen_porcategoria_bytes).decode('utf-8')
    plt.close('all')
    return imagen_porcategoria_b64
   