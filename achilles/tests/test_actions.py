from django.test import RequestFactory
from django.test import TestCase

from achilles import actions


class ActionsTests(TestCase):

    @classmethod
    def setupClass(cls):
        cls.register = actions.Library()
        cls.request_factory = RequestFactory()

    def setUp(self):
        self.request = self.request_factory.get('/path')

    def test_run_function_action(self):
        @self.register.action
        def action(request):
            return 10

        a = actions.get('action')
        self.assertEqual(a, action)
        self.assertEqual(10, a(self.request))
