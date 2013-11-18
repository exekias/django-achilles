from achilles.common import achilles_data


def log(request, msg):
    """
    Log the given message to javascript console
    """
    logs = achilles_data(request, 'console', [])
    logs.append(msg)


def render(request):
    return achilles_data(request, 'console', [])
