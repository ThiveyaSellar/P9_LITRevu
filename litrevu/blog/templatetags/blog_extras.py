from django import template

register = template.Library()

@register.filter
def model_type(instance):
    return type(instance).__name__

@register.filter
def is_null(instance):
    return instance.image is None

