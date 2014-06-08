from django.test import TestCase
from django.test import RequestFactory

from achilles.common import AchillesTransport
from achilles import console


class ConsoleTests(TestCase):

    def setUp(self):
        request = RequestFactory().get('/path')
        self.transport = AchillesTransport(request)

    def test_console_log(self):

        console.log(self.transport, 'test message')

        self.assertIn('test message', console.render(self.transport))
