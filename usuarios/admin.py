from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.db.models import Count
from django.apps import apps
from django.db import models

# Personalizar o admin de usuários
class CustomUserAdmin(UserAdmin):
    # Personalizar quais campos aparecem na lista
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    
    # Adicionar filtros úteis
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    
    # Campos de pesquisa
    search_fields = ('username', 'first_name', 'last_name', 'email')
    
    # Organização dos campos no formulário
    fieldsets = (
        (_('Login'), {'fields': ('username', 'password')}),
        (_('Informações Pessoais'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissões'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Datas Importantes'), {'fields': ('last_login', 'date_joined')}),
    )
    
    # Melhorar o desempenho na seleção de grupos e permissões
    filter_horizontal = ('groups', 'user_permissions',)

# Personalizar o admin de grupos
class CustomGroupAdmin(GroupAdmin):
    list_display = ('name', 'count_permissions')
    search_fields = ('name',)
    filter_horizontal = ('permissions',)
    
    def count_permissions(self, obj):
        return obj.permissions.count()
    count_permissions.short_description = 'Número de permissões'

# Desregistra o admin padrão do User e Group
admin.site.unregister(User)
admin.site.unregister(Group)

# Registra os admin customizados
admin.site.register(User, CustomUserAdmin)
admin.site.register(Group, CustomGroupAdmin)

# Criar grupo de Operador de Pedidos se não existir
def create_operator_group():
    # Busca o grupo Operador de pedidos, ou cria se não existir
    operator_group, created = Group.objects.get_or_create(name='Operador de Pedidos')
    
    if created or operator_group.permissions.count() == 0:
        # Busca as permissões relevantes para o operador de pedidos
        # Permissões de visualização, adição e alteração de pedidos
        pedido_model = apps.get_model('pedidos', 'Pedido')
        content_type = admin.models.ContentType.objects.get_for_model(pedido_model)
        
        view_perm = Permission.objects.get(
            content_type=content_type, 
            codename='view_pedido'
        )
        add_perm = Permission.objects.get(
            content_type=content_type, 
            codename='add_pedido'
        )
        change_perm = Permission.objects.get(
            content_type=content_type, 
            codename='change_pedido'
        )
        
        # Atribui as permissões ao grupo
        operator_group.permissions.add(view_perm, add_perm, change_perm)
        
        print(f"Grupo 'Operador de pedidos' criado/atualizado com permissões!")

# Tenta criar o grupo quando o arquivo é carregado
try:
    # Somente tenta criar o grupo se o banco de dados estiver disponível
    from django.db.utils import OperationalError, ProgrammingError
    try:
        create_operator_group()
    except (OperationalError, ProgrammingError):
        # O banco de dados provavelmente não está pronto ainda (ex: durante migrações)
        pass
except:
    # Ignora qualquer erro durante a criação do grupo
    pass
