from django.test import TestCase
from django.test.utils import override_settings

from django.template import Template, Context
from django.conf.urls import patterns, url, include

urlpatterns = patterns('', url(r'^achilles$', include('achilles.urls')),)


@override_settings(
    STATIC_URL='',
    ROOT_URLCONF='achilles.tests.test_templatetags',
)
class BlocksTests(TestCase):

    def test_achilles_js(self):

        out = Template("{% load achilles %}"
                       "{% achilles_js %}").render(Context())
        self.assertEqual(out, '<script src="js/achilles.js">' +
                              '</script>\n<script type="text/javascript">' +
                              'achilles = Achilles(\'/achilles\')</script>')
