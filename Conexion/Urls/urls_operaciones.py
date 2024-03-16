from django.urls import path
from Conexion.Apis.Operaciones.api_registros_basicos import *
from Conexion.Apis.Operaciones.api_registros_movimientos import *
urlpatterns = [



    path('RegistroGasto/',registrogasto,name='registrogasto'),
    path('EliminarGastos/',eliminargastos,name='eliminargastos'),

    path('RegistroCategoria/',registrocategoria,name='registrocategoria'),
    path('EliminarCategorias/',eliminarcategorias,name='eliminarcategorias'),

    path('RegistroEgreso/',registroegreso,name='registroegreso'),
    path('EliminarEgreso/',eliminaregreso,name='eliminaregreso'),


    path('RegistroProductoFinanciero/',registroproductofinanciero,name='registroproductofinanciero'),
    path('EliminarProductos/',eliminarproductos,name='eliminarproductos'),
    

    path('RegistroIngreso/',registroingreso,name='registroingreso'),
    path('EliminarIngreso/',eliminaringreso,name='eliminaringreso'),

    path('ObtenerDatosUsuario/',obtenerdatosusuario,name='obtenerdatosusuario'),
    path('ActualizarDatosUsuario/',actualizardatosusuario,name='actualizardatosusuario'),

    path('EnvioCorreoPassword/',enviocorreocontraseña,name='enviocorreocontraseña'),
    path('ComprobarCodigo/',comprobarcodigo,name='comprobarcodigo'),
    path('ActualizarPassword/',actualizarpassword,name='actualizarpassword'),
    

]