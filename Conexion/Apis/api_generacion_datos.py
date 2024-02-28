from django.db.models import Q
import pandas as pd
from  Conexion.models import Egresos, Ingresos
# from Conexion.Serializers import EgresosSerializers,IngresosSerializers,BalanceSerializers,ResumenSerializers
from Conexion.Serializadores.EgresosSerializers import *
from Conexion.Serializadores.IngresosSerializers import *
from Conexion.Serializadores.BalanceSerializers import *
from Conexion.Serializadores.ResumenSerializers import *
from django.utils import timezone
from datetime import datetime
import pandas as pd
from Conexion.Apis.Graficos.api_generacion_graficos import *

def registros_ingresos(user,anno,mes):
    
    if anno>0:
        condicion1 = Q(user_id__exact=user)
        condicion2 = Q(fecha_ingreso__year=anno)
        condicion3 = Q(fecha_ingreso__month=mes)
        lista=Ingresos.objects.filter(condicion1 & condicion2 & condicion3)
    else:
        condicion1 = Q(user_id__exact=user)
        lista=Ingresos.objects.filter(condicion1 )
    
    
    if lista:
       return lista
            
    else:
        return []
    
def agrupar_periodos_ingresos(data):
    
    df_data=pd.DataFrame(data)
    
    df_data_agrupado = df_data.groupby(['AnnoIngreso', 'MesIngreso']).agg({'monto_ingreso': ['sum', 'count']})
    df_data_agrupado.columns = ['SumaMonto', 'ConteoRegistros']
    df_data_agrupado = df_data_agrupado.reset_index()
    df_zip=zip(df_data_agrupado['AnnoIngreso'].tolist() , df_data_agrupado['MesIngreso'].tolist(),
                        df_data_agrupado['SumaMonto'].tolist() , df_data_agrupado['ConteoRegistros'].tolist())
    
    df_dict = [{'AnnoIngreso': anno, 'MesIngreso': mes, 'SumaMonto': suma_monto, 'ConteoRegistros': conteo}
                for anno, mes, suma_monto, conteo in df_zip]
    
    
    return df_dict

def registros_egresos(user,anno,mes):
    condicion1 = Q(user_id__exact=user)
    condicion2 = Q(fecha_gasto__year=anno)
    condicion3 = Q(fecha_gasto__month=mes)
    lista=Egresos.objects.filter(condicion1 & condicion2 & condicion3)
            
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

    # if egresos and ingresos:
        

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
            
            

        return[]
    else:
        return[]
    
def datos_resumen(user,anno,mes):
    egresos=datos_egresos(user,anno,mes)
    
    ingresos=datos_ingresos(user,anno,mes)
    

    balance=datos_balance(user,anno,mes)
    resumen_data={
                    'Resumen':balance,
                    'Ingresos':ingresos,
                    'Egresos':egresos
                }
    r_final = ResumenSerializers(resumen_data)
    if r_final.data:
        imagen_resumen=generar_graf_barra_resumen(user,anno,mes)
        imagen_egresos=generar_graf_torta_egresos(user,anno,mes)
        imagen_ingresos=generar_graf_torta_ingresos(user,anno,mes)
        return{
            'datos':r_final.data,
            'graficos':{
                'imgResumen':imagen_resumen,
                'imgEgresos':imagen_egresos,
                'imgIngresos':imagen_ingresos,
            }

        } 
    else:
        return []