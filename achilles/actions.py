from django.conf import settings
from importlib import import_module

from achilles.common import BaseLibrary

import logging
import sys
import six
import traceback
import django.dispatch


logger = logging.getLogger(__name__)


class Library(BaseLibrary):
    """
    Action library holds a register of all defined actions

    Use it to define and register new actions, grouping them under
    a common namespace::

        from achilles import actions

        register = actions.Library('myapp')

        @register.action
        def foo(transport, *args, **kwargs):
            # do stuff
            pass

    :param namespace: Unique namespace for this register
    """
    def __init__(self, namespace=None):
        BaseLibrary.__init__(self, namespace)

        # Provide action register
        self.action = self.register


def get(name):
    """
    Retrieve an action function with the given name. Example::

        actions.get('myapp:foo')

    :param name: Fully namespaced action name
    """
    # make sure all actions are loaded
    for app in settings.INSTALLED_APPS:
        if six.PY2:
            try:
                import_module(app + '.actions')
            except ImportError:
                tb = sys.exc_info()[2]
                stack = traceback.extract_tb(tb, 3)
                if len(stack) > 2:
                    raise
        else:
            from importlib import find_loader
            if find_loader(app + '.actions'):
                import_module(app + '.actions')

    return Library.get_global(name)


#: Signal dispatched before executing client sent actions
pre_actions_call = django.dispatch.Signal(providing_args=['transport'])

#: Signal dispatched after executing client sent actions
post_actions_call = django.dispatch.Signal(providing_args=['transport'])


def run_actions(transport, actions):
    """
    Run the given list of actions sent by the client
    """
    pre_actions_call.send(transport, transport=transport)

    data = transport.data('actions', {})
    for a in actions:
        name = a['name']
        action = get(name)

        # run and save return value
        try:
            result = action(transport, *a.get('args', []), **a.get('kwargs', {}))
            data[a['id']] = {
                'value': result
            }
        except Exception as e:
            # Mark as error
            data[a['id']] = {
                'error': e.__class__.__name__,
                'message': str(e),
            }
            if settings.DEBUG:
                data[a['id']]['trace'] = traceback.format_exc()

            logger.exception("Error on %s action" % name)

    post_actions_call.send(transport, transport=transport)


def render(transport):
    return transport.data('actions', {})
