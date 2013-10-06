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

    def test_register_block1(self):
        @self.register.block()
        class MyBlock(blocks.Block):
            template_name = 'template'

        self.assertIsInstance(self.register.get('MyBlock'), MyBlock)

    def test_register_block2(self):
        @self.register.block
        class MyBlock(blocks.Block):
            template_name = 'template'

        self.assertIsInstance(self.register.get('MyBlock'), MyBlock)

    def test_register_block3(self):
        @self.register.block('new_name')
        class MyBlock(blocks.Block):
            template_name = 'template'

        self.assertIsInstance(self.register.get('new_name'), MyBlock)

    def test_register_simple_block(self):
        @self.register.simple_block('template')
        def foo(context):
            return {}

        self.assertIsInstance(self.register.get('foo'), blocks.Block)

    def test_block_get(self):
        @self.register.simple_block('block_template.html')
        def message(request):
            return {'message': 'foo'}

        self.assertIsInstance(blocks.get('message'), blocks.Block)

    def test_block_namespaces(self):
        register = blocks.Library('foo')
        @register.simple_block('block_template.html')
        def message(request):
            return {'message': 'foo'}

        self.assertIsInstance(blocks.get('foo:message'), blocks.Block)

    def test_render_block(self):
        @self.register.simple_block('block_template.html')
        def message(request):
            return {'message': 'foo'}

        out = Template(
            "{% load ablock %}"
            "{% ablock 'message' %}").render(Context())

        self.assertEqual(out, '<div data-ablock="name">foo\n</div>')
