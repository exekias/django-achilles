def log(transport, msg):
    """
    Log the given message to client's javascript console

    :param transport: Achilles transport object that is being served
    :param msg: Log message that will be pushed to the console
    """
    transport.data('console', []).append(msg)


def render(transport):
    return transport.data('console', [])
