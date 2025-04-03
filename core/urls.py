from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('inicio/', views.home, name='home'),
    path('configuracoes/', views.configuracoes, name='configuracoes'),
    path('visao-gerencial/', views.visao_gerencial, name='visao_gerencial'),
    path('visao-gerencial/dados/', views.visao_gerencial_dados, name='visao_gerencial_dados'),
    path('visao-gerencial/verificar-dados/', views.verificar_dados, name='verificar_dados'),
    path('visao-gerencial/exportar/', views.exportar_dashboard, name='exportar_dashboard'),
    path('exportar-dados/', views.exportar_dados, name='exportar_dados'),
    path('limpar-temporarios/', views.limpar_temporarios, name='limpar_temporarios'),
    path('diagnostico-endereco/', views.diagnostico_endereco, name='diagnostico_endereco'),
] 