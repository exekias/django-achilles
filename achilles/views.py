from django.http import HttpResponseBadRequest, HttpResponse

import json

from .blocks import render_blocks
import actions


def endpoint(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    data = json.loads(request.body)
    for a in data:
        name = a['name']
        action = actions.get(name)
        action(request, *a.get('args', []), **a.get('kwargs', {}))

    result = {
        'blocks': render_blocks(request),
    }
    return HttpResponse(json.dumps(result), content_type="application/json")
