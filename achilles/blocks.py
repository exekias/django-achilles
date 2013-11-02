from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from django.utils.log import getLogger

from inspect import isclass
from importlib import import_module

from achilles.common import BaseLibrary, achilles_data
from achilles.actions import Library as ActionsLibrary

logger = getLogger(__name__)


class Library(BaseLibrary):
    """
    Blocks register library
    """
    registers = {}

    def __init__(self, namespace=None):
        BaseLibrary.__init__(self, namespace)

    def register(self, name=None):
        if name is None:
            return BaseLibrary.register(self, name)
        elif isclass(name) and issubclass(name, Block):
            return self._register(name)
        elif callable(name):
            res = self.create_class(name)
            res.__name__ = getattr(name, '_decorated_function', name).__name__
            return self._register(res)
        else:
            return BaseLibrary.register(self, name)

    def block(self, name=None, template_name=None, takes_context=False):
        """
        Block register method
        """
        if not template_name:
            return self.register(name)

        def dec(name):
            res = self.register(name)
            if template_name:
                res.template_name = template_name
                res.takes_context = takes_context
            return res
        return dec

    def create_class(self, func):
        class B(Block):
            def get_context_data(self, *args, **kwargs):
                context = super(B, self).get_context_data(*args, **kwargs)
                if self.takes_context:
                    res = func(self.context, *args, **kwargs)
                else:
                    res = func(*args, **kwargs)
                context.update(res)
                return context
        return B


def get(name, context=None):
    """
    Return block instance for the given name
    """
    # make sure all blocks are loaded
    for app in settings.INSTALLED_APPS:
        try:
            import_module(app + '.blocks')
        except ImportError:
            pass

    return Library.get_global(name)(context)


class Block(object):
    """
    Block section, defines a block in the page. template_name instance field
    should be defined, so render method will use it in conjunction with
    get_context_data
    """
    # Should be defined
    template_name = None

    def __init__(self, context):
        self.context = context or Context()

    def render(self, *args, **kwargs):
        t = get_template(self.template_name)
        return t.render(self.get_context_data(*args, **kwargs))

    def get_context_data(self, *args, **kwargs):
        return self.context


register = ActionsLibrary('blocks')


@register.action
def update(request, name, *args, **kwargs):
    """
    Update a block (with optional block params)
    """
    block = get(name)
    blocks = achilles_data(request, 'blocks', [])
    blocks.append({
        'name': name,
        'args': args,
        'kwargs': kwargs,
        'data': block.render(*args, **kwargs),
    })


def render_blocks(request):
    return achilles_data(request, 'blocks', [])
