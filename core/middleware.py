"""
Middleware para controle de acesso baseado em perfis
"""
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import resolve, reverse

class PerfilAcessoMiddleware:
    """
    Middleware que restringe o acesso a certas URLs com base no perfil do usuário.
    
    - Gerente Operacional: Não pode acessar o painel admin e configurações
    - Usuários não autenticados: Só podem acessar a página de login e arquivos estáticos
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verificar se o usuário está autenticado
        if not request.user.is_authenticated:
            # URLs permitidas sem autenticação
            allowed_paths = [
                '/usuarios/login/',
                '/admin/login/',
                '/static/',
                '/media/',
                '/favicon.ico',
            ]
            
            current_path = request.path_info
            
            # Verificar se o caminho atual é permitido sem autenticação
            is_allowed = False
            for path in allowed_paths:
                if current_path.startswith(path):
                    is_allowed = True
                    break
            
            # Se não for uma URL permitida, redirecionar para a página de login
            if not is_allowed:
                return redirect('usuarios:login')
        
        # Se o usuário está autenticado, aplicar as restrições de perfil
        elif request.user.is_authenticated:
            current_url = request.path_info
            
            # NUNCA bloqueie superusuários (verificação explícita)
            if request.user.is_superuser:
                # Para superusuários, continue normalmente sem restrições
                pass
            # Verificamos se é um Gerente Operacional
            elif request.user.groups.filter(name='Gerente Operacional').exists():
                # Restringir acesso ao admin
                if current_url.startswith('/admin/'):
                    messages.error(request, 'Seu perfil não tem acesso ao painel de administração.')
                    return redirect('/')
                
                # Restringir acesso às configurações
                elif current_url.startswith('/configuracoes/'):
                    messages.error(request, 'Seu perfil não tem acesso às configurações do sistema.')
                    return redirect('/')
        
        # Continua o processamento da requisição
        response = self.get_response(request)
        return response 