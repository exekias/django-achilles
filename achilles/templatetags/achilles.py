from django import template
from django.conf import settings
from django.core.urlresolvers import reverse

from .. import blocks


register = template.Library()


@register.simple_tag
def achilles_js():
    achilles_js = settings.STATIC_URL + 'js/achilles.js'
    endpoint = reverse('achilles.views.endpoint')
    return ("<script src=\"%s\"></script>\n"
            "<script type=\"text/javascript\">"
            "achilles = Achilles('%s')</script>") % (achilles_js, endpoint)


@register.simple_tag(takes_context=True)
def ablock(context, name, *args, **kwargs):
    """
    Achilles block, this will load a block once the page is loaded
    """
    block = blocks.get(name, context, *args, **kwargs)
    return '<div data-ablock="%s">%s</div>' % (name, block.render())


@register.simple_tag(takes_context=True)
def ablock_lazy(context, name, *args, **kwargs):
    """
    This block won't load until someone asks for it (from Javascript or
    server side)
    """
    # Make sure the block exists
    blocks.get(name, context, *args, **kwargs)
    return '<div data-ablock="%s" data-noload="true"></div>' % name
