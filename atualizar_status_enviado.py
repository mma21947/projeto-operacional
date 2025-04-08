#!/usr/bin/env python
"""
Script para atualizar pedidos com status 'enviado' para 'pedido_enviado'
"""
import os
import sys
import django

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Importar modelos
from pedidos.models import Pedido, PedidoLog
from django.contrib.auth.models import User
from django.utils import timezone

def main():
    """
    Função principal para verificar e atualizar pedidos com status 'enviado' para 'pedido_enviado'
    """
    # Verificar se há um usuário admin para registrar os logs
    try:
        usuario_admin = User.objects.filter(is_superuser=True).first()
    except:
        usuario_admin = None
        
    # Procurar por pedidos com status 'enviado'
    pedidos_enviados = Pedido.objects.filter(status='enviado')
    count = pedidos_enviados.count()
    
    if count == 0:
        print(f"Nenhum pedido encontrado com status 'enviado'")
        return
    
    print(f"Encontrados {count} pedidos com status 'enviado'")
    print("Atualizando para 'pedido_enviado'...")
    
    # Atualizar cada pedido
    for pedido in pedidos_enviados:
        # Guardar o status anterior para o log
        status_anterior = pedido.status
        status_anterior_display = 'Enviado'
        status_novo_display = 'Pedido Enviado'
        
        # Atualizar o status
        pedido.status = 'pedido_enviado'
        pedido.save()
        
        # Registrar log
        if usuario_admin:
            PedidoLog.objects.create(
                pedido=pedido,
                usuario=usuario_admin,
                acao='alteracao_status',
                status_anterior=status_anterior,
                status_novo='pedido_enviado',
                descricao=f"Status alterado automaticamente de '{status_anterior_display}' para '{status_novo_display}' devido à atualização do sistema"
            )
    
    print(f"Atualização concluída. {count} pedidos foram atualizados.")

if __name__ == "__main__":
    main() 