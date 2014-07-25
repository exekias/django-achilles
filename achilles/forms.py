from django.template import Context
try:
    from django.http.request import QueryDict
except ImportError:
    from django.http import QueryDict

from achilles import blocks, actions

import json


register = actions.Library('forms')


class Button(object):
    """
    Form button, execute some action on the specific form
    """
    creation_counter = 0

    def __init__(self, verbose_name=None, type='submit',
                 classes=''):
        """
        :param verbose_name: User visible name
        :param type: Button type (submit, button, reset)
        :param classes: CSS classes to apply
        """
        Button.creation_counter += 1
        self.creation_counter = Button.creation_counter
        self.verbose_name = verbose_name
        self.classes = classes
        self.type = type

    def render(self):
        return '<button type="%s" class="%s">%s</button>' % \
               (self.type, self.classes, self.verbose_name)


class SubmitButton(Button):
    """
    Form submit button
    """
    def __init__(self, verbose_name=None,
                 classes='btn btn-primary', **kwargs):
        super(SubmitButton, self).__init__(verbose_name, type='submit',
                                           classes=classes, **kwargs)


class ResetButton(Button):
    """
    Form reset button
    """
    def __init__(self, verbose_name=None,
                 classes='btn btn-link', **kwargs):
        super(ResetButton, self).__init__(verbose_name, type='reset',
                                          classes=classes, **kwargs)


class Form(blocks.Block):
    """
    Form block, display a form, see action func:`send` for submitting
    """
    #: Template file
    template_name = 'achilles/form.html'

    initial = {}
    form_class = None

    def __init__(self, context=Context()):
        super(Form, self).__init__(context)
        self._form = None

    def get_initial(self):
        return self.initial.copy()

    def get_form(self, form_data=None, *args, **kwargs):
        if not self._form:
            if self.form_class is None:
                raise ValueError("form_class is undefined %s" %
                                 type(self).__name__)
            self._form = self.form_class(data=form_data,
                                         **self.get_form_kwargs(*args,
                                                                **kwargs))
        return self._form

    def get_form_kwargs(self, *args, **kwargs):
        instance = self.get_instance(*args, **kwargs)
        kwargs = {
            'initial': self.get_initial(),
        }
        if instance:
            kwargs['instance'] = instance

        return kwargs

    def get_instance(self, *args, **kwargs):
        """
        Return a instance object to pass to the form constructor
        """
        return None

    def get_context_data(self, *args, **kwargs):
        context = super(Form, self).get_context_data(*args, **kwargs)
        context.update({
            'formblock': self,
            'form': self.get_form(None, *args, **kwargs),
            'args': json.dumps(args),
            'kwargs': json.dumps(kwargs),
        })
        return context

    def buttons(self):
        """
        List of :class:`Button` elements defined for this form
        """
        buttons = []
        for b in dir(self):
            if not b.startswith('_'):
                b = getattr(self, b)
                if isinstance(b, Button):
                    buttons.append(b)

        # We are not caching this because column number should be low enough
        buttons.sort(key=lambda btn: btn.creation_counter)
        return buttons

    def form_valid(self, transport, form, *args, **kwargs):
        raise NotImplementedError("You should implement this method")

    def form_invalid(self, transport, form, *args, **kwargs):
        """
        Update the form with error messages
        """
        self.update(transport)


class ModelForm(Form):
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

    def form_valid(self, transport, form, *args, **kwargs):
        form.save()


@register.action
def send(transport, form, args=[], kwargs={}, data={}):
    """
    Validate a form and call the proper callback Form.form_valid
    or Form.form_invalid

    :param transport: Achilles transport object
    :param form: Form block name
    :param data: Serialized form data
    :returns: True if the form was valid, False if not
    """
    block = blocks.get(form)
    data = QueryDict(data, encoding=transport.encoding)
    form = block.get_form(data, *args, **kwargs)

    if form.is_valid():
        block.form_valid(transport, form, *args, **kwargs)
        return True
    else:
        block.form_invalid(transport, form, *args, **kwargs)
        return False
