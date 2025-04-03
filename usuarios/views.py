from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages

# Create your views here.
@login_required
def perfil_view(request):
    """
    Exibe e permite editar o perfil do usuário logado
    """
    return render(request, 'usuarios/perfil.html', {
        'usuario': request.user
    })

def logout_view(request):
    """
    Realiza o logout do usuário e exibe uma mensagem de sucesso
    """
    if request.user.is_authenticated:
        nome_usuario = request.user.username
        logout(request)
        messages.success(request, f'Logoff realizado com sucesso! Até logo, {nome_usuario}.')
    return render(request, 'usuarios/logout_sucesso.html')
