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

        # Register merged columsn under invisible namespace:
        for (cname, column) in self.columns:
            subname = '_' + name + '_' + cname
            setattr(table, subname, column)
            column.contribute_to_class(table, subname)

    def content(self, obj):
        return ' '.join([c.render(obj) for (n, c) in self.columns])


class ButtonColumn(Column):
    """
    Button column, just a link to the given href
    """
    def __init__(self, href='#', classes='', *args, **kwargs):
        super(ButtonColumn, self).__init__(*args, **kwargs)
        self.href = href
        self.classes = classes

    def get_href(self):
        return self.href

    def content(self, obj):
        return ("<a class=\"%s\" href=\"%s\">%s</a>") % (
            self.classes, self.get_href(obj), self.verbose_name)


class ActionColumn(ButtonColumn):
    """
    Action calling column, it will show a button that will can
    the given action on click, the action will get the the table
    and object in the row as arguments
    """
    def __init__(self, action, classes='', *args, **kwargs):
        super(ActionColumn, self).__init__(classes=classes, *args, **kwargs)
        self.action = action

    def call(self, *args, **kwargs):
        return self.action(*args, **kwargs)

    def get_href(self, obj):
        id_field = self.table.id_field
        return ("javascript:achilles.action("
                "'tables:row_action', ['%s', '%s', '%s'])") % (
            self.table.register_name, self.name, getattr(obj, id_field))


@register.action
def table_action(transport, table_name, action_name, *args, **kwargs):
    """
    Call table action

    :param transport: achilles transport
    :param table_name: Name of the table calling this
    :param action_name: Name of the action to call
    """
    # Get TableAction item
    context = RequestContext(transport.request, {})
    table = blocks.get(table_name, context)
    action = getattr(table, action_name)

    # Call the action
    res = action.call(transport, table, *args, **kwargs)
    blocks.update(transport, table.register_name)
    return res


@register.action
def row_action(transport, table_name, action_name, row_id, *args, **kwargs):
    """
    Call table action on the given row

    :param transport: achilles transport
    :param table_name: Name of the table calling this
    :param action_name: Name of the action to call
    :param row_id: Id of the object
    """
    # Get TableAction item
    context = RequestContext(transport.request, {})
    table = blocks.get(table_name, context)
    action = getattr(table, action_name)

    # Get the object from the row
    obj = table.get_object(row_id)

    # Call the action
    res = action.call(transport, table, obj, *args, **kwargs)
    blocks.update(transport, table.register_name)
    return res
