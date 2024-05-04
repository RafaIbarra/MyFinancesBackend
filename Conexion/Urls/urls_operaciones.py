from django.urls import path
from Conexion.Apis.Operaciones.api_registros_basicos import *
from Conexion.Apis.Operaciones.api_registros_movimientos import *
from Conexion.Apis.Estadisticas.api_estadisticas import *
from Conexion.Apis.SeguimientoApp.seguimiento_app import *
urlpatterns = [


    ################################Operaciones##################################################
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


    ################################Listados##################################################

    path('Meses/',meses,name='meses'),
    path('MisGastos/',misgastos,name='misgastos'),
    path('MisEgresos/<int:anno>/<int:mes>/',misegresos,name='misegresos'),

    path('MisDatosRegistroEgreso/',misdatosregistroegreso,name='misdatosregistroegreso'),
    path('MisCategorias/',miscategorias,name='miscategorias'),

    path('EstadisticasEgresos/<int:anno>/<int:mes>/',estadisticas_egresos,name='estadisticas_egresos'),
    path('EstadisticasIngresos/<int:anno>/<int:mes>/',estadisticas_ingresos,name='estadisticas_ingresos'),

    path('MisProductosFinancieros/',misproductosfinancieros,name='misproductosfinancieros'),
    path('MisIngresos/<int:anno>/<int:mes>/',misingresos,name='misingresos'),

    path('Balance/<int:anno>/<int:mes>/',balance,name='balance'),
    path('Resumen/<int:anno>/<int:mes>/',resumen,name='resumen'),

    path('EstadisticasMes/<int:anno>/<int:mes>/',estadisticas_mes,name='imagenes_mes'),

    ################################Listados Movile ##################################################

    path('MovileMisIngresos/<int:anno>/<int:mes>/',MovileMisIngresos,name='MovileMisIngresos'),
    path('MovileMisEgresos/<int:anno>/<int:mes>/',MovileMisEgresos,name='MovileMisEgresos'),
    path('MovileDatoEgreso/<int:anno>/<int:mes>/<int:id>/',MovileDatoEgreso,name='MovileDatoEgreso'),
    path('ComprobarSesionUsuario/',comprobarsesionusuario,name='comprobarsesionusuario'),

    

    ################################Datos Iniciales##################################################
    path('RegistroTipoGasto/',registrotipogasto,name='registrotipogasto'),
    path('ObtenerTipoGasto/',obtenertipogasto,name='obtenertipogasto'),
    path('RegistroTipoProduto/',registrotipoproduto,name='registrotipoproduto'),
    path('ObtenerTipoProducto/',obtenertipoproducto,name='obtenertipoproducto'),
    path('RegistroMeses/',registromeses,name='registromeses'),


    ################################Seguimiento##################################################
    path('SeguimientoUsuarios/',seguimiento_usuarios,name='seguimiento_usuarios'),
    path('SeguimientoSesiones/',seguimiento_sesiones,name='seguimiento_sesiones'),


    

]