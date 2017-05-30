from django import template
register = template.Library()

@register.filter
def index(List, i):
    return List[int(i)]

@register.filter
def split(value, sep = "."):
    parts = value.split(sep)
    return (parts[0], sep.join(parts[1:]))