from achilles import blocks
from achilles import tables

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

    a = tables.Column('a')
    b = tables.Column('b')

    def objects(self):
        return [
            { 'a': 'hello', 'b': 3 },
            { 'a': 'world', 'b': 4 },
        ]
