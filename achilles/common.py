from inspect import isclass


class BaseLibrary(object):
    """
    Base register library, provides decorator functions to register
    any of the following items:

        * A subclass of base_class
        * A function that will be converted to base_class trough
          create_class method

    All items are registered using a name to uniquely identify them

    This register library is namespaced, so every new instance of it
    gets registered under the given namespace. This will avoid
    collisions between apps
    """
    namespace_separator = ':'

    def __init__(self, base_class, namespace):
        # global namespaced register
        if not hasattr(type(self), 'registers'):
            type(self).registers = {}

        # Register the instanced library
        if namespace in type(self).registers:
            raise ValueError("An namespace with name "
                             "'%s' is already registered" % namespace)

        type(self).registers[namespace] = self
        self.base_class = base_class
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
            return self._register_class
        elif isclass(name) and issubclass(name, self.base_class):
            return self._register_class(name)
        elif callable(name):
            res = self.create_class(name)
            res.__name__ = getattr(name, '_decorated_function', name).__name__
            return self._register_class(res)
        else:

            def dec(func):
                return self._register_class(func, name)

            return dec

    def _register_class(self, func, name=None):
        name = name or getattr(func, '_decorated_function', func).__name__
        self.items[name] = func
        return func

    def create_class(self, func):
        raise NotImplemented("This method should create a "
                             "classbased on a given function")
