#!/usr/bin/env python
"""
Script para verificar e ajustar grupos do superusuário
=============================================================
Este script verifica se o usuário admin está em algum grupo que
possa estar causando conflitos e permite removê-lo desses grupos.

Executar com: python verificar_grupos_admin.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User, Group

# Função principal
def verificar_grupos_admin():
    try:
        # Encontrar o primeiro superusuário (geralmente chamado admin)
        admin = User.objects.filter(is_superuser=True).first()
        
        if not admin:
            print("⚠️ ERRO: Nenhum superusuário encontrado no sistema.")
            return
        
        print(f"\n=== Verificando grupos do superusuário: {admin.username} ===")
        
        # Verificar se admin está em algum grupo
        grupos_admin = admin.groups.all()
        
        if not grupos_admin:
            print("✅ O superusuário não pertence a nenhum grupo. Isto é recomendado.")
            return
        
        print(f"⚠️ O superusuário pertence aos seguintes grupos:")
        for grupo in grupos_admin:
            print(f"   • {grupo.name}")
        
        print("\nIsto pode estar causando conflitos de permissões.")
        remover = input("Deseja remover o superusuário de todos os grupos? (s/n): ")
        
        if remover.lower() == 's':
            # Remover admin de todos os grupos
            admin.groups.clear()
            print("✅ O superusuário foi removido de todos os grupos.")
        else:
            print("⚠️ Operação cancelada. O superusuário continua nos grupos.")
            
    except Exception as e:
        print(f"⚠️ ERRO ao verificar grupos: {str(e)}")

# Executar o script
if __name__ == "__main__":
    verificar_grupos_admin() 