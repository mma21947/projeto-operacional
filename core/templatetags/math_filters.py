from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def sub(value, arg):
    """Subtrai o valor do argumento."""
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        try:
            if isinstance(value, Decimal) or isinstance(arg, Decimal):
                return Decimal(str(value)) - Decimal(str(arg))
            return value - arg
        except:
            return 0

@register.filter
def mul(value, arg):
    """Multiplica o valor pelo argumento."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        try:
            if isinstance(value, Decimal) or isinstance(arg, Decimal):
                return Decimal(str(value)) * Decimal(str(arg))
            return value * arg
        except:
            return 0

@register.filter
def div(value, arg):
    """Divide o valor pelo argumento."""
    try:
        if float(arg) == 0:
            return 0
        return float(value) / float(arg)
    except (ValueError, TypeError):
        try:
            if arg == 0 or arg == 0.0 or arg == Decimal('0'):
                return 0
            if isinstance(value, Decimal) or isinstance(arg, Decimal):
                return Decimal(str(value)) / Decimal(str(arg))
            return value / arg
        except:
            return 0

@register.filter
def percentage(value, arg):
    """Calcula a porcentagem: (value/arg)*100."""
    try:
        if float(arg) == 0:
            return 0
        return (float(value) / float(arg)) * 100
    except (ValueError, TypeError):
        return 0

@register.filter
def subtract_from(value, arg):
    """Subtrai o valor do argumento (inverso de sub)."""
    try:
        return float(arg) - float(value)
    except (ValueError, TypeError):
        try:
            if isinstance(value, Decimal) or isinstance(arg, Decimal):
                return Decimal(str(arg)) - Decimal(str(value))
            return arg - value
        except:
            return 0

@register.filter
def default_if_none(value, default):
    """Retorna um valor padrão se o valor for None."""
    if value is None:
        return default
    return value

@register.filter
def abs_value(value):
    """Retorna o valor absoluto de um número."""
    try:
        return abs(float(value))
    except (ValueError, TypeError):
        try:
            if isinstance(value, Decimal):
                return abs(value)
            return abs(value)
        except:
            return 0

@register.filter(name='has_group')
def has_group(user, group_name):
    """
    Verifica se o usuário pertence a um grupo específico.
    Uso: {% if user|has_group:'Nome do Grupo' %}
    """
    from django.contrib.auth.models import Group
    try:
        group = Group.objects.get(name=group_name)
        return group in user.groups.all()
    except Group.DoesNotExist:
        return False 