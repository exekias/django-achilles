from django.template import RequestContext

from achilles import blocks, actions


register = actions.Library('tables')


def default_accessor(object, name):
    """
    Extract the given field from a model:

    :param object: Object to read the field from
    :param name: Field name to access on the object
    """
    return getattr(object, name)


class Column(object):
    """
    Table column, extract information from objects and render it whitin the
    table
    """
    # Creation counter used to retrieve original column order
    creation_counter = 0

    def __init__(self, verbose_name=None,
                 accessor=default_accessor,
                 visible=lambda x: True):
        """
        :param verbose_name: Column human-readable name
        :param accessor: Function to access get data from the object
        :param visible: Function giving visibility flag for the given row
        """
        self.creation_counter = Column.creation_counter
        Column.creation_counter += 1

        self.verbose_name = verbose_name
        self.accessor = accessor
        self.visible = visible

    def contribute_to_class(self, table, name):
        self.name = name
        self.verbose_name = self.verbose_name or name
        self.table = table

    def render(self, obj):
        """
        Dump cell for the given object
        """
        if self.visible(obj):
            return self.content(obj)
        else:
            return ''

    def content(self, obj):
        """
        Render column value for the given object

        :param obj: Object to read the value from
        """
        return str(self.accessor(obj, self.name))


class MergeColumn(Column):
    """
    Merge some columns under the same cell
    """
    def __init__(self, columns, *args, **kwargs):
        """
        :param columns: Tuple of name, column pairs for all merged
            columns to show
        """
        super(MergeColumn, self).__init__(*args, **kwargs)
        self.columns = columns

    def contribute_to_class(self, table, name):
        super(MergeColumn, self).contribute_to_class(table, name)

        for (name, column) in self.columns:
            column.contribute_to_class(table, name)

    def content(self, obj):
        return ' '.join([c.render(obj) for (n, c) in self.columns])


class ActionColumn(Column):
    """
    Action calling column, it will show a button that will can
    the given action on click, the action will get the the table
    and object in the row as arguments
    """
    def __init__(self, action, classes='', *args, **kwargs):
        super(ActionColumn, self).__init__(*args, **kwargs)
        self.action = action
        self.classes = classes

    def content(self, obj):
        id_field = self.table.id_field
        return ("<a class=\"%s\" href=\"javascript:achilles.action("
                "'tables:call_action', ['%s', '%s', '%s'])\">%s</a>") % (
            self.classes, self.table.register_name, self.action,
            getattr(obj, id_field), self.verbose_name)


@register.action
def call_action(request, table, action, id):
    """
    Call table action on the given row

    :param request: The client request
    :param table: Name of the table calling this
    :param action: Name of the action to call
    :param id: Id of the object
    """
    context = RequestContext(request, {})
    table = blocks.get(table, context)
    obj = table.get_object(id)
    action = actions.get(action)
    action(request, table, obj)
