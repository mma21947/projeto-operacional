from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def sub(value, arg):
    """Subtrai o argumento do valor"""
    try:
        # Converte para Decimal para evitar problemas com float
        value = Decimal(str(value))
        arg = Decimal(str(arg))
        return value - arg
    except (ValueError, TypeError):
        return ""

@register.filter(name='subtract')
def subtract(value, arg):
    """Subtrai o argumento do valor (novo nome mais descritivo)"""
    try:
        # Converte para Decimal para evitar problemas com float
        value = Decimal(str(value))
        arg = Decimal(str(arg))
        return value - arg
    except (ValueError, TypeError):
        return 0

@register.filter(name='percentage')
def percentage(value, total):
    """Calcula a porcentagem de value em relação ao total"""
    try:
        value = Decimal(str(value))
        total = Decimal(str(total))
        if total == 0:
            return 0
        return round((value / total) * 100, 1)
    except (ValueError, TypeError):
        return 0

@register.filter(name='currency')
def currency(value):
    """Formata um valor como moeda"""
    try:
        value = Decimal(str(value))
        return f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except (ValueError, TypeError):
        return "R$ 0,00" 