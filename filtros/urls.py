from django.urls import path, include
from . import views

app_name = 'filtros'
urlpatterns = [
  path('', views.index, name='index'),
  path('aplicar_filtro/', views.aplicar_filtro, name='aplicar_filtro')
]