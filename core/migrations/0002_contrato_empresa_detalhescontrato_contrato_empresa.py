# Generated by Django 5.1.7 on 2025-03-28 11:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contrato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=50, verbose_name='Número do Contrato')),
                ('descricao', models.TextField(blank=True, null=True, verbose_name='Descrição')),
                ('data_inicio', models.DateField(verbose_name='Data de Início')),
                ('data_fim', models.DateField(verbose_name='Data de Término')),
                ('valor_total', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Valor Total (R$)')),
                ('status', models.CharField(choices=[('ATIVO', 'Ativo'), ('PENDENTE', 'Pendente'), ('FINALIZADO', 'Finalizado'), ('CANCELADO', 'Cancelado')], default='ATIVO', max_length=20, verbose_name='Status')),
                ('data_criacao', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('data_atualizacao', models.DateTimeField(auto_now=True, verbose_name='Última Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Contrato Ativo')),
            ],
            options={
                'verbose_name': 'Contrato',
                'verbose_name_plural': 'Contratos',
                'ordering': ['-data_inicio'],
            },
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, verbose_name='Nome da Empresa')),
                ('cnpj', models.CharField(blank=True, max_length=20, null=True, verbose_name='CNPJ')),
                ('endereco', models.TextField(blank=True, null=True, verbose_name='Endereço')),
                ('telefone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Telefone')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='E-mail')),
                ('contato', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nome do Contato')),
                ('data_cadastro', models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')),
                ('ativo', models.BooleanField(default=True, verbose_name='Empresa Ativa')),
            ],
            options={
                'verbose_name': 'Empresa',
                'verbose_name_plural': 'Empresas',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='DetalhesContrato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('responsavel', models.CharField(blank=True, max_length=255, null=True, verbose_name='Responsável')),
                ('email_responsavel', models.EmailField(blank=True, max_length=254, null=True, verbose_name='E-mail do Responsável')),
                ('telefone_responsavel', models.CharField(blank=True, max_length=20, null=True, verbose_name='Telefone do Responsável')),
                ('observacoes', models.TextField(blank=True, null=True, verbose_name='Observações')),
                ('orcamento_por_pedido', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Orçamento por Pedido (R$)')),
                ('limite_pedidos_mes', models.IntegerField(default=0, verbose_name='Limite de Pedidos por Mês')),
                ('regras_aprovacao', models.TextField(blank=True, null=True, verbose_name='Regras de Aprovação')),
                ('contrato', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='detalhes', to='core.contrato', verbose_name='Contrato')),
            ],
            options={
                'verbose_name': 'Detalhes do Contrato',
                'verbose_name_plural': 'Detalhes dos Contratos',
            },
        ),
        migrations.AddField(
            model_name='contrato',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contratos', to='core.empresa', verbose_name='Empresa'),
        ),
    ]
