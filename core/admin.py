from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.sites import site
from django.apps import apps
from django.urls import path
from django.template.response import TemplateResponse
from . import views

# Personalizar o título e cabeçalho do Admin
admin.site.site_header = "Administração do Sistema"
admin.site.site_title = "Painel Administrativo"
admin.site.index_title = "Autenticação e Autorização"

# Remover o link para o site principal
admin.site.site_url = None

# Classe personalizada para adicionar as views de backup/restauração ao admin
class AdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('backup-sistema/', self.admin_view(views.backup_sistema), name='backup_sistema'),
            path('restaurar-sistema/', self.admin_view(views.restaurar_sistema), name='restaurar_sistema'),
            path('confirmar-restauracao/', self.admin_view(views.confirmar_restauracao), name='confirmar_restauracao'),
        ]
        return custom_urls + urls
    
    def index(self, request, extra_context=None):
        # Adicionar links para backup e restauração na página inicial do admin
        extra_context = extra_context or {}
        extra_context['backup_restauracao'] = [
            {
                'name': 'Backup do Sistema',
                'admin_url': 'admin:backup_sistema',
                'description': 'Criar um backup completo do banco de dados e arquivos de mídia.'
            },
            {
                'name': 'Restaurar Sistema',
                'admin_url': 'admin:restaurar_sistema',
                'description': 'Restaurar o sistema a partir de um arquivo de backup.'
            }
        ]
        return super().index(request, extra_context)

# Substituir o AdminSite padrão pelo nosso customizado
admin.site.__class__ = AdminSite

# Removendo explicitamente todas as aplicações não relacionadas a autenticação
# Esta abordagem é mais direta e garante que todos os modelos serão desregistrados

# Remover modelos da aplicação 'escolas'
try:
    from escolas.models import Escola, Supervisor
    admin.site.unregister(Escola)
    admin.site.unregister(Supervisor)
except (ImportError, admin.sites.NotRegistered):
    pass

# Remover modelos da aplicação 'pedidos'
try:
    from pedidos.models import Pedido, ItemPedido
    admin.site.unregister(Pedido)
    admin.site.unregister(ItemPedido)
except (ImportError, admin.sites.NotRegistered):
    pass

# Remover modelos da aplicação 'produtos'
try:
    from produtos.models import Produto
    admin.site.unregister(Produto)
except (ImportError, admin.sites.NotRegistered):
    pass

# Remover configurações do sistema
try:
    from core.models import ConfiguracaoSistema
    admin.site.unregister(ConfiguracaoSistema)
except (ImportError, admin.sites.NotRegistered):
    pass

# Verificar o admin e remover qualquer modelo que não seja das apps auth ou contenttypes
for model, model_admin in list(admin.site._registry.items()):
    app_label = model._meta.app_label
    if app_label not in ['auth', 'contenttypes']:
        try:
            admin.site.unregister(model)
        except admin.sites.NotRegistered:
            pass
