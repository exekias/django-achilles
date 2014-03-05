from achilles import blocks, tables
from time import sleep

from models import Person

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
    call_example2 = tables.ActionColumn(action='example:delete_person',
                                        verbose_name='Delete')

    model = Person
