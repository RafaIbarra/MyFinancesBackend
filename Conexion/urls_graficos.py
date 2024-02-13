from django.urls import path
from Conexion.Estaditicas.Graficos.api_graficos import *

urlpatterns = [
    path('GraficoBalance/<int:anno>/<int:mes>/',graf_balance,name='graf_balance'),
]