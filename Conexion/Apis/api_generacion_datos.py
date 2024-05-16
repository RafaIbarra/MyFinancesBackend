from django.db.models import Q
import pandas as pd
from  Conexion.models import Egresos, Ingresos
from Conexion.Serializadores.EgresosSerializers import *
from Conexion.Serializadores.IngresosSerializers import *
from Conexion.Serializadores.BalanceSerializers import *
from Conexion.Serializadores.ResumenSerializers import *
from Conexion.Serializadores.SaldosPeriodoSerializers import *
from django.utils import timezone
from datetime import datetime
import pandas as pd

from Conexion.Apis.Operaciones.api_generacion_graficos import *
def registros_ingresos(user,anno,mes):
    
    if anno>0:
        condicion1 = Q(user_id__exact=user)
        condicion2 = Q(fecha_ingreso__year=anno)
        if mes>0:
            condicion3 = Q(fecha_ingreso__month=mes)
            lista=Ingresos.objects.filter(condicion1 & condicion2 & condicion3)
        else:
            
            lista=Ingresos.objects.filter(condicion1 & condicion2 )
    else:
        condicion1 = Q(user_id__exact=user)
        lista=Ingresos.objects.filter(condicion1 )
    
    
    if lista:
       return lista
            
    else:
        return []
    
def agrupar_periodos_ingresos(data):
    
    df_data=pd.DataFrame(data)
    
    df_data_agrupado = df_data.groupby(['AnnoIngreso', 'MesIngreso','NombreMesIngreso']).agg({'monto_ingreso': ['sum', 'count']})
    df_data_agrupado.columns = ['SumaMonto', 'ConteoRegistros']
    df_data_agrupado = df_data_agrupado.reset_index()
    df_zip=zip(df_data_agrupado['AnnoIngreso'].tolist() , df_data_agrupado['MesIngreso'].tolist(), df_data_agrupado['NombreMesIngreso'].tolist(),
                        df_data_agrupado['SumaMonto'].tolist() , df_data_agrupado['ConteoRegistros'].tolist())
    
    df_dict = [{'AnnoIngreso': anno, 'MesIngreso': mes,'NombreMesIngreso':nom_mes, 'SumaMonto': suma_monto, 'ConteoRegistros': conteo}
                for anno, mes,nom_mes, suma_monto, conteo in df_zip]
    
    
    return df_dict

def agrupar_periodos_egresos(data):
    
    df_data=pd.DataFrame(data)
    
    df_data_agrupado = df_data.groupby(['AnnoEgreso', 'MesEgreso','NombreMesEgreso']).agg({'monto_gasto': ['sum', 'count']})
    df_data_agrupado.columns = ['SumaMonto', 'ConteoRegistros']
    df_data_agrupado = df_data_agrupado.reset_index()
    df_zip=zip(df_data_agrupado['AnnoEgreso'].tolist() , df_data_agrupado['MesEgreso'].tolist(), df_data_agrupado['NombreMesEgreso'].tolist(),
                        df_data_agrupado['SumaMonto'].tolist() , df_data_agrupado['ConteoRegistros'].tolist())
    
    df_dict = [{'AnnoEgreso': anno, 'MesEgreso': mes,'NombreMesEgreso':nom_mes, 'SumaMonto': suma_monto, 'ConteoRegistros': conteo}
                for anno, mes,nom_mes, suma_monto, conteo in df_zip]
    
    
    return df_dict


def registros_egresos(user,anno,mes):
    if anno >0:
        condicion1 = Q(user_id__exact=user)
        condicion2 = Q(fecha_gasto__year=anno)
        if mes>0:
            condicion3 = Q(fecha_gasto__month=mes)
            lista=Egresos.objects.filter(condicion1 & condicion2 & condicion3)
        else:
            lista=Egresos.objects.filter(condicion1 & condicion2)
    else:
        condicion1 = Q(user_id__exact=user)
        lista=Egresos.objects.filter(condicion1 )
            
    if lista:
        return lista
            
    else:
        []

def datos_ingresos(user,anno,mes):
    lista = registros_ingresos(user,anno,mes)
    if lista:
        result_serializer=IngresosSerializers(lista,many=True)
        if result_serializer.data:
            return result_serializer.data
    else:
        return []
    
def datos_egresos(user,anno,mes):
    
    lista = registros_egresos(user,anno,mes)
    
    
    if lista:
        result_serializer=EgresosSerializers(lista,many=True)
        if result_serializer.data:
            return result_serializer.data
    else:
        
        return []




def datos_balance(user,anno,mes):
    egresos=registros_egresos(user,anno,mes)
    ingresos=registros_ingresos(user,anno,mes)
    if egresos:
        df_egresos = pd.DataFrame(EgresosSerializers(egresos, many=True).data)
        
        
    else:
         
        empytegresos=[{
             'id':0,
             'gasto':0,
             'NombreGasto':'SNG',
             'TipoGasto':'SNG',
             'CategoriaGasto':'SNG',
             'monto_gasto':0,
             'user':1,
             'fecha_gasto':datetime.now(),
             'anotacion':'',
             'fecha_registro':datetime.now(),
         }]

        df_egresos = pd.DataFrame(empytegresos)


    df_egresos_agrupado = df_egresos.groupby(['NombreGasto','TipoGasto'])['monto_gasto'].sum().reset_index()
    df_egresos_agrupado['Codigo'] = 2
    df_egresos_agrupado = df_egresos_agrupado.rename(columns={'NombreGasto': 'Descripcion', 'TipoGasto': 'Tipo', 'monto_gasto': 'MontoEgreso'})

    if ingresos:
        
        df_ingresos = pd.DataFrame(IngresosSerializers(ingresos, many=True).data)

    else:
        
        emptyingresos=[{'id': 0, 'producto_financiero': 0, 'NombreIngreso':'SN','TipoIngreso':'SN',
                        'monto_ingreso': 0, 'user': 1, 'fecha_ingreso':datetime.now() , 'anotacion': '', 'fecha_registro': datetime.now()
                        }]
        df_ingresos = pd.DataFrame(emptyingresos)


    df_ingresos_agrupado = df_ingresos.groupby(['NombreIngreso','TipoIngreso'])['monto_ingreso'].sum().reset_index()
    df_ingresos_agrupado['Codigo'] = 1
    df_ingresos_agrupado = df_ingresos_agrupado.rename(columns={'NombreIngreso': 'Descripcion', 'TipoIngreso': 'Tipo', 'monto_ingreso': 'MontoIngreso'})        

    df_final = pd.merge(df_ingresos_agrupado,df_egresos_agrupado,  on=['Codigo','Descripcion', 'Tipo'], how='outer', suffixes=('_Ingreso','_Egreso' ))
    df_final = df_final.fillna(0)
    
    sumaingresos=df_final['MontoIngreso'].sum()
    sumaegresos=df_final['MontoEgreso'].sum()
    saldo=sumaingresos- sumaegresos
    
    list_saldos={'Codigo':3,'Descripcion':'Totales','Tipo':'Resumen','MontoIngreso':sumaingresos,'MontoEgreso':sumaegresos}
    df_final = df_final.sort_values(by='MontoIngreso',ascending=False) 
    
    
    df_saldos = pd.DataFrame([list_saldos])
    df_result_final = pd.concat([df_final, df_saldos], ignore_index=True, sort=False)
    df_result_final = df_result_final.fillna(0)
    df_result_final['Saldo']=saldo
    
    data_list = df_result_final.to_dict(orient='records')
    
    resultado=BalanceSerializers(data=data_list,many=True)

    
    if  resultado.is_valid():
        
        return(resultado.data)
            
            

        
    else:
        return[]
    

def datos_saldos_periodos(user,anno):
    data_egresos = datos_egresos(user,anno,0)
    data_ingresos=datos_ingresos(user,anno,0)

    if data_ingresos and data_egresos:
        

        df_data_egresos=pd.DataFrame(data_egresos)
        df_data_egresos['Periodo']=df_data_egresos['NombreMesEgreso'] + '-' + df_data_egresos['AnnoEgreso'].astype(str)
        df_data_egresos=df_data_egresos.reset_index()

        df_data_egreso_agrupado = df_data_egresos.groupby(['AnnoEgreso', 'MesEgreso','NombreMesEgreso','Periodo']).agg({'monto_gasto': ['sum']})
        df_data_egreso_agrupado.columns = ['TotalEgreso']
        df_data_egreso_agrupado = df_data_egreso_agrupado.sort_values(by=['AnnoEgreso', 'MesEgreso'], ascending=[True, True])
        df_data_egreso_agrupado = df_data_egreso_agrupado.reset_index()


        df_data_ingresos=pd.DataFrame(data_ingresos)
        df_data_ingresos['Periodo']=df_data_ingresos['NombreMesIngreso'] + '-' + df_data_ingresos['AnnoIngreso'].astype(str)
        df_data_ingresos=df_data_ingresos.reset_index()

        df_data_ingresos_agrupado = df_data_ingresos.groupby(['AnnoIngreso', 'MesIngreso','NombreMesIngreso','Periodo']).agg({'monto_ingreso': ['sum']})
        df_data_ingresos_agrupado.columns = ['TotalIngreso']
        df_data_ingresos_agrupado = df_data_ingresos_agrupado.sort_values(by=['AnnoIngreso', 'MesIngreso'], ascending=[True, True])
        df_data_ingresos_agrupado = df_data_ingresos_agrupado.reset_index()

        df_resultado = pd.merge(df_data_ingresos_agrupado, df_data_egreso_agrupado, on='Periodo', how='inner')
        df_resultado=df_resultado.rename(columns={'AnnoIngreso':'AnnoOperacion','MesIngreso':'MesOperacion', 'NombreMesIngreso':'NombreMesOperacion'})
        columns_to_drop = ['AnnoEgreso', 'MesEgreso','NombreMesEgreso','MesOperacion']
        df_resultado = df_resultado.drop(columns=columns_to_drop)

        df_resultado['Saldo']=df_resultado['TotalIngreso'] - df_resultado['TotalEgreso']
        df_resultado['PorcentajeEgreso']= round( df_resultado['TotalEgreso']/df_resultado['TotalIngreso'] * 100 , 2)
        df_resultado['PorcentajeSaldo']=round(df_resultado['Saldo'] / df_resultado['TotalIngreso'] * 100 , 2)
        
        data_list = df_resultado.to_dict(orient='records')
    
        resultado=SaldosPeriodoSerializers(data=data_list,many=True)    
       
        if  resultado.is_valid():
            return(resultado.data)
        return[]
    else:
        return[]
    
def datos_resumen(user,anno,mes):
    
    
    egresos=datos_egresos(user,anno,mes)
    ingresos=datos_ingresos(user,anno,mes)
    balance=datos_balance(user,anno,mes)

    saldosperiodo=datos_saldos_periodos(user,anno)
    
    resumen_data={
                    'Resumen':balance,
                    'Ingresos':ingresos,
                    'Egresos':egresos,
                    'Saldos':saldosperiodo
                }
    r_final = ResumenSerializers(resumen_data)
    if r_final.data:
        # imagen_resumen=generar_graf_torta_resumen(ingresos,egresos)
        # imagen_egresos=generar_graf_torta_egresos(user,anno,mes)
        # imagen_ingresos=generar_graf_torta_ingresos(user,anno,mes)
        return{
            'datos':r_final.data,
            # 'graficos':{
            #     'imgResumen':imagen_resumen,
            #     'imgEgresos':imagen_egresos,
            #     'imgIngresos':imagen_ingresos,
            # }

        } 
    else:
        return []
    
def imagenes_mes(user,anno,mes):
    
    egresos=datos_egresos(user,anno,mes)
    ingresos=datos_ingresos(user,anno,mes)
    
    imagen_resumen=generar_graf_torta_resumen(ingresos,egresos)
    imagen_egresos=generar_graf_torta_egresos(user,anno,mes)
    imagen_ingresos=generar_graf_torta_ingresos(user,anno,mes)
    data_imagenes=[]
    data_imagenes.append({'imgResumen':imagen_resumen,
                          'imgEgresos':imagen_egresos,
                          'imgIngresos':imagen_ingresos,
                          })
    return data_imagenes


def datos_resumen_movile(user,anno,mes):

    balance=datos_balance(user,anno,mes)
    registros_con_codigo_menor_a_3 = [registro for registro in balance if registro['Codigo'] < 3]
    
    if balance:
        # imagen_resumen=generar_graf_torta_resumen(ingresos,egresos)
        # imagen_egresos=generar_graf_torta_egresos(user,anno,mes)
        # imagen_ingresos=generar_graf_torta_ingresos(user,anno,mes)
        return registros_con_codigo_menor_a_3
            
        
    else:
        return []
    

def movile_imagenes_mes_saldo(user,anno,mes):
    
    egresos=datos_egresos(user,anno,mes)
    ingresos=datos_ingresos(user,anno,mes)
    
    imagen_resumen=generar_graf_torta_resumen(ingresos,egresos)
    
    data_imagenes=[]
    data_imagenes.append({'imgResumen':imagen_resumen})
    return data_imagenes


def movile_imagenes_mes_ingreso(user,anno,mes):
    
    
    imagen_ingresos=generar_graf_torta_ingresos(user,anno,mes)
    data_imagenes=[]
    data_imagenes.append({
                          'imgIngresos':imagen_ingresos,
                          })
    return data_imagenes

def movile_imagenes_mes_egreso(user,anno,mes):
    
   
    imagen_egresos=generar_graf_torta_egresos(user,anno,mes)
    data_imagenes=[]
    data_imagenes.append({
                          'imgEgresos':imagen_egresos,
                          })
    return data_imagenes

    




