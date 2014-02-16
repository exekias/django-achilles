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


class ActionColumn(Column):
    """
    Action calling column, it will show a button that will can
    the given action on click, the action will get the item
    in the row as parameter
    """
    def render(self, obj):
        return "Action!"
