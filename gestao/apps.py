from django.apps import AppConfig
from django.db.models.signals import post_migrate


class GestaoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestao'
    
    def ready(self):
        from django.contrib.auth.models import Group, Permission
        
        def create_default_groups(sender, **kwargs):
            # Criar grupo 'Operador de Pedidos' se não existir
            operador_group, created = Group.objects.get_or_create(name='Operador de Pedidos')
            
            # Se o grupo acabou de ser criado, atribuir permissões
            if created:
                # Permissões para Pedidos
                try:
                    # Permissões para visualizar e adicionar pedidos
                    view_pedido = Permission.objects.get(codename='view_pedido')
                    add_pedido = Permission.objects.get(codename='add_pedido')
                    change_pedido = Permission.objects.get(codename='change_pedido')
                    
                    operador_group.permissions.add(view_pedido, add_pedido, change_pedido)
                    
                    # Permissões para visualizar produtos e escolas
                    view_produto = Permission.objects.get(codename='view_produto')
                    view_escola = Permission.objects.get(codename='view_escola')
                    
                    operador_group.permissions.add(view_produto, view_escola)
                    
                    print(f"Grupo 'Operador de Pedidos' criado e permissões atribuídas com sucesso.")
                except Exception as e:
                    print(f"Erro ao atribuir permissões ao grupo 'Operador de Pedidos': {e}")
        
        # Conectar o sinal post_migrate para criar os grupos após a migração
        post_migrate.connect(create_default_groups, sender=self)
