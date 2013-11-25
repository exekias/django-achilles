__version__ = (0, 0, 5)


def get_version(*args, **kwargs):
    return '.'.join([str(x) for x in __version__])

# Static init of current backend
from backends.django_backend import DjangoBackend
backend = DjangoBackend()
