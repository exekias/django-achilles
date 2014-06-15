from django.contrib import messages

from achilles import actions, blocks, console


register = actions.Library('example')

@register.action
def multiply(transport, a, b):
    messages.info(request, 'Multiplication done')
    return float(a) * float(b)

@register.action
def divide(transport, a, b):
    messages.info(request, 'Division done')
    return float(a) / float(b)

@register.action
def log(transport):
    messages.info(request, 'Check your browser console')
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
