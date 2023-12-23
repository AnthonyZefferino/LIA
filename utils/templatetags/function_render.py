from django import template
from django.utils.safestring import mark_safe
from utils.Functions import IconSet

register = template.Library()


@register.simple_tag
def render_boolean(value):
    if value:
        return mark_safe('<span class="text-success"><i class="bx bx-check"></i></span>')
    else:
        return mark_safe('<span class="text-muted"><i class="bx bx-x"></i></span>')


@register.filter
def replace(value, args):
    search, replace = args.split(',')
    return value.replace(search, replace)


@register.filter
def trim(value):
    return value.strip()


@register.simple_tag
def get_icon_set():
    return IconSet()
