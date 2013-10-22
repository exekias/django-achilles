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
        BaseLibrary.__init__(self, Action, namespace)

        # Provide action register
        self.action = self.register

    def create_class(self, func):
        class A(Action):
            def run(self):
                return func(self.request, *self.args, **self.kwargs)
        return A


def get(name):
    """
    Return action function for the given name
    """
    # make sure all actions are loaded
    for app in settings.INSTALLED_APPS:
        try:
            import_module(app + '.actions')
        except:
            pass

    return Library.get_global(name)


class Action(object):
    """
    Block section, defines a block in the page. template_name instance field
    should be defined, so render method will use it in conjunction with
    get_context_data
    """

    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs

    def run(self):
        raise NotImplemented('This method should process the action')
