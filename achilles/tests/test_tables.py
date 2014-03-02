from django.test import TestCase
from django.template import Template, Context
from mock import Mock, MagicMock

from achilles import blocks, tables


class TablesTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.register = blocks.Library('tables')

    def setUp(self):
        self.p1 = Mock(id=1, first_name='Diego', last_name='Rivera')
        self.p2 = Mock(id=2, first_name='Frida', last_name='Kahlo')

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
        column = table.columns()[0]
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
        self.assertEqual(out.count('<th '), 2)

        # Cell row
        self.assertTrue("Kahlo" in out)

    def test_action_column(self):
        column = tables.ActionColumn('foobar:action', verbose_name='doit!')
        column.table = Mock(register_name='foobar:table', id_field='id')

        obj = Mock(id=2)
        column_text = ("<a href=\"javascript:achilles.action"
                       "('tables:call_action', ['foobar:table', "
                       "'foobar:action', '2'])\">doit!</a>")

        self.assertEqual(column.render(obj), column_text)
