from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from django.utils.log import getLogger
from importlib import import_module

from .common import BaseLibrary

logger = getLogger(__name__)


class Library(BaseLibrary):
    """
    Blocks register library
    """
    registers = {}

    def __init__(self, namespace=None):
        BaseLibrary.__init__(self, Block, namespace)

    def block(self, name=None, template_name=None):
        """
        Block register method
        """
        if not template_name:
            return self.register(name)

        def dec(name):
            res = self.register(name)
            if template_name:
                res.template_name = template_name
            return res
        return dec

    def create_class(self, func):
        class B(Block):
            def get_context_data(self, *args, **kwargs):
                context = super(B, self).get_context_data(*args, **kwargs)
                context.update(func(self.context, *args, **kwargs))
                return context
        return B


def get(name, context=None, *args, **kwargs):
    """
    Return block instance for the given name
    """
    # make sure all blocks are loaded
    for app in settings.INSTALLED_APPS:
        try:
            import_module(app + '.blocks')
        except:
            pass

    return Library.get_global(name)(context, *args, **kwargs)


class Block(object):
    """
    Block section, defines a block in the page. template_name instance field
    should be defined, so render method will use it in conjunction with
    get_context_data
    """
    # Should be defined
    template_name = None

    def __init__(self, context, *args, **kwargs):
        self.context = context or Context()
        self.args = args
        self.kwargs = kwargs

    def render(self):
        t = get_template(self.template_name)
        return t.render(self.get_context_data(*self.args, **self.kwargs))

    def get_context_data(self, *args, **kwargs):
        return self.context
