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

    first_name = tables.Column()
    last_name = tables.Column()
    call_example = tables.ActionColumn(action='example:counter',
                                       verbose_name='miau')

    model = Person
