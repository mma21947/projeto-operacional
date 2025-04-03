"""
Script para criar perfis de acesso personalizados no sistema
=============================================================
Este script cria três perfis (grupos) de acesso:
1. Analista de Relatórios - Acesso apenas para visualização e geração de relatórios
2. Operador de Pedidos - Pode inserir pedidos e excluir apenas os não aprovados
3. Gerente Operacional - Acesso total como super admin, sem acesso ao painel admin

Executar com: python manage.py shell < criar_perfis.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from pedidos.models import Pedido, ItemPedido
from produtos.models import Produto
from escolas.models import Escola, Supervisor
from django.db.models import Q

# Função auxiliar para criar ou atualizar um grupo com permissões específicas
def criar_ou_atualizar_grupo(nome, descricao, permissoes):
    print(f"Criando/atualizando o grupo: {nome}")
    grupo, criado = Group.objects.get_or_create(name=nome)
    
    # Limpar permissões existentes
    grupo.permissions.clear()
    
    # Adicionar novas permissões
    for perm in permissoes:
        grupo.permissions.add(perm)
    
    print(f"✓ Grupo '{nome}' {'criado' if criado else 'atualizado'} com {grupo.permissions.count()} permissões")
    return grupo

# =============================================================
# Obter todos os content types relevantes para permissões
# =============================================================
pedido_ct = ContentType.objects.get_for_model(Pedido)
item_pedido_ct = ContentType.objects.get_for_model(ItemPedido)
produto_ct = ContentType.objects.get_for_model(Produto)
escola_ct = ContentType.objects.get_for_model(Escola)
supervisor_ct = ContentType.objects.get_for_model(Supervisor)

print("\n=== Configurando Perfis de Acesso ===")

# =============================================================
# 1. ANALISTA DE RELATÓRIOS
# =============================================================
# Permissões: Visualizar escolas, produtos e pedidos
print("\n=== CRIANDO PERFIL: ANALISTA DE RELATÓRIOS ===")
permissoes_analista = Permission.objects.filter(
    Q(content_type__in=[pedido_ct, item_pedido_ct, produto_ct, escola_ct, supervisor_ct]) &
    Q(codename__startswith='view_')
)

criar_ou_atualizar_grupo(
    "Analista de Relatórios",
    "Acesso apenas para visualização e geração de relatórios",
    permissoes_analista
)

# =============================================================
# 2. OPERADOR DE PEDIDOS
# =============================================================
# Permissões: Visualizar produtos/escolas, adicionar/editar/excluir pedidos não aprovados
print("\n=== CRIANDO PERFIL: OPERADOR DE PEDIDOS ===")
permissoes_operador = Permission.objects.filter(
    # Permissões de visualização para todos os modelos
    Q(content_type__in=[pedido_ct, item_pedido_ct, produto_ct, escola_ct, supervisor_ct]) &
    Q(codename__startswith='view_')
) | Permission.objects.filter(
    # Permissões completas para pedidos
    Q(content_type__in=[pedido_ct, item_pedido_ct]) &
    Q(codename__startswith='add_') |
    Q(codename__startswith='change_')
)

# Adicionamos delete_pedido separadamente - a lógica de "apenas não aprovados" precisa ser
# implementada na view, pois permissões do Django não têm esse nível de granularidade
permissao_delete_pedido = Permission.objects.get(
    content_type=pedido_ct,
    codename='delete_pedido'
)
permissao_delete_item = Permission.objects.get(
    content_type=item_pedido_ct,
    codename='delete_itempedido'
)

permissoes_operador_lista = list(permissoes_operador)
permissoes_operador_lista.extend([permissao_delete_pedido, permissao_delete_item])

criar_ou_atualizar_grupo(
    "Operador de Pedidos",
    "Pode inserir pedidos e excluir apenas quando não aprovados",
    permissoes_operador_lista
)

# =============================================================
# 3. GERENTE OPERACIONAL
# =============================================================
# Permissões: Acesso total ao sistema, exceto admin e configurações
print("\n=== CRIANDO PERFIL: GERENTE OPERACIONAL ===")
permissoes_gerente = Permission.objects.filter(
    content_type__in=[pedido_ct, item_pedido_ct, produto_ct, escola_ct, supervisor_ct]
)

criar_ou_atualizar_grupo(
    "Gerente Operacional",
    "Acesso total como super admin, exceto ao painel administrativo",
    permissoes_gerente
)

print("\n✓ Perfis de acesso criados com sucesso!")
print("Nota: As restrições específicas como 'excluir apenas pedidos não aprovados'")
print("      precisam ser implementadas no nível das views, pois o sistema de")
print("      permissões do Django não suporta esse nível de granularidade.")

# =============================================================
# FUNÇÃO UTILITÁRIA PARA ASSOCIAR USUÁRIOS A PERFIS
# =============================================================
print("\n=== FUNÇÃO UTILITÁRIA PARA ASSOCIAR USUÁRIOS A PERFIS ===")
print("""
Para associar um usuário a um perfil, execute o seguinte comando no shell:

from django.contrib.auth.models import User, Group
usuario = User.objects.get(username='nome_do_usuario')
grupo = Group.objects.get(name='Nome do Perfil')
usuario.groups.add(grupo)
usuario.save()

Onde 'Nome do Perfil' pode ser:
- Analista de Relatórios
- Operador de Pedidos
- Gerente Operacional
""") 