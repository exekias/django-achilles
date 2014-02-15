from achilles import blocks, tables

from models import Person

register = blocks.Library('example')

COUNTER = 0

@register.block(template_name='blocks/counter.html')
def counter():
    global COUNTER
    COUNTER += 1
    return {
        'counter' : COUNTER,
    }

@register.block('mytable')
class Table(tables.Table):

    a = tables.Column('first_name')
    b = tables.Column('last_name')

    model = Person
