from django.utils.translation import ugettext as _
from django.template import Context

from achilles import blocks


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

    def cells(self):
        """
        List of :class:`Cell` objects sorted by column order
        """
        for col in self.table.columns():
            yield Cell(self.table, col, self.obj)

    def __iter__(self):
        return self.cells()


def default_accessor(object, name):
    """
    Extract the given field from an object in two different forms:

        * For dicts it will return: object[name]
        * For objects it will return: object.name

    :param object: Object to read the field from
    :param name: Field name to access on the object
    """
    try:
        return object[name]
    except KeyError:
        return getattr(object, name)


class Column(object):
    """
    Table column, extract information from objects and render it whitin the
    table
    """
    def __init__(self, name, verbose_name=None, accessor=default_accessor):
        """
        :param name: Field name to extract from objects
        :param verbose_name: Column human-readable name
        :param accessor: Function to access get data from the object
        """
        self.name = name
        self.verbose_name = verbose_name or name
        self.accessor = accessor

    def render(self, obj):
        """
        Render column value for the given object

        :param obj: Object to read the value from
        """
        return str(self.accessor(obj, self.name))


class Cell(object):
    """
    Cell object, item from a :class:`Row` showing the data
    for a :class:`Column`
    """
    template_name = 'achilles/table-row.html'

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

    def __init__(self, context=Context()):
        context.update({'table': self})
        super(Table, self).__init__(context)

    def objects(self, *args, **kwargs):
        if self.model:
            return self.model.objects.all()
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
        for c in dir(self):
            c = getattr(self, c)
            if isinstance(c, Column):
                yield c
