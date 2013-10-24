

def achilles_from_request(request, key=None, default=None):
    """
    Return achilles response dict. Achilles stores here data related
    to the request, in order to prepare a reply.

    If key value is given, this function will return that key (if exists)
    from achilles response dict.

    If default is given it will be asigned and returned in it does not exists
    """
    if not hasattr(request, '_achilles'):
        request._achilles = {}

    if key is None:
        return request._achilles

    if key not in request._achilles and default is not None:
        request._achilles[key] = default

    return request._achilles[key]


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
            raise ValueError("An namespace with name "
                             "'%s' is already registered" % namespace)

        type(self).registers[namespace] = self
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
            raise KeyError("'%s' namespace doesn't exists" % namespace)
        register = cls.registers[namespace]
        try:
            return register.get(name)
        except KeyError:
            pass

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
        self.items[name] = func
        return func
