from achilles import actions, blocks, console

register = actions.Library('example')

@register.action
def multiply(transport, a, b):
    return float(a) * float(b)

@register.action
def divide(transport, a, b):
    return float(a) / float(b)

@register.action
def log(transport):
    console.log(transport, "This is a message from the server!")

@register.action
def miau_person(transport, table, person):
    person.last_name = 'Miau ' + person.last_name
    person.save()
    blocks.update(transport, 'example:mytable')

@register.action
def delete_person(transport, table, person):
    person.delete()
    blocks.update(transport, 'example:mytable')
