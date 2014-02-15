from django.test import TestCase
from django.template import Template, Context
from mock import MagicMock

from achilles import blocks, tables


class TablesTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.register = blocks.Library('tables')

    def setUp(self):
        self.p1 = MagicMock()
        self.p1.id = 1
        self.p1.first_name = 'Diego'
        self.p1.last_name = 'Rivera'

        self.p2 = MagicMock()
        self.p2.id = 2
        self.p2.first_name = 'Frida'
        self.p2.last_name = 'Kahlo'

        # mocked model
        self.person = MagicMock()
        self.person.objects.all.return_value = [self.p1, self.p2]

        # table
        @self.register.block()
        class People(tables.Table):
            model = self.person

            first_name = tables.Column('first_name')
            last_name = tables.Column('last_name')

    def test_access_cols(self):
        table = self.register.get('People')()
        self.assertEqual([c.name for c in table.columns()],
                         ['first_name', 'last_name'])

    def test_render_col(self):
        table = self.register.get('People')()
        column = next(table.columns())
        self.assertEqual(column.render(self.p1), 'Diego')

    def test_access_rows(self):
        table = self.register.get('People')()
        self.assertEqual(len(list(table.rows())), 2)

    def test_access_row_cells(self):
        table = self.register.get('People')()
        row2 = list(table.rows())[1]

        self.assertEqual([c.render() for c in row2.cells()],
                         ['Frida', 'Kahlo'])

    def test_render_table(self):
        out = Template(
            "{% load achilles %}"
            "{% ablock 'tables:People' %}").render(Context())

        # headers
        self.assertEqual(out.count('<th>'), 2)

        # Cell row
        self.assertTrue("Kahlo" in out)
