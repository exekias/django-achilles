from django.utils.translation import ugettext as _
from django.template import Context
from six import add_metaclass

from achilles import blocks
from achilles.tables.columns import Column


class Row(object):
    """
    Row object, item from a :class:`Table` bounded to it
    """
    def __init__(self, table, obj):
        """
        :param table: Table this Row belongs to
        :param obj: Object to show in this row
        """
        self.table = table
        self.obj = obj
        self.id = getattr(obj, table.id_field)

    def cells(self):
        """
        List of :class:`Cell` objects sorted by column order
        """
        for col in self.table.columns():
            yield Cell(self.table, col, self.obj)

    def __iter__(self):
        return self.cells()


class Cell(object):
    """
    Cell object, item from a :class:`Row` showing the data
    for a :class:`Column`
    """
    def __init__(self, table, column, obj):
        """
        :param table: Table this cell belongs to
        :param column: Column within the table this cell belongs to
        :param obj: Object to show in this cell
        """
        self.table = table
        self.column = column
        self.obj = obj

    def render(self):
        return self.column.render(self.obj)


class TableMeta(type):
    """
    Table metaclass, it calls contribute_to_class to column fields during
    class creation
    """
    def __new__(meta, name, bases, attrs):
        cls = super(TableMeta, meta).__new__(meta, name, bases, attrs)

        for column_name, column in attrs.items():
            if not isinstance(column, Column):
                continue
            column.contribute_to_class(cls, column_name)

        return cls


@add_metaclass(TableMeta)
class Table(blocks.Block):
    """
    Table block, displays a table of elements
    """
    #: Template file
    template_name = 'achilles/table.html'

    #: Text to show when no items
    empty_text = _('This list is empty')

    #: Django model to read the objects from
    model = None

    #: ID field for non-model objects
    id_field = 'id'

    def __init__(self, context=Context()):
        context.update({'table': self})
        super(Table, self).__init__(context)

    def objects(self, *args, **kwargs):
        if self.model:
            return self.model.objects.all()
        else:
            raise NotImplementedError('You should implement this method or '
                                      'define model field')

    def get_object(self, id):
        """
        Return a table object from its unique object id
        """
        if self.model:
            return self.model.objects.get(id=id)
        else:
            raise NotImplementedError('You should implement this method or '
                                      'define model field')

    def rows(self):
        """
        Generator over :class:`Row` elements for each item in object list
        """
        for obj in self.objects():
            yield Row(self, obj)

    def columns(self):
        """
        List of :class:`Column` elements defined for this table
        """
        cols = []
        for c in dir(self):
            c = getattr(self, c)
            if isinstance(c, Column):
                cols.append(c)

        # We are not caching this because column number should be low enough
        cols.sort(key=lambda col: col.creation_counter)
        return cols
