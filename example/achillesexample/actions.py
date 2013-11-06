from achilles import actions

register = actions.Library('example')

@register.action
def multiply(request, a, b):
    return int(a) * int(b)
