from achilles import actions, blocks, console

register = actions.Library('example')

@register.action
def multiply(request, a, b):
    return float(a) * float(b)

@register.action
def divide(request, a, b):
    return float(a) / float(b)

@register.action
def log(request):
    console.log(request, "This is a message from the server!")

@register.action
def miau_person(request, table, person):
    person.last_name = 'Miau ' + person.last_name
    person.save()
    blocks.update(request, 'example:mytable')
