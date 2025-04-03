from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from escolas.models import Supervisor
from django.db import transaction

# Create your views here.

@login_required
@permission_required('escolas.view_supervisor')
def supervisores_lista(request):
    """Lista todos os supervisores cadastrados"""
    supervisores = Supervisor.objects.all().order_by('nome')
    return render(request, 'gestao/supervisores_lista.html', {
        'supervisores': supervisores
    })

@login_required
@permission_required('escolas.add_supervisor')
def supervisor_novo(request):
    """Adiciona um novo supervisor e usuário com perfil de Operador de Pedidos"""
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        ativo = request.POST.get('ativo') == 'on'
        
        # Campos de usuário
        username = request.POST.get('username')
        password = request.POST.get('password')
        criar_usuario = request.POST.get('criar_usuario') == 'on'
        
        # Validações básicas
        if not nome:
            messages.error(request, 'O nome do supervisor é obrigatório.')
            return render(request, 'gestao/supervisor_form.html', {
                'supervisor': None
            })
        
        # Validar informações de usuário se solicitado
        usuario = None
        if criar_usuario:
            if not username:
                messages.error(request, 'O nome de usuário é obrigatório para criar uma conta.')
                return render(request, 'gestao/supervisor_form.html', {
                    'supervisor': None,
                    'criar_usuario': criar_usuario,
                    'username': username
                })
            
            if not password:
                messages.error(request, 'A senha é obrigatória para criar uma conta.')
                return render(request, 'gestao/supervisor_form.html', {
                    'supervisor': None,
                    'criar_usuario': criar_usuario,
                    'username': username
                })
                
            # Verificar se o usuário já existe
            if User.objects.filter(username=username).exists():
                messages.error(request, f'O nome de usuário "{username}" já está em uso.')
                return render(request, 'gestao/supervisor_form.html', {
                    'supervisor': None,
                    'criar_usuario': criar_usuario,
                    'username': username
                })
        
        # Usar transação para garantir integridade dos dados
        with transaction.atomic():
            # Criar novo supervisor
            supervisor = Supervisor(
                nome=nome,
                email=email,
                telefone=telefone,
                ativo=ativo
            )
            supervisor.save()
            
            # Criar usuário se solicitado
            if criar_usuario:
                try:
                    # Criar usuário
                    usuario = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        first_name=nome
                    )
                    
                    # Adicionar ao grupo Operador de Pedidos
                    grupo_operador = Group.objects.get(name='Operador de Pedidos')
                    usuario.groups.add(grupo_operador)
                    
                    supervisor.usuario = usuario
                    supervisor.save()
                    
                    messages.success(request, f'Usuário "{username}" criado e adicionado ao grupo Operador de Pedidos.')
                except Exception as e:
                    messages.error(request, f'Erro ao criar usuário: {str(e)}')
        
        messages.success(request, f'Supervisor "{nome}" cadastrado com sucesso!')
        return redirect('gestao:supervisores_lista')
    
    return render(request, 'gestao/supervisor_form.html', {
        'supervisor': None,
        'criar_usuario': False
    })

@login_required
@permission_required('escolas.change_supervisor')
def supervisor_editar(request, pk):
    """Edita um supervisor existente e gerencia o usuário associado"""
    supervisor = get_object_or_404(Supervisor, pk=pk)
    usuario_existente = hasattr(supervisor, 'usuario') and supervisor.usuario is not None
    
    if request.method == 'POST':
        supervisor.nome = request.POST.get('nome')
        supervisor.email = request.POST.get('email')
        supervisor.telefone = request.POST.get('telefone')
        supervisor.ativo = request.POST.get('ativo') == 'on'
        
        # Campos de usuário
        username = request.POST.get('username')
        password = request.POST.get('password')
        criar_usuario = request.POST.get('criar_usuario') == 'on'
        
        # Validações
        if not supervisor.nome:
            messages.error(request, 'O nome do supervisor é obrigatório.')
            return render(request, 'gestao/supervisor_form.html', {
                'supervisor': supervisor,
                'criar_usuario': criar_usuario,
                'username': username,
                'usuario_existente': usuario_existente
            })
        
        # Usar transação para garantir integridade dos dados
        with transaction.atomic():
            supervisor.save()
            
            # Gerenciar usuário
            if criar_usuario and not usuario_existente:
                if not username:
                    messages.error(request, 'O nome de usuário é obrigatório para criar uma conta.')
                    return render(request, 'gestao/supervisor_form.html', {
                        'supervisor': supervisor,
                        'criar_usuario': criar_usuario,
                        'username': username,
                        'usuario_existente': usuario_existente
                    })
                
                if not password:
                    messages.error(request, 'A senha é obrigatória para criar uma conta.')
                    return render(request, 'gestao/supervisor_form.html', {
                        'supervisor': supervisor,
                        'criar_usuario': criar_usuario,
                        'username': username,
                        'usuario_existente': usuario_existente
                    })
                    
                # Verificar se o usuário já existe
                if User.objects.filter(username=username).exists():
                    messages.error(request, f'O nome de usuário "{username}" já está em uso.')
                    return render(request, 'gestao/supervisor_form.html', {
                        'supervisor': supervisor,
                        'criar_usuario': criar_usuario,
                        'username': username,
                        'usuario_existente': usuario_existente
                    })
                
                try:
                    # Criar usuário
                    usuario = User.objects.create_user(
                        username=username,
                        email=supervisor.email,
                        password=password,
                        first_name=supervisor.nome
                    )
                    
                    # Adicionar ao grupo Operador de Pedidos
                    grupo_operador = Group.objects.get(name='Operador de Pedidos')
                    usuario.groups.add(grupo_operador)
                    
                    supervisor.usuario = usuario
                    supervisor.save()
                    
                    messages.success(request, f'Usuário "{username}" criado e adicionado ao grupo Operador de Pedidos.')
                except Exception as e:
                    messages.error(request, f'Erro ao criar usuário: {str(e)}')
            
            # Atualizar senha se for um usuário existente e senha fornecida
            elif usuario_existente and password:
                try:
                    usuario = supervisor.usuario
                    usuario.set_password(password)
                    usuario.save()
                    messages.success(request, f'Senha do usuário "{usuario.username}" atualizada com sucesso.')
                except Exception as e:
                    messages.error(request, f'Erro ao atualizar senha: {str(e)}')
        
        messages.success(request, f'Supervisor "{supervisor.nome}" atualizado com sucesso!')
        return redirect('gestao:supervisores_lista')
    
    return render(request, 'gestao/supervisor_form.html', {
        'supervisor': supervisor,
        'criar_usuario': False,
        'usuario_existente': usuario_existente,
        'username': getattr(supervisor.usuario, 'username', '') if usuario_existente else ''
    })

@login_required
@permission_required('escolas.view_supervisor')
def supervisor_detalhes(request, pk):
    """Exibe detalhes de um supervisor, incluindo as escolas associadas"""
    supervisor = get_object_or_404(Supervisor, pk=pk)
    escolas = supervisor.escolas.all().order_by('nome')
    usuario_existente = hasattr(supervisor, 'usuario') and supervisor.usuario is not None
    
    # Calcular contratos ativos e inativos
    contratos_ativos = escolas.filter(ativo=True).count()
    contratos_inativos = escolas.filter(ativo=False).count()
    
    return render(request, 'gestao/supervisor_detalhes.html', {
        'supervisor': supervisor,
        'escolas': escolas,
        'usuario_existente': usuario_existente,
        'contratos_ativos': contratos_ativos,
        'contratos_inativos': contratos_inativos
    })

@login_required
@permission_required('escolas.delete_supervisor')
def supervisor_desativar(request, pk):
    """Desativa um supervisor (não exclui)"""
    supervisor = get_object_or_404(Supervisor, pk=pk)
    
    if request.method == 'POST':
        supervisor.ativo = False
        supervisor.save()
        
        # Desativar o usuário associado, se existir
        if hasattr(supervisor, 'usuario') and supervisor.usuario:
            supervisor.usuario.is_active = False
            supervisor.usuario.save()
            messages.success(request, f'Usuário "{supervisor.usuario.username}" desativado.')
            
        messages.success(request, f'Supervisor "{supervisor.nome}" desativado com sucesso!')
        return redirect('gestao:supervisores_lista')
    
    return render(request, 'gestao/supervisor_confirmar_desativacao.html', {
        'supervisor': supervisor,
        'usuario_existente': hasattr(supervisor, 'usuario') and supervisor.usuario
    })
