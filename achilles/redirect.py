def redirect(transport, url):
    """
    Log the given message to client's javascript console

    :param transport: Achilles tranport object that is being served
    :param url: URL to go to
    """
    redirect = transport.data('redirect', {})
    redirect['url'] = url


def render(transport):
    return transport.data('redirect', {})
