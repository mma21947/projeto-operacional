from django.core.management.base import BaseCommand
from core.models import Empresa, Contrato, DetalhesContrato
from django.utils import timezone

class Command(BaseCommand):
    help = 'Cria dados de exemplo para o widget de utilização de orçamento'

    def handle(self, *args, **options):
        # Criar empresas
        self.stdout.write('Criando empresas de exemplo...')
        empresas = []
        nomes_empresas = ['Empresa Real A', 'Empresa Real B', 'Empresa Real C', 
                          'Empresa Real D', 'Empresa Real E', 'Empresa Real F']
        
        for i, nome in enumerate(nomes_empresas):
            # Verifica se a empresa já existe
            if not Empresa.objects.filter(nome=nome).exists():
                empresa = Empresa.objects.create(
                    nome=nome,
                    cnpj=f'1234567890{i+1:04d}',
                    contato=f'Contato {chr(65+i)}',
                    email=f'email{chr(65+i)}@empresa.com',
                    telefone=f'1122333{i+1:04d}',
                    ativo=True
                )
                self.stdout.write(f'  - {empresa.nome} criada com ID {empresa.id}')
            else:
                empresa = Empresa.objects.get(nome=nome)
                self.stdout.write(f'  - {empresa.nome} já existe (ID {empresa.id})')
            
            empresas.append(empresa)
        
        # Criar contratos - vamos criar contratos primeiro
        self.stdout.write('Criando contratos...')
        hoje = timezone.now().date()
        contratos = []
        
        # Orçamentos e percentuais para cada contrato
        orcamentos = [120000, 85000, 150000, 95000, 110000, 75000]
        percentuais = [85, 90, 85, 60, 90, 70]  # em %
        
        for i, (empresa, orcamento, percentual) in enumerate(zip(empresas, orcamentos, percentuais)):
            numero_contrato = f'CONT-REAL-{i+1:03d}'
            
            # Verifica se o contrato já existe
            if not Contrato.objects.filter(numero=numero_contrato).exists():
                contrato = Contrato.objects.create(
                    numero=numero_contrato,
                    empresa=empresa,
                    data_inicio=hoje.replace(month=1, day=1),
                    data_fim=hoje.replace(month=12, day=31),
                    valor_total=orcamento * 4,  # Orçamento para 4 trimestres
                    descricao=f'Contrato Real {chr(65+i)}',
                    ativo=True
                )
                self.stdout.write(f'  - Contrato {contrato.numero} criado para {empresa.nome}')
            else:
                contrato = Contrato.objects.get(numero=numero_contrato)
                self.stdout.write(f'  - Contrato {contrato.numero} já existe para {empresa.nome}')
            
            contratos.append(contrato)
        
        # Agora vamos criar/atualizar os detalhes de contrato
        self.stdout.write('Criando detalhes de contrato...')
        
        for contrato, orcamento in zip(contratos, orcamentos):
            # Verificar se já existe detalhes para este contrato
            try:
                detalhe = DetalhesContrato.objects.get(contrato=contrato)
                detalhe.orcamento_por_pedido = orcamento
                detalhe.save()
                self.stdout.write(f'  - Detalhes atualizados para {contrato.numero} com orçamento R${orcamento}')
            except DetalhesContrato.DoesNotExist:
                detalhe = DetalhesContrato.objects.create(
                    contrato=contrato,
                    orcamento_por_pedido=orcamento
                )
                self.stdout.write(f'  - Detalhes criados para {contrato.numero} com orçamento R${orcamento}')
            
            # Atualizar o contrato para apontar para os detalhes
            contrato.detalhes = detalhe
            contrato.save()
        
        self.stdout.write(self.style.SUCCESS('Dados criados com sucesso!')) 