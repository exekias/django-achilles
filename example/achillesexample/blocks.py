from achilles import blocks

register = blocks.Library('example')

COUNTER = 0

@register.block(template_name='blocks/counter.html')
def counter():
    global COUNTER
    COUNTER += 1
    return {
        'counter' : COUNTER,
    }
