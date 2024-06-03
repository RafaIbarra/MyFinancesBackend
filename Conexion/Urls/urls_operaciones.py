from django.urls import path
from Conexion.Apis.Operaciones.api_registros_basicos import *
from Conexion.Apis.Operaciones.api_registros_movimientos import *
from Conexion.Apis.Estadisticas.api_estadisticas import *
from Conexion.Apis.SeguimientoApp.seguimiento_app import *
urlpatterns = [


    ################################Operaciones##################################################
    path('RegistroGasto/',registrogasto,name='registrogasto'),
    path('EliminarGastos/',eliminargastos,name='eliminargastos'),


    path('RegistroMedioPago/',registromediopago,name='registromediopago'),
    path('EliminarMediosPagos/',eliminarmediospagos,name='eliminarmediospagos'),

    path('RegistroCategoria/',registrocategoria,name='registrocategoria'),
    path('EliminarCategorias/',eliminarcategorias,name='eliminarcategorias'),

    path('RegistroEgreso/',registroegreso,name='registroegreso'),
    path('EliminarEgreso/',eliminaregreso,name='eliminaregreso'),


    path('RegistroProductoFinanciero/',registroproductofinanciero,name='registroproductofinanciero'),
    path('EliminarProductos/',eliminarproductos,name='eliminarproductos'),
    

    path('RegistroIngreso/',registroingreso,name='registroingreso'),
    path('EliminarIngreso/',eliminaringreso,name='eliminaringreso'),

    path('RegistroMovimientoBeneficio/',registromovimientobeneficio,name='registromovimientobeneficio'),
    path('EliminarMovimientoBeneficio/',eliminarmovimientobeneficio,name='eliminarmovimientobeneficio'),

    path('RegistroEntidadBeneficio/',registroentidadbeneficio,name='registroentidadbeneficio'),
    path('EliminarEntidadesBeneficios/',eliminarentidadesbeneficios,name='eliminarentidadesbeneficios'),

    path('ObtenerDatosUsuario/',obtenerdatosusuario,name='obtenerdatosusuario'),
    path('ActualizarDatosUsuario/',actualizardatosusuario,name='actualizardatosusuario'),

    path('EnvioCorreoPassword/',enviocorreocontraseña,name='enviocorreocontraseña'),
    path('ComprobarCodigo/',comprobarcodigo,name='comprobarcodigo'),
    path('ActualizarPassword/',actualizarpassword,name='actualizarpassword'),


    ################################Listados##################################################

    path('Meses/',meses,name='meses'),
    path('MisGastos/<int:id>/',misgastos,name='misgastos'),
    path('MisEgresos/<int:anno>/<int:mes>/',misegresos,name='misegresos'),

    path('MisDatosRegistroEgreso/',misdatosregistroegreso,name='misdatosregistroegreso'),
    path('MisCategorias/<int:id>/',miscategorias,name='miscategorias'),
    path('MisMediosPagos/<int:id>/',mismediospagos,name='mismediospagos'),
    

    path('EstadisticasEgresos/<int:anno>/<int:mes>/',estadisticas_egresos,name='estadisticas_egresos'),
    path('EstadisticasIngresos/<int:anno>/<int:mes>/',estadisticas_ingresos,name='estadisticas_ingresos'),

    path('MisProductosFinancieros/<int:id>/',misproductosfinancieros,name='misproductosfinancieros'),
    path('MisIngresos/<int:anno>/<int:mes>/',misingresos,name='misingresos'),

    path('MisEntidadesBeneficios/<int:id>/',misentidadesbeneficios,name='misentidadesbeneficios'),
    path('MisMovimientosBeneficios/<int:anno>/<int:mes>/<int:codigo>/',mismovimientosbeneficios,name='mismovimientosbeneficios'),

    path('Balance/<int:anno>/<int:mes>/',balance,name='balance'),
    path('Resumen/<int:anno>/<int:mes>/',resumen,name='resumen'),

    path('EstadisticasMes/<int:anno>/<int:mes>/',estadisticas_mes,name='imagenes_mes'),

    ################################Listados Movile ##################################################

    path('MovileMisIngresos/<int:anno>/<int:mes>/',MovileMisIngresos,name='MovileMisIngresos'),
    path('MovileDatoIngreso/<int:anno>/<int:mes>/<int:id>/',MovileDatoIngreso,name='MovileDatoIngreso'),


    path('MovileMisEgresos/<int:anno>/<int:mes>/',MovileMisEgresos,name='MovileMisEgresos'),
    path('MovileDatoEgreso/<int:anno>/<int:mes>/<int:id>/',MovileDatoEgreso,name='MovileDatoEgreso'),


    path('MovileResumenMes/<int:anno>/<int:mes>/',MovileResumenMes,name='MovileResumenMes'),
    path('MovileSaldos/<int:anno>/',MovileSaldos,name='MovileSaldos'),
    path('MovileEstadisticaMesSaldo/<int:anno>/<int:mes>/',estadisticas_mes_saldo,name='estadisticas_mes_saldo'),
    path('MovileEstadisticaMesIngreso/<int:anno>/<int:mes>/',estadisticas_mes_ingreso,name='estadisticas_mes_ingreso'),
    path('MovileEstadisticaMesEgreso/<int:anno>/<int:mes>/',estadisticas_mes_egreso,name='estadisticas_mes_egreso'),
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

    ################################Migraciones##################################################
    path('CargarMediosUsuarios/',CargarMediosUsuarios,name='CargarMediosUsuarios'),
    path('CargarDistribucionEgresos/',CargarDistribucionEgresos,name='CargarDistribucionEgresos'),


    

]