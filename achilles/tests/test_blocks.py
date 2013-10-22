import os

from django.test import TestCase
from django.test.utils import override_settings
from django.template import Template, Context

from achilles import blocks


@override_settings(
    TEMPLATE_DIRS=(os.path.join(os.path.dirname(__file__), 'templates/'),),
    TEMPLATE_LOADERS=('django.template.loaders.filesystem.Loader',),
)
class BlocksTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.register = blocks.Library()

    def test_render_function_block(self):
        @self.register.block(template_name='block_template.html')
        def message():
            return {'message': 'foo'}

        out = Template(
            "{% load achilles %}"
            "{% ablock 'message' %}").render(Context())

        self.assertEqual(out, '<div data-ablock="message">foo\n</div>')

    def test_render_function_block_with_context(self):
        @self.register.block(template_name='block_template.html',
                             takes_context=True)
        def message(context):
            return {'message': 'foo'}

        out = Template(
            "{% load achilles %}"
            "{% ablock 'message' %}").render(Context())
        self.assertEqual(out, '<div data-ablock="message">foo\n</div>')

    def test_render_class_block(self):
        @self.register.block('message')
        class Message(blocks.Block):
            template_name = 'block_template.html'

            def get_context_data(self, *args, **kwargs):
                context = super(Message, self).get_context_data(*args,
                                                                **kwargs)
                context.update({'message': 'foo'})
                return context

        out = Template(
            "{% load achilles %}"
            "{% ablock 'message' %}").render(Context())

        self.assertEqual(out, '<div data-ablock="message">foo\n</div>')
