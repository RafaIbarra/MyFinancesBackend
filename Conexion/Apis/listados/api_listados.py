from django.db.models import Q


from rest_framework.response import Response
from rest_framework import status  
from rest_framework.decorators import api_view
import pandas as pd


from Conexion.obtener_datos_token import obtener_datos_token
from Conexion.validaciones import validacionpeticion

from Conexion.models import Egresos, Ingresos
from Conexion.Serializers import EgresosSerializers, IngresosSerializers,BalanceSerializers,ResumenSerializers
from Conexion.Apis.listados.datos import detalle_egresos,detalle_ingresos

@api_view(['POST'])
def resumen(request,anno,mes):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True: 
        # Obtener datos de la base de datos
        
        
        egresos=detalle_egresos(id_user,anno,mes)
        
        ingresos=detalle_ingresos(id_user,anno,mes)
        
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
            

            ingresos_serializer=IngresosSerializers(ingresos,many=True)
            
            egresos_serializer=EgresosSerializers(egresos,many=True)
            
            if ingresos_serializer.data and egresos_serializer.data and resultado.is_valid():
                
                resumen_data={
                    'Resumen':resultado.validated_data,
                    'Ingresos':ingresos_serializer.data,
                    'Egresos':egresos_serializer.data
                }
                
                r_final = ResumenSerializers(resumen_data)
                if r_final.data:
                    return Response(r_final.data, status=status.HTTP_200_OK)
                
                return Response({'message':r_final.errors},status= status.HTTP_400_BAD_REQUEST)

            return Response({'message':ingresos_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
        else:
            return Response([],status= status.HTTP_200_OK)
        
    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)