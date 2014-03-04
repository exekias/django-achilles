from django.template import Context

from achilles import blocks


class Form(blocks.Block):
    """
    Form block, display a formulary
    """
    #: Template file
    template_name = 'achilles/form.html'

    initial = {}
    form_class = None

    def __init__(self, context=Context()):
        super(Form, self).__init__(context)

    def get_initial(self):
        return self.initial.copy()

    def get_form(self, form_data=None, *args, **kwargs):
        return self.form_class(**self.get_form_kwargs())

    def get_form_kwargs(self, form_data=None, *args, **kwargs):
        kwargs = {
            'initial': self.get_initial(),
        }
        if form_data:
            kwargs['data'] = form_data
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(Form, self).get_context_data(*args, **kwargs)
        context.update({
            'form': self.get_form(*args, **kwargs),
        })
        return context

    def form_valid(self, form):
        raise NotImplemented("You should implement this method")

    def form_invalid(self, form):
        raise NotImplemented("You should implement this method")
