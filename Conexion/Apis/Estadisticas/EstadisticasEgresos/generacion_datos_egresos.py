from django.db.models import Q
import pandas as pd
import numpy as np

from  Conexion.models import Egresos, Ingresos
from Conexion.Apis.api_generacion_datos import datos_egresos

def estadistica_egresos_periodo(id_user,anno,mes):
    data_egresos = datos_egresos(id_user,anno,mes)
    if data_egresos:
        df_data_egresos=pd.DataFrame(data_egresos)
        df_data_egresos['Periodo']=df_data_egresos['NombreMesEgreso'] + '-' + df_data_egresos['AnnoEgreso'].astype(str)
        df_data_egresos=df_data_egresos.reset_index()
        ###### por periodos ########
        df_data_agrupado = df_data_egresos.groupby(['AnnoEgreso', 'MesEgreso','NombreMesEgreso','Periodo']).agg({'monto_gasto': ['sum', 'count']})
        df_data_agrupado.columns = ['SumaMonto', 'CantidadRegistros']
        df_data_agrupado = df_data_agrupado.reset_index()
        fila_periodo_maximo = df_data_agrupado.loc[df_data_agrupado['SumaMonto'].idxmax()]
        resultado_concepto_maximo = [{'Periodo': fila_periodo_maximo['Periodo']}, {'SumaMonto': fila_periodo_maximo['SumaMonto']}, {'CantidadRegistros': fila_periodo_maximo['CantidadRegistros']}]
        promedio_periodo = df_data_agrupado['SumaMonto'].mean()

        result=[
            {'DatosMaximoGasto':resultado_concepto_maximo},
            {'PromedioGasto':promedio_periodo},
        ]
        # print(df_data_agrupado)
        # print(resultado_concepto_maximo)
        # print(promedio_periodo)
        return result
    else:
        return []
    
def estadistica_egresos_conceptos(id_user,anno,mes):
    data_egresos = datos_egresos(id_user,anno,mes)
    if data_egresos:
        
        df_data_egresos=pd.DataFrame(data_egresos)
        df_data_egresos['Periodo']=df_data_egresos['NombreMesEgreso'] + '-' + df_data_egresos['AnnoEgreso'].astype(str)
        df_data_egresos=df_data_egresos.reset_index()
        

        df_data_agrupado_conceptos = df_data_egresos.groupby(['NombreGasto']).agg({'monto_gasto': ['sum', 'count']})
        df_data_agrupado_conceptos.columns = ['SumaMonto', 'CantidadRegistros']
        df_data_agrupado_conceptos = df_data_agrupado_conceptos.reset_index()
        

        concepto_maximo = df_data_agrupado_conceptos.loc[df_data_agrupado_conceptos['SumaMonto'].idxmax()]
        resultado_concepto_maximo = [{'Concepto': concepto_maximo['NombreGasto']}, {'Monto': concepto_maximo['SumaMonto']}, {'cantidad': concepto_maximo['CantidadRegistros']}]

        nombre_concepto_maximo=resultado_concepto_maximo[0]['Concepto']
        detalle_concepto_maximo=df_data_egresos.loc[df_data_egresos['NombreGasto'] == nombre_concepto_maximo]
        periodo_concepto_maximo=detalle_concepto_maximo.loc[detalle_concepto_maximo['monto_gasto'].idxmax()]
        resultado_detalle_concepto_maximo = [{'Monto': periodo_concepto_maximo['monto_gasto']}, {'Periodo': periodo_concepto_maximo['Periodo']}, 
                                                {'fecha_gasto': periodo_concepto_maximo['fecha_gasto']}, {'fecha_registro': periodo_concepto_maximo['fecha_registro']}]
        
        promedio_concepto_periodo = detalle_concepto_maximo['monto_gasto'].mean()
        result=[
            {'DatosConceptoGastoMaximo':resultado_concepto_maximo},
            {'DetalleConceptoGastoMaximo':resultado_detalle_concepto_maximo},
            {'PromedioGastoConcepto':promedio_concepto_periodo},

        ]

        return result

    else:
        return []
    
def estadistica_egresos_categoria(id_user,anno,mes):
    data_egresos = datos_egresos(id_user,anno,mes)
    if data_egresos:
        
        df_data_egresos=pd.DataFrame(data_egresos)
        df_data_egresos['Periodo']=df_data_egresos['NombreMesEgreso'] + '-' + df_data_egresos['AnnoEgreso'].astype(str)
        df_data_egresos=df_data_egresos.reset_index()
        
        # print(df_data_egresos)
        df_data_agrupado_categoria = df_data_egresos.groupby(['CategoriaGasto']).agg({'monto_gasto': ['sum', 'count']})
        df_data_agrupado_categoria.columns = ['SumaMonto', 'CantidadRegistros']
        df_data_agrupado_categoria = df_data_agrupado_categoria.reset_index()
        # print(df_data_agrupado_categoria)

        categoria_maxima = df_data_agrupado_categoria.loc[df_data_agrupado_categoria['SumaMonto'].idxmax()]
        resultado_categoria_maxima = [{'Categotia': categoria_maxima['CategoriaGasto']}, {'Monto': categoria_maxima['SumaMonto']}, {'cantidad': categoria_maxima['CantidadRegistros']}]

        nombre_categoria_maximo=resultado_categoria_maxima[0]['Categotia']
        detalle_categoria_maxima=df_data_egresos.loc[df_data_egresos['CategoriaGasto'] == nombre_categoria_maximo]
        periodo_categoria_maximo=detalle_categoria_maxima.loc[detalle_categoria_maxima['monto_gasto'].idxmax()]
        resultado_detalle_categoria_maxima = [{'Monto': periodo_categoria_maximo['monto_gasto']}, {'Periodo': periodo_categoria_maximo['Periodo']}, 
                                                {'fecha_gasto': periodo_categoria_maximo['fecha_gasto']}, {'fecha_registro': periodo_categoria_maximo['fecha_registro']}]
        
        promedio_categoria_periodo = detalle_categoria_maxima['monto_gasto'].mean()
        result=[
            {'DatosCategoriaGastoMaximo':resultado_categoria_maxima},
            {'DetalleCategoriaGastoMaximo':resultado_detalle_categoria_maxima},
            {'PromedioGastoCategoria':promedio_categoria_periodo},

        ]

        return result

    else:
        return []
        
        