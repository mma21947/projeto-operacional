from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    path('', views.lista, name='lista'),
    path('novo/', views.novo, name='novo'),
    path('editar/<int:pk>/', views.editar, name='editar'),
    path('<int:pk>/', views.detalhes, name='detalhes'),
    path('<int:pk>/atualizar-status/', views.atualizar_status, name='atualizar_status'),
    path('<int:pk>/excluir/', views.excluir, name='excluir'),
    path('<int:pk>/duplicar/', views.duplicar, name='duplicar'),
    path('<int:pk>/imprimir/', views.imprimir_pedido, name='imprimir_pedido'),
    path('exportar/', views.exportar, name='exportar'),
    path('relatorio/', views.relatorio, name='relatorio'),
    path('dashboard/', views.dashboard_relatorios, name='dashboard_relatorios'),
    path('central-relatorios/', views.central_relatorios, name='central_relatorios'),
    path('exportar-excel/', views.exportar_excel, name='exportar_excel'),
] 