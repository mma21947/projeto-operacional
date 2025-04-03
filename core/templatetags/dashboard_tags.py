from django import template
from django.template.defaultfilters import floatformat
from decimal import Decimal

register = template.Library()

@register.filter
def sum_list(value, key):
    """Soma os valores de uma lista de dicionários baseado em uma chave"""
    if not value:
        return 0
    
    try:
        return sum(item[key] for item in value if key in item)
    except (KeyError, TypeError):
        return 0

@register.filter
def multiply(value, arg):
    """Multiplica o valor pelo argumento"""
    try:
        return float(value or 0) * float(arg or 0)
    except (ValueError, TypeError):
        return 0

@register.filter
def divide(value, arg):
    """Divide o valor pelo argumento"""
    try:
        arg = float(arg or 0)
        if arg == 0:
            return 0
        return float(value or 0) / arg
    except (ValueError, TypeError, ZeroDivisionError):
        return 0

@register.filter
def subtract(value, arg):
    """Subtrai o argumento do valor"""
    try:
        return float(value or 0) - float(arg or 0)
    except (ValueError, TypeError):
        return 0

@register.filter
def get_item(dictionary, key):
    """Obtém um item de um dicionário pelo nome da chave"""
    return dictionary.get(key, 0)

@register.filter
def dictsort(value, key):
    """Ordena uma lista de dicionários pelo valor de uma chave específica"""
    try:
        return sorted(value, key=lambda k: k.get(key, 0))
    except (AttributeError, TypeError):
        return value

@register.filter
def dictvalue(value, key):
    """Obtém um valor específico de um dicionário ordenado por uma chave"""
    try:
        for item in value:
            if item.get('status', '') == key or item.get(key, None) is not None:
                return item.get('total', item.get(key, 0))
        return 0
    except (AttributeError, TypeError):
        return 0

@register.filter
def percentage(value, arg):
    """Calcula a porcentagem de value em relação a arg"""
    try:
        arg = float(arg or 0)
        if arg == 0:
            return 0
        percentage = (float(value or 0) / arg) * 100
        return floatformat(percentage, 1)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0 