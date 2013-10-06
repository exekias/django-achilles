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
    # Static field to hold all registered libraries
    registers = {}

    def __init__(self, namespace=None):
        if namespace in Library.registers:
            raise ValueError("A block namespace with name "
                             "'%s' is already registered" % namespace)

        Library.registers[namespace] = self
        BaseLibrary.__init__(self)

    def get(self, name, context=None, *args, **kwargs):
        """
        Return block instance for the given name
        """
        if name not in self.items:
            raise KeyError("'%s' block doesn't exists" % name)

        return BaseLibrary.get(self, name)(context, *args, **kwargs)

    # Provide block register
    block = BaseLibrary._register

    def simple_block(self, template, name=None):
        def dec(func):
            class SimpleBlock(Block):
                template_name = template

                def get_context_data(self, *args, **kwargs):
                    context = super(SimpleBlock,
                                    self).get_context_data(*args, **kwargs)
                    context.update(func(self.context, *args, **kwargs))
                    return context

            block_name = (
                name or
                getattr(func, '_decorated_function', func).__name__)

            self.block(block_name, SimpleBlock)
            return func
        return dec


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

    if ':' in name:
        namespace, name = name.split(':', 1)
    else:
        namespace = None

    if namespace not in Library.registers:
        raise KeyError("'%s' namespace doesn't exists for blocks" % namespace)

    register = Library.registers[namespace]
    try:
        return register.get(name, context, *args, **kwargs)
    except KeyError:
        pass

    raise KeyError("'%s' block doesn't exists" % name)


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
