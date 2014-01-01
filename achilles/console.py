from achilles.common import achilles_data


def log(request, msg):
    """
    Log the given message to client's javascript console

    :param request: Django request object that is being served
    :param msg: Log message that will be pushed to the console
    """
    logs = achilles_data(request, 'console', [])
    logs.append(msg)


def render(request):
    return achilles_data(request, 'console', [])
