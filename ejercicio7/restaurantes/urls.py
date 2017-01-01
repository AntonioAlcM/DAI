from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^redireccionar/registrar$', views.redireccionar, name='redireccionar'),
  url(r'^registrarRestaurante/$', views.registrarRestaurante, name='registrarRestaurante'),
  url(r'^modificarRestaurante/$', views.modificarRestaurante, name='modificarRestaurante'),
  url(r'^redireccionar/buscar$', views.redireccionarBuscarRestaurante, name='redireccionarBuscar'),
  url(r'^buscarRestaurante/$', views.buscadorDeRestaurantes, name='buscarRestaurante'),
  url(r'^ajax/$', views.devuelve_filas, name='ajax'),
  url(r'^redireccionar/mapa$', views.redireccionarMapa, name='redireccionarMapa'),
  url(r'^mapa/$', views.devuelve_coordenadas, name='verMapa'),
  url(r'^redireccionar/estadistica$', views.redireccionarEstadistica, name='redireccionarEstadistica'),
  url(r'^estadistica/$', views.devuelve_informacion, name='verEstadistica'),
  url(r'^redireccionar/twitter$', views.redireccionarTwitter, name='redireccionarTwitter'),
  url(r'^buscarTwitter/$', views.buscarTwitter, name='buscarTwitter'),
  url(r'^modificarRestaurante/(?P<identificador>\d+)/$', views.modificarUnRestaurante, name='modificarUnRestaurante'),
  url(r'^modificarRestaurante/restaurante$', views.modRestaurante, name='modificarRestauranteExistente'),
  url(r'^test/$', views.test, name='test'),
]