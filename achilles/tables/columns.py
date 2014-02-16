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
    def __init__(self, verbose_name=None,
                 accessor=default_accessor):
        """
        :param verbose_name: Column human-readable name
        :param accessor: Function to access get data from the object
        """
        self.verbose_name = verbose_name
        self.accessor = accessor

    def contribute_to_class(self, table, name):
        self.name = name
        self.verbose_name = self.verbose_name or name
        self.table = table

    def render(self, obj):
        """
        Render column value for the given object

        :param obj: Object to read the value from
        """
        return str(self.accessor(obj, self.name))


class ActionColumn(Column):
    """
    Action calling column, it will show a button that will can
    the given action on click, the action will get the item
    in the row as parameter
    """
    def __init__(self, action, *args, **kwargs):
        super(ActionColumn, self).__init__(*args, **kwargs)
        self.action = action

    def render(self, obj):
        return ("<a href=\"javascript:achilles.action('tables:call_action', " +
                "['%s', '%s', '%s'])\">%s</a>") % (self.table.register_name,
                                                   self.name, obj.id,
                                                   self.verbose_name)


@register.action
def call_action(request, table, action, id):
    context = RequestContext(request, {})
    table = blocks.get(table, context)
