from django.contrib import admin
from .models import Pedido, ItemPedido

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    autocomplete_fields = ['produto']
    fields = ('produto', 'quantidade', 'valor_unitario')
    extra = 1
    min_num = 1

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'escola', 'data_solicitacao', 'status', 'get_valor_total')
    list_filter = ('status', 'escola', 'data_solicitacao')
    search_fields = ('escola__nome', 'observacoes')
    autocomplete_fields = ['escola']
    readonly_fields = ('data_solicitacao',)
    inlines = [ItemPedidoInline]
    
    def get_valor_total(self, obj):
        return f"R$ {obj.valor_total:.2f}"
    get_valor_total.short_description = "Valor Total"
