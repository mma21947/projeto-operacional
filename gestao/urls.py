from django.urls import path
from . import views

app_name = 'gestao'

urlpatterns = [
    # URLs para Supervisores
    path('supervisores/', views.supervisores_lista, name='supervisores_lista'),
    path('supervisores/novo/', views.supervisor_novo, name='supervisor_novo'),
    path('supervisores/<int:pk>/editar/', views.supervisor_editar, name='supervisor_editar'),
    path('supervisores/<int:pk>/', views.supervisor_detalhes, name='supervisor_detalhes'),
    path('supervisores/<int:pk>/desativar/', views.supervisor_desativar, name='supervisor_desativar'),
] 