from django import template

# This creates a library so Django can understand our new tools
register = template.Library()

@register.filter
def multiply(value, arg):
    """
    Multiplies the value by the argument.
    Usage: {{ value|multiply:0.5 }}
    Example: 10 * 0.5 = 5.0
    """
    try:
        # We convert both numbers to 'float' (decimal numbers) to be safe
        return float(value) * float(arg)
    except (ValueError, TypeError):
        # If something goes wrong (like text instead of numbers), return 0
        return 0

@register.filter
def percentage(value, total):
    """
    Calculates the percentage.
    Usage: {{ value|percentage:total }}
    Example: 50 / 100 = 50%
    """
    try:
        val = float(value)
        tot = float(total)
        if tot == 0:
            return 0
        return (val / tot) * 100
    except (ValueError, TypeError):
        return 0

@register.filter
def safe_divide(value, arg):
    """
    Divides value by arg safely.
    Usage: {{ value|safe_divide:2 }}
    If arg is 0, it returns 0 instead of crashing.
    """
    try:
        val = float(value)
        divisor = float(arg)
        if divisor == 0:
            return 0
        return val / divisor
    except (ValueError, TypeError):
        return 0

# Note: Django already has a built-in 'add' filter, but here is a safe version if needed
@register.filter(name='safe_add')
def safe_add(value, arg):
    """
    Adds two numbers safely.
    Usage: {{ value|safe_add:5 }}
    """
    try:
        return float(value) + float(arg)
    except (ValueError, TypeError):
        return value
