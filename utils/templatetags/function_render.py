from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def render_boolean(value):
    if value:
        return mark_safe('<span class="text-success"><i class="bx bx-check"></i></span>')
    else:
        return mark_safe('<span class="text-muted"><i class="bx bx-x"></i></span>')
