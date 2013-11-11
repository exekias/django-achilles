from django.test import RequestFactory
from django.test import TestCase

from achilles.common import achilles_plugins
from achilles.views import endpoint

import json


class ActionsTests(TestCase):

    @classmethod
    def setupClass(cls):
        cls.request_factory = RequestFactory()

    def setUp(self):
        self.request = self.request_factory.post(
            '/path', data='[]',
            content_type='application/octet-stream')

    def test_json_endpoint(self):
        result = endpoint(self.request)
        data = json.loads(result.content)

        self.assertListEqual(achilles_plugins().keys(), data.keys())
