from unittest import TestCase
from achilles import blocks


class BlocksTests(TestCase):

    def setUp(self):
        self.register = blocks.Library()

    def test_register_initially_empty(self):
        self.assertEqual(len(self.register.blocks), 0)

    def test_register_block1(self):
        @self.register.block()
        class MyBlock(blocks.ZBlock):
            template_name = 'template'

        self.assertEqual(self.register.blocks['MyBlock'], MyBlock)

    def test_register_block2(self):
        @self.register.block
        class MyBlock(blocks.ZBlock):
            template_name = 'template'

        self.assertEqual(self.register.blocks['MyBlock'], MyBlock)

    def test_register_block3(self):
        @self.register.block('new_name')
        class MyBlock(blocks.ZBlock):
            template_name = 'template'

        self.assertNotIn(MyBlock, self.register.blocks)
        self.assertEqual(self.register.blocks['new_name'], MyBlock)

    def test_register_simple_block(self):
        @self.register.simple_block('template')
        def foo(request):
            return {}

        self.assertEqual(len(self.register.blocks), 1)
        self.assertIn('foo', self.register.blocks)
