from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from django.utils.log import getLogger
from importlib import import_module


logger = getLogger(__name__)


class Library(object):
    """
    Blocks register library
    """
    def __init__(self):
        self.blocks = {}

    def get(self, name, context=None, *args, **kwargs):
        """
        Return block instance for the given name
        """
        # make sure all blocks are loaded
        for app in settings.INSTALLED_APPS:
            try:
                import_module(app + '.blocks')
            except:
                pass
        return self.blocks[name](context=context, *args, **kwargs)

    def block(self, name=None, compile_function=None):
        if name is None:
            # @register.block()
            return self.block_function
        elif name is not None and compile_function is None:
            if callable(name):
                # @register.block
                return self.block_function(name)
            else:
                # @register.block('somename') @register.block(name='somename')
                def dec(func):
                    return self.block(name, func)
                return dec
        elif name is not None and compile_function is not None:
            # register.block('somename', somefunc)
            self.blocks[name] = compile_function
            return compile_function
        else:
            raise ValueError(
                "Unsupported arguments to "
                "Library.block: (%r, %r)", (name, compile_function))

    def block_function(self, func):
        self.blocks[getattr(func, "_decorated_function", func).__name__] = func
        return func

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

# Global register
register = Library()


class Block(object):
    """
    Block section, defines a block in the page. template_name instance field
    should be defined, so render method will use it in conjunction with
    get_context_data
    """
    # Should be defined
    template_name = None

    def __init__(self, context=None, *args, **kwargs):
        self.context = context or Context()
        self.args = args
        self.kwargs = kwargs

    def render(self):
        t = get_template(self.template_name)
        return t.render(self.get_context_data(*self.args, **self.kwargs))

    def get_context_data(self, *args, **kwargs):
        return self.context
