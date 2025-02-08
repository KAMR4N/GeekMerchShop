from django import template

register = template.Library()

@register.filter
def comma_separate(value):
    try:
        value = int(value)
        return "{:,.0f}".format(value)
    except (ValueError, TypeError):
        return value