import os

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
        self.assertEqual(10, a(self.request).run())

    def test_run_class_action(self):
        @self.register.action('classaction')
        class AnAction(actions.Action):
            def run(self):
                return 10

        a = actions.get('classaction')
        self.assertEqual(a, AnAction)
        self.assertEqual(10, a(self.request).run())
