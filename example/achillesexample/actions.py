from achilles import actions
from achilles import console

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
