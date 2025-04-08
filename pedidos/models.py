from django.db import models
from django.utils import timezone
from escolas.models import Escola
from produtos.models import Produto

class Pedido(models.Model):
    STATUS_CHOICES = (
        ('pendente', 'Pendente'),
        ('aprovado', 'Aprovado'),
        ('pedido_enviado', 'Pedido Enviado'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    )
    
    escola = models.ForeignKey(
        Escola, 
        on_delete=models.CASCADE, 
        verbose_name="Escola",
        related_name="pedidos"
    )
    data_solicitacao = models.DateTimeField("Data da Solicitação", default=timezone.now)
    data_aprovacao = models.DateTimeField("Data de Aprovação", blank=True, null=True)
    data_envio = models.DateTimeField("Data de Envio", blank=True, null=True)
    data_entrega = models.DateTimeField("Data de Entrega", blank=True, null=True)
    recebido_por = models.CharField("Recebido por", max_length=100, blank=True, null=True)
    status = models.CharField("Status", max_length=20, choices=STATUS_CHOICES, default='pendente')
    observacoes = models.TextField("Observações", blank=True, null=True)
    justificativa_cancelamento = models.TextField("Justificativa de Cancelamento", blank=True, null=True)
    
    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ["-data_solicitacao"]
    
    def __str__(self):
        return f"Pedido #{self.id} - {self.escola.nome}"
    
    @property
    def valor_total(self):
        return sum(item.valor_total for item in self.itens.all())
    
    def atualizar_status(self, novo_status, data_entrega_manual=None, recebido_por=None):
        self.status = novo_status
        
        # Atualiza as datas conforme o status
        if novo_status == 'aprovado':
            self.data_aprovacao = timezone.now()
        elif novo_status == 'pedido_enviado':
            self.data_envio = timezone.now()
        elif novo_status == 'entregue':
            # Usar a data fornecida ou a data atual se não fornecida
            self.data_entrega = data_entrega_manual or timezone.now()
            # Armazenar quem recebeu o pedido
            if recebido_por:
                self.recebido_por = recebido_por
            
        self.save()

class ItemPedido(models.Model):
    pedido = models.ForeignKey(
        Pedido, 
        on_delete=models.CASCADE, 
        verbose_name="Pedido",
        related_name="itens"
    )
    produto = models.ForeignKey(
        Produto, 
        on_delete=models.PROTECT, 
        verbose_name="Produto"
    )
    quantidade = models.PositiveIntegerField("Quantidade")
    valor_unitario = models.DecimalField("Valor Unitário (R$)", max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens do Pedido"
        unique_together = ['pedido', 'produto']
    
    def __str__(self):
        return f"{self.quantidade} x {self.produto.nome}"
    
    @property
    def valor_total(self):
        return self.quantidade * self.valor_unitario
    
    def save(self, *args, **kwargs):
        # Atualiza o valor unitário baseado no valor atual do produto
        if not self.valor_unitario:
            self.valor_unitario = self.produto.valor_unitario
        super().save(*args, **kwargs)

class PedidoLog(models.Model):
    """Modelo para registrar o histórico de operações em pedidos"""
    ACAO_CHOICES = (
        ('criacao', 'Criação'),
        ('alteracao_status', 'Alteração de Status'),
        ('edicao', 'Edição de Dados'),
        ('exclusao', 'Exclusão'),
    )
    
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        verbose_name="Pedido",
        related_name="logs"
    )
    usuario = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Usuário"
    )
    data_hora = models.DateTimeField("Data/Hora", auto_now_add=True)
    acao = models.CharField("Ação", max_length=20, choices=ACAO_CHOICES)
    status_anterior = models.CharField("Status Anterior", max_length=20, blank=True, null=True)
    status_novo = models.CharField("Novo Status", max_length=20, blank=True, null=True)
    descricao = models.TextField("Descrição", blank=True, null=True)
    
    class Meta:
        verbose_name = "Log de Pedido"
        verbose_name_plural = "Logs de Pedidos"
        ordering = ["-data_hora"]
    
    def __str__(self):
        return f"Log #{self.id} - Pedido #{self.pedido.id}"
