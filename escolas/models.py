from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Supervisor(models.Model):
    nome = models.CharField("Nome do Supervisor", max_length=255)
    email = models.EmailField("E-mail", blank=True, null=True)
    telefone = models.CharField("Telefone", max_length=20, blank=True, null=True)
    ativo = models.BooleanField("Ativo", default=True)
    usuario = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Usuário do Sistema", related_name="supervisor")
    
    class Meta:
        verbose_name = "Supervisor"
        verbose_name_plural = "Supervisores"
        ordering = ["nome"]
    
    def __str__(self):
        return self.nome

class Escola(models.Model):
    nome = models.CharField("Nome da Escola", max_length=255)
    codigo = models.CharField("Código da Escola", max_length=50, blank=True, null=True)
    lote = models.CharField("Lote", max_length=50, blank=True, null=True)
    empresa = models.CharField("Empresa", max_length=100, blank=True, null=True)
    budget = models.DecimalField("Orçamento (R$)", max_digits=10, decimal_places=2, default=0, help_text="Valor máximo permitido por pedido")
    data_validade_budget = models.DateField("Validade do Orçamento", blank=True, null=True, help_text="Data limite para utilização do orçamento")
    endereco = models.TextField("Endereço Completo", blank=True, null=True)
    cep = models.CharField("CEP", max_length=10, blank=True, null=True)
    cidade = models.CharField("Cidade", max_length=100, blank=True, null=True)
    estado = models.CharField("Estado", max_length=2, blank=True, null=True)
    telefone = models.CharField("Telefone", max_length=20, blank=True, null=True)
    email = models.EmailField("E-mail", blank=True, null=True)
    supervisor = models.ForeignKey(
        Supervisor, 
        on_delete=models.SET_NULL, 
        verbose_name="Supervisor Responsável", 
        related_name="escolas",
        blank=True, 
        null=True
    )
    data_cadastro = models.DateTimeField("Data de Cadastro", auto_now_add=True)
    ativo = models.BooleanField("Escola Ativa", default=True)
    
    class Meta:
        verbose_name = "Escola"
        verbose_name_plural = "Escolas"
        ordering = ["nome"]
    
    def __str__(self):
        return self.nome

    @property
    def budget_valido(self):
        """Verifica se o orçamento ainda é válido"""
        if self.data_validade_budget is None:
            return True  # Se não tem data de validade, considera-se válido
        
        return self.data_validade_budget >= timezone.localdate()
