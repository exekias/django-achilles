from django import forms as djforms

from achilles import blocks, forms, tables
from time import sleep

from .models import Person
from .actions import miau_person, delete_person

register = blocks.Library('example')

COUNTER = 0

@register.block(template_name='blocks/message.html')
def counter():
    global COUNTER
    COUNTER += 1
    return {
        'message': 'Block loaded %s times' % COUNTER,
    }

@register.block(template_name='blocks/message.html')
def slow():
    sleep(2)
    return {
        'message':'This block was loaded after page was loaded!',
    }

@register.block(template_name='blocks/message.html')
def with_args(index):
    MSG = { x:'This is the %s block' % x.upper() for x in ('a', 'b', 'c') }
    return {
        'message':MSG[index],
    }

@register.block('mytable')
class Table(tables.Table):

    first_name = tables.Column(verbose_name='First name')
    last_name = tables.Column(verbose_name='First name')
    call_example = tables.ActionColumn(action=miau_person,
                                       verbose_name='Miauify')
    call_example2 = tables.ActionColumn(action=delete_person,
                                        verbose_name='Delete')

    model = Person

class MyForm(djforms.Form):
    first_name = djforms.CharField()
    last_name = djforms.CharField()

@register.block('myform')
class Form(forms.Form):
    form_class = MyForm

    # Buttons
    reset = forms.ResetButton('Reset')
    send = forms.SubmitButton('Save')

    def form_valid(self, transport, form):
        Person.objects.get_or_create(**form.cleaned_data)
        blocks.update(transport, 'example:mytable')
