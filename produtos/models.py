from django.db import models

# Create your models here.

class Produto(models.Model):
    nome = models.CharField("Nome do Produto", max_length=255)
    descricao = models.TextField("Descrição", blank=True, null=True)
    valor_unitario = models.DecimalField("Valor Unitário (R$)", max_digits=10, decimal_places=2)
    unidade_medida = models.CharField("Unidade de Medida", max_length=50, default="Unidade")
    codigo = models.CharField("Código do Produto", max_length=50, blank=True, null=True)
    data_cadastro = models.DateTimeField("Data de Cadastro", auto_now_add=True)
    ativo = models.BooleanField("Produto Ativo", default=True)
    
    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ["nome"]
    
    def __str__(self):
        return f"{self.nome} - R$ {self.valor_unitario}"
