from achilles import blocks
from time import sleep


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
