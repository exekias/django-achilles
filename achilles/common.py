class BaseLibrary(object):
    """
    Base register library, provides decorator functions to register
    items on it
    """
    def __init__(self):
        self.items = {}

    def get(self, name):
        if name not in self.items:
            raise KeyError("'%s' item doesn't exists" % name)
        return self.items[name]

    def _register(self, name=None, compile_function=None):
        if name is None:
            # @register.item()
            return self._register_function
        elif name is not None and compile_function is None:
            if callable(name):
                # @register.item
                return self._register_function(name)
            else:
                # @register.item('somename') @register.item(name='somename')
                def dec(func):
                    return self._register(name, func)
                return dec
        elif name is not None and compile_function is not None:
            # register.item('somename', somefunc)
            self.items[name] = compile_function
            return compile_function
        else:
            raise ValueError(
                "Unsupported arguments to "
                "Library.item: (%r, %r)", (name, compile_function))

    def _register_function(self, func):
        self.items[getattr(func, "_decorated_function", func).__name__] = func
        return func
