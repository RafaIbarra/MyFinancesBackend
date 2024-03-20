from django.db.models import Q
import pandas as pd
import numpy as np

from  Conexion.models import CategoriaGastos
from Conexion.Apis.api_generacion_datos import datos_egresos
from Conexion.Apis.Estadisticas.EstadisticasEgresos.generacion_graficos import *
def estadistica_egresos_periodo(id_user,anno,mes):
    data_egresos = datos_egresos(id_user,anno,mes)
    if data_egresos:
        df_data_egresos=pd.DataFrame(data_egresos)
        df_data_egresos['Periodo']=df_data_egresos['NombreMesEgreso'] + '-' + df_data_egresos['AnnoEgreso'].astype(str)
        df_data_egresos=df_data_egresos.reset_index()
        ###### por periodos ########
        df_data_agrupado = df_data_egresos.groupby(['AnnoEgreso', 'MesEgreso','NombreMesEgreso','Periodo']).agg({'monto_gasto': ['sum', 'count']})
        
        df_data_agrupado.columns = ['SumaMonto', 'CantidadRegistros']
        df_data_agrupado = df_data_agrupado.sort_values(by=['AnnoEgreso', 'MesEgreso'], ascending=[True, True])
        df_data_agrupado = df_data_agrupado.reset_index() # para el grafico
        cantidad_periodos=len(df_data_agrupado)
        fila_periodo_maximo = df_data_agrupado.loc[df_data_agrupado['SumaMonto'].idxmax()]
        
        promedio_periodo = df_data_agrupado['SumaMonto'].mean()
        titulo= 'GASTOS POR MESES DEL AÑO ' + str(anno)
        grafico_periodo=estadistica_grafico_linas(df_data_agrupado,titulo,promedio_periodo)
        
        resultado_concepto_maximo = [{'Periodo': fila_periodo_maximo['Periodo'],
                                      'SumaMonto': fila_periodo_maximo['SumaMonto'],
                                      'CantidadRegistros': fila_periodo_maximo['CantidadRegistros'],
                                      'PromedioGasto':promedio_periodo,
                                      'CantidadPeriodos':cantidad_periodos,
                                      'grafico':grafico_periodo

                                      }]
        result=[{'DatosMaximoGasto':resultado_concepto_maximo}]
        
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
        df_data_agrupado_conceptos = df_data_agrupado_conceptos.sort_values(by=['SumaMonto'], ascending=[False]).reset_index()
        
        df_10_maximos = df_data_agrupado_conceptos.head(10)
        imagen=estadistica_grafico_10_conceptos(df_10_maximos)
        concepto_maximo = df_data_agrupado_conceptos.loc[df_data_agrupado_conceptos['SumaMonto'].idxmax()]

        

        nombre_concepto_maximo= concepto_maximo['NombreGasto']
        detalle_concepto_maximo=df_data_egresos.loc[df_data_egresos['NombreGasto'] == nombre_concepto_maximo]
        periodo_concepto_maximo=detalle_concepto_maximo.loc[detalle_concepto_maximo['monto_gasto'].idxmax()]
        resultado_detalle_concepto_maximo = [{'Monto': periodo_concepto_maximo['monto_gasto'],
                                              'Periodo': periodo_concepto_maximo['Periodo'],
                                              'fecha_gasto': periodo_concepto_maximo['fecha_gasto'],
                                              'fecha_registro': periodo_concepto_maximo['fecha_registro']
                                              }]
        
        promedio_concepto_periodo = detalle_concepto_maximo['monto_gasto'].mean()
        resultado_concepto_maximo = [{'Concepto': concepto_maximo['NombreGasto'],
                                      'Monto': concepto_maximo['SumaMonto'],
                                      'cantidad': concepto_maximo['CantidadRegistros'],
                                      'Pomedio':promedio_concepto_periodo
                                      }]
        
        result=[
            {'DatosConceptoGastoMaximo':resultado_concepto_maximo},
            {'DetalleConceptoGastoMaximo':resultado_detalle_concepto_maximo},
            
            {'grafico':imagen},

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
        
        
        df_data_agrupado_categoria = df_data_egresos.groupby(['CategoriaGasto']).agg({'monto_gasto': ['sum', 'count']})
        df_data_agrupado_categoria.columns = ['SumaMonto', 'CantidadRegistros']
        df_data_agrupado_categoria = df_data_agrupado_categoria.reset_index()
        imagen=estadistica_grafico_por_categoria(df_data_agrupado_categoria)

        categoria_maxima = df_data_agrupado_categoria.loc[df_data_agrupado_categoria['SumaMonto'].idxmax()]
        nombre_categoria_maximo=categoria_maxima['CategoriaGasto']
        detalle_categoria_maxima=df_data_egresos.loc[df_data_egresos['CategoriaGasto'] == nombre_categoria_maximo]
        promedio_categoria_periodo = detalle_categoria_maxima['monto_gasto'].mean()
        

        resultado_categoria_maxima = [{'Categoria': categoria_maxima['CategoriaGasto'],
                                       'Monto': categoria_maxima['SumaMonto'],
                                       'cantidad': categoria_maxima['CantidadRegistros'],
                                       'promedio':promedio_categoria_periodo
                                       }, 
                                      
                                      ]
        
        periodo_categoria_maximo=detalle_categoria_maxima.loc[detalle_categoria_maxima['monto_gasto'].idxmax()]
        resultado_detalle_categoria_maxima = [{'Monto': periodo_categoria_maximo['monto_gasto'],
                                               'Periodo': periodo_categoria_maximo['Periodo'],
                                               'fecha_gasto': periodo_categoria_maximo['fecha_gasto'],
                                                'fecha_registro': periodo_categoria_maximo['fecha_registro']
                                                
                                               }
                                              ]
        
        
        result=[
            {'DatosCategoriaGastoMaximo':resultado_categoria_maxima},
            {'DetalleCategoriaGastoMaximo':resultado_detalle_categoria_maxima},
            {'grafico':imagen}

        ]

        return result

    else:
        return []

def estadistica_egresos_quince_dias(id_user,anno,mes):
    data_egresos = datos_egresos(id_user,anno,mes)
    if data_egresos:
        
        df_data_egresos=pd.DataFrame(data_egresos)
        df_data_egresos['Periodo']=df_data_egresos['NombreMesEgreso'] + '-' + df_data_egresos['AnnoEgreso'].astype(str)
        df_data_egresos=df_data_egresos.reset_index()
        df_data_egresos['fecha_gasto']=pd.to_datetime(df_data_egresos['fecha_gasto'])
        
        df_data_filtro=df_data_egresos[df_data_egresos['fecha_gasto'].dt.day<16]
        
        
        df_data_filtro_agrupado = df_data_filtro.groupby(['Periodo', 'CategoriaGasto','MesEgreso','AnnoEgreso'])['monto_gasto'].sum().reset_index()
        
        categoria_maxima_indices = df_data_filtro_agrupado.groupby(['Periodo','MesEgreso','AnnoEgreso'])['monto_gasto'].idxmax()
        categoria_maxima_perdiodo = df_data_filtro_agrupado.loc[categoria_maxima_indices]
        categoria_maxima_perdiodo = categoria_maxima_perdiodo.sort_values(by=['AnnoEgreso', 'MesEgreso'], ascending=[True, True]) # detalle por periodo de categorias con mas gastos
        
        cantidad_registros=categoria_maxima_perdiodo.shape[0]
        categoria_maxima_perdiodo_cantidades=categoria_maxima_perdiodo.groupby(['CategoriaGasto']).count().reset_index()
        categoria_maxima_perdiodo_cantidades.rename(columns={'monto_gasto': 'CantidadVeces'}, inplace=True)
        categoria_maxima_perdiodo_cantidades = categoria_maxima_perdiodo_cantidades.drop('Periodo', axis=1)
        categoria_maxima_perdiodo_cantidades['CantidadRegistros']=cantidad_registros
        categoria_maxima_perdiodo_cantidades['Porcentaje']=round(categoria_maxima_perdiodo_cantidades['CantidadVeces']/categoria_maxima_perdiodo_cantidades['CantidadRegistros']*100,2 )# datos para el grafico

        
        mayor_categoria=categoria_maxima_perdiodo_cantidades['CantidadVeces'].idxmax()
        datos_mayor_categoria=categoria_maxima_perdiodo_cantidades.loc[mayor_categoria]
        nombre_mayor_categoria=datos_mayor_categoria['CategoriaGasto']
        
        
        distribucion_mayor_categoria=df_data_filtro.loc[df_data_filtro['CategoriaGasto']==nombre_mayor_categoria]
        distribucion_mayor_categoria=distribucion_mayor_categoria.reset_index()
        monto_total_distribucion=distribucion_mayor_categoria['monto_gasto'].sum()
        
        distribucion_mayor_categoria_agrupada=distribucion_mayor_categoria.groupby(['NombreGasto', 'CategoriaGasto'])['monto_gasto'].sum().reset_index()
        distribucion_mayor_categoria_agrupada['MontoTotal']=monto_total_distribucion
        distribucion_mayor_categoria_agrupada['Porcentaje']=round(distribucion_mayor_categoria_agrupada['monto_gasto']/distribucion_mayor_categoria_agrupada['MontoTotal']*100,2)
        distribucion_mayores=distribucion_mayor_categoria_agrupada[distribucion_mayor_categoria_agrupada['Porcentaje']> 5.0]
        distribucion_menores=distribucion_mayor_categoria_agrupada[distribucion_mayor_categoria_agrupada['Porcentaje']<= 5.0]
        distribucion_menores_agrupado=distribucion_menores.groupby(['CategoriaGasto']).agg({'monto_gasto': ['sum', 'count']})
        distribucion_menores_agrupado.columns = ['MontoMenores', 'CantidadMenores']
        distribucion_menores_agrupado=distribucion_menores_agrupado.reset_index()
        

        result_distribucion=distribucion_mayores.reset_index()
        
        nueva_fila={'NombreGasto':'Otros ' + str(distribucion_menores_agrupado['CantidadMenores'].iloc[0])+' conceptos',
                    'CategoriaGasto':distribucion_menores_agrupado['CategoriaGasto'].iloc[0],
                    'monto_gasto':distribucion_menores_agrupado['MontoMenores'].iloc[0],
                    'MontoTotal':monto_total_distribucion,
                    'Porcentaje':round(distribucion_menores_agrupado['MontoMenores'].iloc[0] / monto_total_distribucion *100,2)
                    }
        
        
       
        result_distribucion.loc[len(result_distribucion)] = nueva_fila
        result_distribucion=result_distribucion.reset_index()
        
        result_mayor_categoria=[
            {
                'Categoria':datos_mayor_categoria['CategoriaGasto'],
                'CantidadVeces':datos_mayor_categoria['CantidadVeces'],
                'Porcentaje':datos_mayor_categoria['Porcentaje'],
                'CantidadRegistros':datos_mayor_categoria['CantidadRegistros'],
            }
        ] #Datos de la categoria que mas veces se gasto.
        
        result_detalle_periodo=[]
        for Periodo,CategoriaGasto, MesEgreso ,AnnoEgreso,monto_gasto in zip(categoria_maxima_perdiodo['Periodo'].tolist(),
                                                                            categoria_maxima_perdiodo['CategoriaGasto'].tolist(),
                                                                            categoria_maxima_perdiodo['MesEgreso'].tolist(),
                                                                            categoria_maxima_perdiodo['AnnoEgreso'].tolist(),
                                                                            categoria_maxima_perdiodo['monto_gasto'].tolist()
                                                                            ):
            result_detalle_periodo.append([
                {'Periodo':Periodo,'CategoriaGasto':CategoriaGasto,'MesEgreso':MesEgreso,'AnnoEgreso':AnnoEgreso,'monto_gasto':monto_gasto}
            ])

        valores=[]
        
        grafico_15dias=estadistica_grafico_15_dias(categoria_maxima_perdiodo_cantidades,result_distribucion)
        valores.append({'DatosMayoCategoria':result_mayor_categoria})
        valores.append({'DetallePeriodo':result_detalle_periodo})
        valores.append({'grafico':grafico_15dias})
        
       

        return valores

    else:
        return []
    
def estadistica_egresos_por_categoria(id_user,anno,mes):
    data_egresos = datos_egresos(id_user,anno,mes)
    if data_egresos:
        
        df_data_egresos=pd.DataFrame(data_egresos)
        df_data_egresos['Periodo']=df_data_egresos['NombreMesEgreso'] + '-' + df_data_egresos['AnnoEgreso'].astype(str)
        df_data_egresos=df_data_egresos.reset_index()
        
        resul_final=[]
        lista_categorias=CategoriaGastos.objects.values()
        for item in lista_categorias:
            
            categoria_act=item['nombre_categoria']
            df_data_egresos_categoria=df_data_egresos.loc[df_data_egresos['CategoriaGasto'] == categoria_act].reset_index()
            df_data_egresos_categoria_conceptos = df_data_egresos_categoria.groupby(['NombreGasto']).agg({'monto_gasto': ['sum', 'count']})
            df_data_egresos_categoria_conceptos.columns = ['SumaMonto', 'CantidadRegistros']
            df_data_egresos_categoria_conceptos = df_data_egresos_categoria_conceptos.reset_index()
            total_monto=df_data_egresos_categoria_conceptos['SumaMonto'].sum()
            total_cantidades=df_data_egresos_categoria_conceptos['CantidadRegistros'].sum()
            df_data_egresos_categoria_conceptos['TotalMontos']=total_monto
            df_data_egresos_categoria_conceptos['PorcentajeMontos']=round(df_data_egresos_categoria_conceptos['SumaMonto']/df_data_egresos_categoria_conceptos['TotalMontos']*100,2)

            df_data_egresos_categoria_conceptos['TotalCantidades']=total_cantidades
            df_data_egresos_categoria_conceptos['PorcentajeCantidades']=round(df_data_egresos_categoria_conceptos['CantidadRegistros']/df_data_egresos_categoria_conceptos['TotalCantidades']*100,2)

            
            
            ############################# Por Montos #######################
            concepto_maximo_montos = df_data_egresos_categoria_conceptos.loc[df_data_egresos_categoria_conceptos['SumaMonto'].idxmax()]
            result_montos = [   {'NombreGasto': concepto_maximo_montos['NombreGasto']},   
                                {'Monto': concepto_maximo_montos['SumaMonto']}, 
                                {'Porcentaje': concepto_maximo_montos['PorcentajeMontos']}, 
                                {'TotalMontos': concepto_maximo_montos['TotalMontos']}, 
                                ]
            
            ############################# Por Cantidades #######################
            concepto_maximo_cantidades = df_data_egresos_categoria_conceptos.loc[df_data_egresos_categoria_conceptos['CantidadRegistros'].idxmax()]
            
            result_cantidades = [   {'NombreGasto': concepto_maximo_cantidades['NombreGasto']},   
                                    {'Cantidad': concepto_maximo_cantidades['CantidadRegistros']}, 
                                    {'Porcentaje': concepto_maximo_cantidades['PorcentajeCantidades']}, 
                                    {'TotalCantidades': concepto_maximo_cantidades['TotalCantidades']}, 
                                ]
            result_concepto=[
                                {'Categoria': categoria_act,
                                'Datos': [
                                        {'DatosMontos': result_montos}, 
                                        {'DatosCantidades': result_cantidades},
                                    ]
                                }
                            ]
            resul_final.append(result_concepto)

        return resul_final
    else:
        return []
        