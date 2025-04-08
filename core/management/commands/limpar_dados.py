from django.core.management.base import BaseCommand
from core.models import Empresa, Contrato, DetalhesContrato

class Command(BaseCommand):
    help = 'Limpa todos os dados de exemplo para o widget de utilização de orçamento'

    def handle(self, *args, **options):
        self.stdout.write('Limpando dados existentes...')
        
        # Remover detalhes de contrato
        count = DetalhesContrato.objects.all().count()
        DetalhesContrato.objects.all().delete()
        self.stdout.write(f'  - {count} detalhes de contrato removidos')
        
        # Remover contratos
        count = Contrato.objects.all().count()
        Contrato.objects.all().delete()
        self.stdout.write(f'  - {count} contratos removidos')
        
        # Remover empresas
        count = Empresa.objects.all().count()
        Empresa.objects.all().delete()
        self.stdout.write(f'  - {count} empresas removidas')
        
        self.stdout.write(self.style.SUCCESS('Todos os dados foram removidos com sucesso!')) 