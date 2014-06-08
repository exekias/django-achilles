from django.conf import settings
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.utils.log import getLogger

import sys
import six
import traceback
from inspect import isclass
from importlib import import_module

from achilles.common import BaseLibrary
from achilles.actions import Library as ActionsLibrary

logger = getLogger(__name__)


class Library(BaseLibrary):
    """
    Blocks library holds a register of all defined blocks

    Use it to define and register new blocks, grouping them under
    a common namespace. See :func:`block`.

    :param namespace: Unique namespace for this register
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
            res = self._create_class(name)
            res.__name__ = getattr(name, '_decorated_function', name).__name__
            return self._register(res)
        else:
            return BaseLibrary.register(self, name)

    def block(self, name=None, template_name=None, takes_context=False):
        """
        Block register decorator, register a block on the library.

        When decorating a function, this method will automatically create a
        block. The block will use a dict returned by the function as template
        context::

            from achilles import blocks

            register = blocks.Library('myapp')

            @register.block(template_name='foo.html')
            def foo():
                return {
                    'template_var1' : 42,
                    'template_var2' : True,
                }

        When decorating a Block class it will just register it on the library.

        :param name: Name of the block, if None the decorated function name
                     will be taken
        :param template_name: Path of the block template
        :param takes_context: If True, the decorated function will receive
                              the template context as first parameter
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

    def _create_class(self, func):
        class B(Block):
            def get_context_data(self, *args, **kwargs):
                context = super(B, self).get_context_data(*args, **kwargs)
                if self.takes_context:
                    res = func(self.context, *args, **kwargs)
                else:
                    res = func(*args, **kwargs)
                if res != context:
                    context.update(res)
                return context
        return B


def get(name, context=None):
    """
    Retrieve a block with the given name. Example::

        blocks.get('myapp:foo')

    :param name: Fully namespaced block name
    """
    # make sure all blocks are loaded
    for app in settings.INSTALLED_APPS:
        if six.PY2:
            try:
                import_module(app + '.blocks')
            except ImportError:
                tb = sys.exc_info()[2]
                stack = traceback.extract_tb(tb, 3)
                if len(stack) > 2:
                    raise
        else:
            from importlib import find_loader
            if find_loader(app + '.blocks'):
                import_module(app + '.blocks')

    return Library.get_global(name)(context)


class Block(object):
    """
    Blocks are parts of the page that can be dinamically rendered. By calling
    :func:`update` action you can reload any block asynchronously.

    In most cases blocks are automatically created out of functions decorated
    with :func:`Library.block`. For advanced uses you may need to sublcass
    this.
    """
    #: Template file that will be used in :func:`render`
    template_name = None

    def __init__(self, context):
        self.context = context or Context()

    def render(self, *args, **kwargs):
        """
        Render the block, this method receives block arguments (if any)
        and renders HTML result of the block.
        """
        t = get_template(self.template_name)
        return t.render(self.get_context_data(*args, **kwargs))

    def get_context_data(self, *args, **kwargs):
        """
        Returns context to be passed to the template renderer in
        :func:`render`.
        """
        return self.context

    def update(self, transport, *args, **kwargs):
        """
        Render and send the update of block within the given achilles transport
        """
        transport.data('blocks', []).append({
            'name': self.register_name,
            'args': args,
            'kwargs': kwargs,
            'data': self.render(*args, **kwargs),
        })


register = ActionsLibrary('blocks')


@register.action
def update(transport, name, *args, **kwargs):
    """
    Action name: **blocks:update**

    Update a block, if the block doesn't exists on the page nothing will
    happen.

    Blocks may have arguments, this function will pass any argument to
    the block handler. When using arguments, only blocks matching them
    will be updated.

    :param transport: Achilles transport object that is being served
    :param name: Fully namespaced block name
    """
    context = RequestContext(transport.request, {})
    block = get(name, context)
    block.update(transport, *args, **kwargs)


def render(transport):
    return transport.data('blocks', [])
