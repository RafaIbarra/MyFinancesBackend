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
import seaborn as sns
from matplotlib.colors import to_rgba

def format_with_commas(value, pos):
    return '{:,}'.format(int(value))


def porcentaje_formatter(x, _):
   
    return f'{x:.000%}'



def grafico_saldos_periodos(data):

    horizontal=data['NombreMesOperacion'].tolist()
    vertical1=data['SumaMontoIngreso'].tolist()
    vertical2=data['SumaMontoEgreso'].tolist()
    
    saldos=data['Saldo'].tolist()
    num_barras = len(horizontal)
    

    color_verde_transparente = to_rgba('blue', alpha=0.2)

   
    fig, ax = plt.subplots(figsize=(12, 4.5))

    
    bar_width = 0.4
    bar_positions = range(len(data))
    plt.bar(bar_positions, data['SumaMontoIngreso'], width=bar_width, label='Ingreso',color='green')
    plt.bar([p + bar_width for p in bar_positions], data['SumaMontoEgreso'], width=bar_width, label='Egreso',color='red')
    plt.bar([p + bar_width for p in bar_positions], data['Saldo'], width=bar_width, label='Saldo',color=color_verde_transparente, bottom=data['SumaMontoEgreso'])
    ax.set_xticks([p + bar_width / 2 for p in bar_positions])


    ax.get_yaxis().set_major_formatter(FuncFormatter(format_with_commas))


    ax.set_xticklabels(horizontal)
    ax.grid(axis = 'y', color = 'gray', linestyle = 'dashed')
    ax.set_xlabel('MESES', fontdict = {'fontsize':9, 'fontweight':'bold', 'color':'tab:blue'})
    ax.set_ylabel('MONTOS INGRESOS', fontdict = {'fontsize':9, 'fontweight':'bold', 'color':'tab:blue'})
    ax.set_title('Ingresos y Egresos por Periodo', fontdict = {'fontsize':12, 'fontweight':'bold', 'color':'tab:blue'})
 
    ax.legend()
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    imagen_saldo_periodo_bytes = buffer.getvalue()
    
    imagen_saldo_periodo_b64 = base64.b64encode(imagen_saldo_periodo_bytes).decode('utf-8')
    plt.close('all')
    return imagen_saldo_periodo_b64


def grafico_indice_saldo(data,titulo,promedio_periodo):
    
    periodos=data['NombreMesOperacion'].to_list()
    montos=data['PorcentajeSaldo'].to_list()
    tamañoperiodos=len(periodos)
    fig, ax = plt.subplots(figsize=(12, 4.5))
    
    ax.plot(periodos, montos, color = 'tab:purple', marker = 'o')
   
    desplazamiento = 0.1
    for i, valor in enumerate(montos):
        plt.text(i, valor + desplazamiento, f'{valor}%', ha='left', va='bottom', fontsize=9)

    ax.axhline(y=promedio_periodo, color='r', linestyle='-',label='Promedio')
    ax.legend()

   
    ax.set_xlabel("MESES", fontdict = {'fontsize':9, 'fontweight':'bold', 'color':'tab:blue'})
    ax.set_ylabel("PORCENTAJE SALDOS", fontdict = {'fontsize':9, 'fontweight':'bold', 'color':'tab:blue'})
    
    
    ax.set_title(titulo, loc = "center", fontdict = {'fontsize':12, 'fontweight':'bold', 'color':'tab:blue'})
    
    ax.legend()
    
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    imagen_grafico_lineas_bytes = buffer.getvalue()
    imagen_grafico_lineas_b64 = base64.b64encode(imagen_grafico_lineas_bytes).decode('utf-8') 
    plt.close('all')
    return imagen_grafico_lineas_b64
    