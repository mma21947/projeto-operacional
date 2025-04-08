from django.urls import path
from . import views

app_name = 'produtos'

urlpatterns = [
    path('', views.lista, name='lista'),
    path('novo/', views.novo, name='novo'),
    path('editar/<int:pk>/', views.editar, name='editar'),
    path('importar/', views.importar, name='importar'),
    path('download-modelo/', views.download_modelo, name='download_modelo'),
] 