from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils import six

from importlib import import_module

import sys


class AchillesTransport(object):
    """
    Transport object, holds information context for some user requests
    and response
    """
    def __init__(self, request):
        """
        Achilles Transport init for Django requests, it gets a request object
        and fills its fields from it
        """
        # plugin's data
        self._data = {}

        # common properties
        self.encoding = request.encoding

        # backend specific properties
        self.request = request

    def data(self, key=None, default=None):
        """
        Return achilles response dict. Achilles stores here data related
        to the request, in order to prepare a reply.

        If key value is given, this function will return that key (if exists)
        from achilles response dict.

        If default is given it will be asigned and returned if it doesn't exist
        """
        if key not in self._data and default is not None:
            self._data[key] = default

        return self._data[key]


def achilles_plugins():
    """
    Return a dict of the enabled plugins with achilles namespace as keys
    """
    return getattr(settings, 'ACHILLES_PLUGINS',
                   {
                       'blocks': 'achilles.blocks',
                       'actions': 'achilles.actions',
                       'console': 'achilles.console',
                       'redirect': 'achilles.redirect',
                       'messages': 'achilles.messages',
                   })


def achilles_renders():
    """
    Return a dict of enabled plugin' render functions
    """
    return {k: import_by_path('%s.render' % p)
            for k, p in achilles_plugins().items()}


# This method is borrowed from Django 1.6:
def import_by_path(dotted_path, error_prefix=''):
    """
    Import a dotted module path and return the attribute/class designated
    by the last name in the path. Raise ImproperlyConfigured if something
    goes wrong.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError:  # pragma: no cover
        raise ImproperlyConfigured("%s%s doesn't look like a module path" % (
            error_prefix, dotted_path))
    try:
        module = import_module(module_path)
    except ImportError as e:  # pragma: no cover
        msg = '%sError importing module %s: "%s"' % (
            error_prefix, module_path, e)
        six.reraise(ImproperlyConfigured, ImproperlyConfigured(msg),
                    sys.exc_info()[2])
    try:
        attr = getattr(module, class_name)
    except AttributeError:  # pragma: no cover
        raise ImproperlyConfigured(
            '%sModule "%s" does not define a "%s" attribute/class'
            % (error_prefix, module_path, class_name))
    return attr


class BaseLibrary(object):
    """
    Base register library, provides decorator functions to register
    items of any type.

    All items are registered using a name to uniquely identify them

    This register library is namespaced, so every new instance of it
    gets registered under the given namespace. This will avoid
    collisions between apps
    """
    namespace_separator = ':'

    def __init__(self, namespace):
        # global namespaced register
        if not hasattr(type(self), 'registers'):
            type(self).registers = {}

        # Register the instanced library
        if namespace in type(self).registers:
            library = type(self).registers[namespace]
            raise ValueError("An namespace with name "
                             "'%s' is already registered in '%s'" %
                             (namespace, library.__module__))

        type(self).registers[namespace] = self
        self.namespace = namespace
        self.items = {}

    def get(self, name):
        if name not in self.items:
            raise KeyError("'%s' item doesn't exists" % name)
        return self.items[name]

    @classmethod
    def get_global(cls, name):
        if cls.namespace_separator in name:
            namespace, name = name.split(cls.namespace_separator, 1)
        else:
            namespace = None
        if namespace not in cls.registers:
            raise KeyError("'%s' namespace doesn't exists. "
                           "Avaible namespaces are: %s"
                           % (namespace, cls.registers.keys()))
        register = cls.registers[namespace]
        try:
            return register.get(name)
        except KeyError:
            raise KeyError("'%s' doesn't exists" % name)

    def register(self, name=None):
        if name is None:
            return self._register
        elif callable(name):
            func = name
            name = getattr(name, '_decorated_function', name).__name__
            return self._register(func, name)
        else:
            def dec(func):
                return self._register(func, name)
            return dec

    def _register(self, func, name=None):
        name = name or getattr(func, '_decorated_function', func).__name__
        func.register_name = ':'.join([self.namespace or '', name])
        self.items[name] = func
        return func
