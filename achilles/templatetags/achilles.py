from django import template
from django.conf import settings
from django.core.urlresolvers import reverse

from .. import blocks


register = template.Library()


@register.simple_tag
def achilles_js():
    achilles_js = settings.STATIC_URL + 'js/achilles.js'
    endpoint = reverse('achilles.views.endpoint')
    return """
        <script src="%s"></script>
        <script type="text/javascript">achilles = achilles('%s');</script>
    """ % (achilles_js, endpoint)


@register.simple_tag(takes_context=True)
def ablock(context, name, *args, **kwargs):
    block = blocks.get(name, context, *args, **kwargs)
    return '<div data-ablock="%s">%s</div>' % (name, block.render())
