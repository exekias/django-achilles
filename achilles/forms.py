from django.template import Context
try:
    from django.http.request import QueryDict
except ImportError:
    from django.http import QueryDict

from achilles import blocks, actions
import json


register = actions.Library('forms')


class FormBlock(blocks.Block):
    """
    Form block, display a form, see action func:`send` for submitting
    """
    #: Template file
    template_name = 'achilles/form.html'

    initial = {}
    form_class = None

    def __init__(self, context=Context()):
        super(FormBlock, self).__init__(context)
        self._form = None

    def get_initial(self):
        return self.initial.copy()

    def get_form(self, form_data=None, *args, **kwargs):
        if not self._form:
            if self.form_class is None:
                raise ValueError("form_class is undefined %s" %
                                 type(self).__name__)
            self._form = self.form_class(data=form_data,
                                         **self.get_form_kwargs())
        return self._form

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = {
            'initial': self.get_initial(),
        }
        instance = self.get_instance(*args, **kwargs)
        if instance:
            kwargs['instance'] = instance

        return kwargs

    def get_instance(self, *args, **kwargs):
        """
        Return a instance object to pass to the form constructor
        """
        return None

    def get_context_data(self, *args, **kwargs):
        context = super(FormBlock, self).get_context_data(*args, **kwargs)
        context.update({
            'formblock': self,
            'form': self.get_form(None, *args, **kwargs),
            'args': json.dumps(args),
            'kwargs': json.dumps(kwargs),
        })
        return context

    def form_valid(self, transport, form):
        raise NotImplementedError("You should implement this method")

    def form_invalid(self, transport, form):
        """
        Update the form with error messages
        """
        self.update(transport)


class ModelFormBlock(FormBlock):
    """
    Wraps a Model Form, this class will automatically retrieve instance model
    from an id block attribute and process form_valid event (saving the object)

    form_class field must be a class:`django.forms.ModelForm`
    """
    def get_form(self, form_data=None, id=None, *args, **kwargs):
        instance = None
        if id:
            instance = self.form_class.Meta.model.objects.get(id=id)

        return self.form_class(form_data, instance=instance)

    def form_valid(self, transport, form):
        form.save()


@register.action
def send(transport, form, args=[], kwargs={}, data={}):
    """
    Validate a form and call the proper callback FormBlock.form_valid
    or FormBlock.form_invalid

    :param transport: Achilles transport object
    :param form: Form block name
    :param data: Serialized form data
    :returns: True if the form was valid, False if not
    """
    block = blocks.get(form)
    data = QueryDict(data, encoding=transport.encoding)
    form = block.get_form(data, *args, **kwargs)

    if form.is_valid():
        block.form_valid(transport, form)
        return True
    else:
        block.form_invalid(transport, form)
        return False
