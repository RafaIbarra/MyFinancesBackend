import pandas as pd
from Conexion.Apis.api_generacion_datos import datos_egresos,datos_ingresos
from Conexion.Apis.Estadisticas.EstadisticasIngresos.generacion_graficos_ingresos import *

def estadisticas_saldos_periodos(id_user,anno,mes):
    data_egresos = datos_egresos(id_user,anno,mes)
    data_ingresos=datos_ingresos(id_user,anno,mes)
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

        # categoria_maxima_perdiodo_cantidades['Porcentaje']=categoria_maxima_perdiodo_cantidades['CantidadVeces']/categoria_maxima_perdiodo_cantidades['CantidadRegistros']*100 # datos para el grafico
        mayor_saldo = df_resultado.loc[df_resultado['Saldo'].idxmax()]
        mayor_indice = df_resultado.loc[df_resultado['PorcentajeSaldo'].idxmax()]
        
        resultado_mayor_saldo = [{
                                    'MesOperacion': mayor_saldo['NombreMesOperacion'],
                                    'MontoIngreso': mayor_saldo['SumaMontoIngreso'],
                                    'MontoEgreso': mayor_saldo['SumaMontoEgreso'],
                                    'PorcentajeEgreso':mayor_saldo['PorcentajeEgreso'],
                                    'PorcentajeSaldo':mayor_saldo['PorcentajeSaldo'],
                                    'Periodo':mayor_saldo['Periodo']

                                    }, 
                                      
                                ]
        
        resultado_mayor_indice = [{
                                    'MesOperacion': mayor_indice['NombreMesOperacion'],
                                    'MontoIngreso': mayor_indice['SumaMontoIngreso'],
                                    'MontoEgreso': mayor_indice['SumaMontoEgreso'],
                                    'PorcentajeEgreso':mayor_indice['PorcentajeEgreso'],
                                    'PorcentajeSaldo':mayor_indice['PorcentajeSaldo'],
                                    'Periodo':mayor_indice['Periodo']

                                    }, 
                                      
                                ]
        
        imagen=grafico_saldos_periodos(df_resultado)
        result=[
            {'MayorSaldo':resultado_mayor_saldo},
            {'MayorIndice':resultado_mayor_indice},
            {'grafico':imagen},

        ]
        return result