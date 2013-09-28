from django.template import RequestContext
from django.template.loader import get_template
from django.utils.log import getLogger

logger = getLogger(__name__)


class Library(object):
    """
    Blocks register library
    """
    def __init__(self):
        self.blocks = {}

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
            class SimpleBlock(ZBlock):
                template_name = template

                def get_context_data(self, *args, **kwargs):
                    context = super(SimpleBlock,
                                    self).get_context_data(*args, **kwargs)
                    return context.update(func(self.request, *args, **kwargs))

            block_name = (
                name or
                getattr(func, '_decorated_function', func).__name__)

            self.block(block_name, SimpleBlock)
            return func
        return dec


class ZBlock(object):
    """
    Block section, defines a block in the page. template_name instance field
    should be defined, so render method will use it in conjunction with
    get_context_data
    """
    # Should be defined
    template_name = None

    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs

    def render(self):
        t = get_template(self.template_name)
        return t.render(self.get_context_data(*self.args, **self.kwargs))

    def get_context_data(self, *args, **kwargs):
        return RequestContext(self.request, {})
