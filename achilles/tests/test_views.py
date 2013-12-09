from django.test import RequestFactory, TestCase
from django.conf import settings

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
        data = json.loads(result.content.decode(settings.DEFAULT_CHARSET))

        self.assertEqual(set(achilles_plugins().keys()), set(data.keys()))
