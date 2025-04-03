from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ConfiguracaoSistema(models.Model):
    nome_empresa = models.CharField("Nome da Empresa", max_length=255)
    cnpj = models.CharField("CNPJ", max_length=20, blank=True, null=True)
    endereco = models.TextField("Endereço", blank=True, null=True)
    telefone = models.CharField("Telefone", max_length=20, blank=True, null=True)
    email = models.EmailField("E-mail", blank=True, null=True)
    logo = models.ImageField("Logo", upload_to="logos/", blank=True, null=True)
    
    class Meta:
        verbose_name = "Configuração do Sistema"
        verbose_name_plural = "Configurações do Sistema"
    
    def __str__(self):
        return self.nome_empresa
    
    def save(self, *args, **kwargs):
        # Garante que só existe uma configuração no sistema
        if ConfiguracaoSistema.objects.exists() and not self.pk:
            # Se já existe uma configuração e estamos criando uma nova, atualiza a existente
            config = ConfiguracaoSistema.objects.first()
            config.nome_empresa = self.nome_empresa
            config.cnpj = self.cnpj
            config.endereco = self.endereco
            config.telefone = self.telefone
            config.email = self.email
            if self.logo:
                config.logo = self.logo
            config.save()
            return config
        else:
            return super().save(*args, **kwargs)

class Empresa(models.Model):
    nome = models.CharField("Nome da Empresa", max_length=255)
    cnpj = models.CharField("CNPJ", max_length=20, blank=True, null=True)
    endereco = models.TextField("Endereço", blank=True, null=True)
    telefone = models.CharField("Telefone", max_length=20, blank=True, null=True)
    email = models.EmailField("E-mail", blank=True, null=True)
    contato = models.CharField("Nome do Contato", max_length=255, blank=True, null=True)
    data_cadastro = models.DateTimeField("Data de Cadastro", auto_now_add=True)
    ativo = models.BooleanField("Empresa Ativa", default=True)
    
    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ["nome"]
    
    def __str__(self):
        return self.nome

class Contrato(models.Model):
    STATUS_CHOICES = (
        ('ATIVO', 'Ativo'),
        ('PENDENTE', 'Pendente'),
        ('FINALIZADO', 'Finalizado'),
        ('CANCELADO', 'Cancelado'),
    )
    
    numero = models.CharField("Número do Contrato", max_length=50)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="contratos", verbose_name="Empresa")
    descricao = models.TextField("Descrição", blank=True, null=True)
    data_inicio = models.DateField("Data de Início")
    data_fim = models.DateField("Data de Término")
    valor_total = models.DecimalField("Valor Total (R$)", max_digits=12, decimal_places=2, default=0)
    status = models.CharField("Status", max_length=20, choices=STATUS_CHOICES, default='ATIVO')
    data_criacao = models.DateTimeField("Data de Criação", auto_now_add=True)
    data_atualizacao = models.DateTimeField("Última Atualização", auto_now=True)
    ativo = models.BooleanField("Contrato Ativo", default=True)
    
    class Meta:
        verbose_name = "Contrato"
        verbose_name_plural = "Contratos"
        ordering = ["-data_inicio"]
    
    def __str__(self):
        return f"{self.numero} - {self.empresa.nome}"

class DetalhesContrato(models.Model):
    contrato = models.OneToOneField(Contrato, on_delete=models.CASCADE, related_name="detalhes", verbose_name="Contrato")
    responsavel = models.CharField("Responsável", max_length=255, blank=True, null=True)
    email_responsavel = models.EmailField("E-mail do Responsável", blank=True, null=True)
    telefone_responsavel = models.CharField("Telefone do Responsável", max_length=20, blank=True, null=True)
    observacoes = models.TextField("Observações", blank=True, null=True)
    orcamento_por_pedido = models.DecimalField("Orçamento por Pedido (R$)", max_digits=10, decimal_places=2, default=0)
    limite_pedidos_mes = models.IntegerField("Limite de Pedidos por Mês", default=0)
    regras_aprovacao = models.TextField("Regras de Aprovação", blank=True, null=True)
    
    class Meta:
        verbose_name = "Detalhes do Contrato"
        verbose_name_plural = "Detalhes dos Contratos"
    
    def __str__(self):
        return f"Detalhes - {self.contrato.numero}"
