from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^redireccionar/$', views.redireccionar, name='redireccionar'),
  url(r'^registrarRestaurante/$', views.registrarRestaurante, name='registrarRestaurante'),
  url(r'^modificarRestaurante/$', views.modificarRestaurante, name='modificarRestaurante'),
  url(r'^ajax/$', views.devuelve_filas, name='ajax'),
  url(r'^test/$', views.test, name='test'),
]