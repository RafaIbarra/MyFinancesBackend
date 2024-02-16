from django.db.models import Q
import pandas as pd
from  Conexion.models import Egresos, Ingresos
from Conexion.Serializers import EgresosSerializers,IngresosSerializers,BalanceSerializers


def detalle_ingresos(user,anno,mes):
    condicion1 = Q(user_id__exact=user)
    condicion2 = Q(fecha_ingreso__year=anno)
    condicion3 = Q(fecha_ingreso__month=mes)
    lista=Ingresos.objects.filter(condicion1 & condicion2 & condicion3)

    if lista:
       return lista
            
    else:
        return []

def detalle_egresos(user,anno,mes):
    condicion1 = Q(user_id__exact=user)
    condicion2 = Q(fecha_gasto__year=anno)
    condicion3 = Q(fecha_gasto__month=mes)
    lista=Egresos.objects.filter(condicion1 & condicion2 & condicion3)
            
    if lista:
        return lista
            
    else:
        []

def datos_balance(user,anno,mes):
    egresos=detalle_egresos(user,anno,mes)
    ingresos=detalle_ingresos(user,anno,mes)

    if egresos and ingresos:
            
        df_egresos = pd.DataFrame(EgresosSerializers(egresos, many=True).data)
        df_ingresos = pd.DataFrame(IngresosSerializers(ingresos, many=True).data)
        
    
        df_egresos_agrupado = df_egresos.groupby(['NombreGasto','TipoGasto'])['monto_gasto'].sum().reset_index()
        
        
        df_ingresos_agrupado = df_ingresos.groupby(['NombreIngreso','TipoIngreso'])['monto_ingreso'].sum().reset_index()
        
        df_egresos_agrupado['Codigo'] = 2
        df_egresos_agrupado = df_egresos_agrupado.rename(columns={'NombreGasto': 'Descripcion', 'TipoGasto': 'Tipo', 'monto_gasto': 'MontoEgreso'})
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
            
            

        return[]
    else:
        return[]