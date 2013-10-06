from django import template
from django.template.loader_tags import IncludeNode

from achilles import blocks

register = template.Library()


@register.simple_tag(takes_context=True)
def ablock(context, name, *args, **kwargs):
    block = blocks.get(name, context, *args, **kwargs)
    return '<div data-ablock="name">%s</div>' % block.render()
