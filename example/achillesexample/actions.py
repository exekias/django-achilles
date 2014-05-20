from django.contrib import messages

from achilles import actions, blocks, console


register = actions.Library('example')

@register.action
def multiply(request, a, b):
    messages.info(request, 'Multiplication done')
    return float(a) * float(b)

@register.action
def divide(request, a, b):
    messages.info(request, 'Division done')
    return float(a) / float(b)

@register.action
def log(request):
    messages.info(request, 'Check your browser console')
    console.log(request, "This is a message from the server!")

@register.action
def miau_person(request, table, person):
    person.last_name = 'Miau ' + person.last_name
    person.save()
    blocks.update(request, 'example:mytable')

@register.action
def delete_person(request, table, person):
    person.delete()
    blocks.update(request, 'example:mytable')
