from achilles.common import achilles_data


def redirect(request, url):
    """
    Log the given message to client's javascript console

    :param request: Django request object that is being served
    :param url: URL to go to
    """
    redirect = achilles_data(request, 'redirect', {})
    redirect['url'] = url


def render(request):
    return achilles_data(request, 'redirect', {})
