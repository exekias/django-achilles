from django.test import TestCase
from django.test import RequestFactory

from achilles import console


class ConsoleTests(TestCase):

    @classmethod
    def setupClass(cls):
        cls.request_factory = RequestFactory()

    def setUp(self):
        self.request = self.request_factory.get('/path')

    def test_console_log(self):

        console.log(self.request, 'test message')

        self.assertIn('test message', console.render(self.request))
