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

    def test_register_block1(self):
        @blocks.register.block()
        class MyBlock(blocks.ZBlock):
            template_name = 'template'

        self.assertEqual(blocks.register.get('MyBlock'), MyBlock)

    def test_register_block2(self):
        @blocks.register.block
        class MyBlock(blocks.ZBlock):
            template_name = 'template'

        self.assertEqual(blocks.register.get('MyBlock'), MyBlock)

    def test_register_block3(self):
        @blocks.register.block('new_name')
        class MyBlock(blocks.ZBlock):
            template_name = 'template'

        self.assertNotIn(MyBlock, blocks.register.blocks)
        self.assertEqual(blocks.register.get('new_name'), MyBlock)

    def test_register_simple_block(self):
        @blocks.register.simple_block('template')
        def foo(context):
            return {}

        self.assertIn('foo', blocks.register.blocks)

    def test_render_block(self):
        @blocks.register.simple_block('block_template.html')
        def message(request):
            return {'message': 'foo'}

        out = Template(
            "{% load ablock %}"
            "{% ablock 'message' %}").render(Context())

        self.assertEqual(out, '<div data-ablock="name">foo\n</div>')
