from django.urls import path
from Conexion.Apis.Operaciones.api_registros_basicos import *
from Conexion.Apis.Operaciones.api_registros_movimientos import *
urlpatterns = [



    path('RegistroGasto/',registrogasto,name='registrogasto'),
    path('EliminarGastos/',eliminargastos,name='eliminargastos'),


    path('RegistroEgreso/',registroegreso,name='registroegreso'),
    path('EliminarEgreso/',eliminaregreso,name='eliminaregreso'),


    path('RegistroProductoFinanciero/',registroproductofinanciero,name='registroproductofinanciero'),
    path('EliminarProductos/',eliminarproductos,name='eliminarproductos'),
    

    path('RegistroIngreso/',registroingreso,name='registroingreso'),
    path('EliminarIngreso/',eliminaringreso,name='eliminaringreso'),
    

]