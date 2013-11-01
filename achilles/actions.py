from django.conf import settings
from django.utils.log import getLogger
from importlib import import_module

from achilles.common import BaseLibrary

logger = getLogger(__name__)


class Library(BaseLibrary):
    """
    Actions register library
    """
    def __init__(self, namespace=None):
        BaseLibrary.__init__(self, namespace)

        # Provide action register
        self.action = self.register


def get(name):
    """
    Return action function for the given name
    """
    # make sure all actions are loaded
    for app in settings.INSTALLED_APPS:
        try:
            import_module(app + '.actions')
        except ImportError:
            pass

    return Library.get_global(name)
