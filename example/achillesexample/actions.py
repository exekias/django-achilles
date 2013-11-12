from achilles import actions

register = actions.Library('example')

@register.action
def multiply(request, a, b):
    return float(a) * float(b)

@register.action
def divide(request, a, b):
    return float(a) / float(b)
