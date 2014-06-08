from django.test import RequestFactory
from django.test import TestCase

from achilles.common import AchillesTransport
from achilles import actions


class ActionsTests(TestCase):

    @classmethod
    def setupClass(cls):
        cls.register = actions.Library()

    def setUp(self):
        request = RequestFactory().get('/path')
        self.transport = AchillesTransport(request)

    def test_run_function_action(self):
        @self.register.action
        def action(request):
            return 10

        a = actions.get('action')
        self.assertEqual(a, action)
        self.assertEqual(10, a(self.transport))

    def test_run_actions(self):
        @self.register.action
        def action(request, param=13):
            return param

        actions.run_actions(self.transport, [
            {
                'name': 'action',
                'id': '1',
            },
            {
                'name': 'action',
                'id': '2',
                'args': [2],
            },
            {
                'name': 'action',
                'id': '3',
                'kwargs': {'param': 33},
            },
        ])

        data = actions.render(self.transport)

        self.assertEqual(data["1"]["value"], 13)
        self.assertEqual(data["2"]["value"], 2)
        self.assertEqual(data["3"]["value"], 33)

    def test_run_actions_error(self):
        @self.register.action
        def action(request):
            raise ValueError('foo')

        actions.run_actions(self.transport, [
            {
                'name': 'action',
                'id': '1',
            },
        ])

        data = actions.render(self.transport)

        self.assertEqual(data["1"]["error"], 'ValueError')
        self.assertEqual(data["1"]["message"], 'foo')
