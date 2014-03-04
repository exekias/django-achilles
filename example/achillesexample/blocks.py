from django import forms as djforms

from achilles import blocks, forms, tables
from time import sleep

from .models import Person

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
    sleep(1)
    return {
        'message':'This block was loaded after page was loaded!',
    }

@register.block('mytable')
class Table(tables.Table):

    first_name = tables.Column(verbose_name='First name')
    last_name = tables.Column(verbose_name='First name')
    call_example = tables.ActionColumn(action='example:miau_person',
                                       verbose_name='Miauify')

    model = Person

class MyForm(djforms.Form):
    subject = djforms.CharField(max_length=100)
    message = djforms.CharField()
    sender = djforms.EmailField()
    cc_myself = djforms.BooleanField(required=False)

@register.block('myform')
class Form(forms.Form):
    form_class = MyForm
