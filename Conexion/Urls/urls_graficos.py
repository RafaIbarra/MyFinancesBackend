from django.urls import path
from Conexion.Apis.Graficos.api_graficos import *

urlpatterns = [
    path('GraficoBalance/<int:anno>/<int:mes>/',graf_barra_resumen,name='graf_barra_resumen'),
    path('GraficoEgresos/<int:anno>/<int:mes>/',graf_torta_egresos,name='graf_torta_egresos'),
    path('GraficoIngresos/<int:anno>/<int:mes>/',graf_torta_ingresos,name='graf_torta_ingresos'),
]