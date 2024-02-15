from django.db.models import Q


import pandas as pd


from  Conexion.models import Egresos, Ingresos


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