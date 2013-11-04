from achilles import blocks

register = blocks.Library('counter')

counter = 0

@register.block(template_name='blocks/counter.html')
def simple():
    global counter
    counter += 1
    return {
        'counter' : counter,
    }
