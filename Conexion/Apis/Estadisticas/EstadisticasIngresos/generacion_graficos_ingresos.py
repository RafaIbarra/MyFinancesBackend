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


def grafico_saldos_periodos(data):

    horizontal=data['NombreMesOperacion'].tolist()
    vertical1=data['SumaMontoIngreso'].tolist()
    vertical2=data['SumaMontoEgreso'].tolist()
    saldos=data['Saldo'].tolist()
    num_barras = len(horizontal)

    color_verde_transparente = to_rgba('blue', alpha=0.2)

    # barra agrupadas
    fig, ax = plt.subplots(figsize=(10, 6.5))

    
    bar_width = 0.4
    bar_positions = range(len(data))
    plt.bar(bar_positions, data['SumaMontoIngreso'], width=bar_width, label='Ingreso',color='green')
    plt.bar([p + bar_width for p in bar_positions], data['SumaMontoEgreso'], width=bar_width, label='Egreso',color='red')
    plt.bar([p + bar_width for p in bar_positions], data['Saldo'], width=bar_width, label='Saldo',color=color_verde_transparente, bottom=data['SumaMontoEgreso'])
    ax.set_xticks([p + bar_width / 2 for p in bar_positions])


    ax.get_yaxis().set_major_formatter(FuncFormatter(format_with_commas))

    # ax.set_xticks([p for p in bar_positions])
    ax.set_xticklabels(horizontal)
    ax.grid(axis = 'y', color = 'gray', linestyle = 'dashed')
    ax.set_xlabel('Periodo')
    ax.set_ylabel('Montos')
    ax.set_title('Ingresos y Egresos por Periodo')
    plt.yticks(fontsize=8)
    plt.xticks(fontsize=9)
    ax.legend()
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    imagen_saldo_periodo_bytes = buffer.getvalue()
    
    imagen_saldo_periodo_b64 = base64.b64encode(imagen_saldo_periodo_bytes).decode('utf-8')
    plt.close('all')
    return imagen_saldo_periodo_b64