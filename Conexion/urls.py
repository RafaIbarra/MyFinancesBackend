from django.urls import path
from Conexion.Apis.api_registros_basicos import *
from Conexion.Apis.api_registros_movimientos import *
from Conexion.Estaditicas.estadisticas import balance
urlpatterns = [
    path('RegistroGasto/',registrogasto,name='registrogasto'),
    path('MisGastos/',misgastos,name='misgastos'),
    path('RegistroEgreso/',registroegreso,name='registroegreso'),
    path('MisEgresos/<int:anno>/<int:mes>/',misegresos,name='misegresos'),

    path('RegistroProductoFinanciero/',registroproductofinanciero,name='registroproductofinanciero'),
    path('MisProductosFinancieros/',misproductosfinancieros,name='misproductosfinancieros'),
    path('RegistroIngreso/',registroingreso,name='registroingreso'),
    path('MisIngresos/<int:anno>/<int:mes>/',misingresos,name='misingresos'),
    path('Balance/<int:anno>/<int:mes>/',balance,name='balance'),


]