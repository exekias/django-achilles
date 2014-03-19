import json

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


def ablock_args(*args, **kwargs):
    res = ''
    if args:
        res += " data-ablock-args='%s'" % json.dumps(args)

    if kwargs:
        res += " data-ablock-kwargs='%s'" % json.dumps(kwargs)

    return res


@register.simple_tag(takes_context=True)
def ablock(context, name, *args, **kwargs):
    """
    Achilles block, this will render and embed the block in place
    """
    block = blocks.get(name, context)
    return '<div data-ablock="%s"%s>%s</div>' % (name,
                                                 ablock_args(*args, **kwargs),
                                                 block.render(*args, **kwargs))


@register.simple_tag(takes_context=True)
def ablock_lazy(context, name, *args, **kwargs):
    """
    Achilles block, won't be rendered until the page has load (javascript load)
    """
    # Make sure the block exists
    blocks.get(name, context)
    return ('<div data-ablock="%s" '
            'data-ablock-lazy="true"%s>'
            '</div>') % (name,
                         ablock_args(*args, **kwargs))


@register.simple_tag(takes_context=True)
def ablock_noload(context, name, *args, **kwargs):
    """
    Achilles block, will be placed but not loaded (empty)
    """
    # Make sure the block exists
    blocks.get(name, context)
    return ('<div data-ablock="%s" '
            'data-ablock-noload="true"%s>'
            '</div>') % (name, ablock_args(*args, **kwargs))
