from importlib import import_module

from achilles import backend
from achilles.common import BaseLibrary, achilles_data


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
    for module in backend.action_modules():
        try:
            import_module(module)
        except ImportError:
            pass

    return Library.get_global(name)


def run_actions(request, actions):
    """
    Run the given list of actions sent by the client
    """
    data = achilles_data(request, 'actions', {})
    for a in actions:
        name = a['name']
        action = get(name)

        # run and save return value
        try:
            result = action(request, *a.get('args', []), **a.get('kwargs', {}))
            data[a['id']] = {
                'value': result
            }
        except Exception as e:
            # Mark as error
            data[a['id']] = {
                'error': e.__class__.__name__,
                'message': str(e),
            }


def render(request):
    return achilles_data(request, 'actions', [])
