from django.urls import path

from Conexion.Apis.Listados.api_listados import resumen,balance,meses,misgastos,misegresos,misproductosfinancieros,misingresos
from Conexion.Apis.Estadisticas.api_estadisticas import *
urlpatterns = [

    path('Meses/',meses,name='meses'),
    path('MisGastos/',misgastos,name='misgastos'),
    path('MisEgresos/<int:anno>/<int:mes>/',misegresos,name='misegresos'),

    path('EstadisticasEgresos/<int:anno>/<int:mes>/',estadisticas_egresos,name='estadisticas_egresos'),


    path('MisProductosFinancieros/',misproductosfinancieros,name='misproductosfinancieros'),
    path('MisIngresos/<int:anno>/<int:mes>/',misingresos,name='misingresos'),

    path('Balance/<int:anno>/<int:mes>/',balance,name='balance'),
    path('Resumen/<int:anno>/<int:mes>/',resumen,name='resumen'),

]