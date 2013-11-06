from django.http import HttpResponseBadRequest, HttpResponse

import json

from achilles.actions import run_actions, render_actions
from achilles.blocks import render_blocks


def endpoint(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    data = json.loads(request.body)
    run_actions(request, data)

    result = {
        'blocks': render_blocks(request),
        'actions': render_actions(request),
    }
    return HttpResponse(json.dumps(result), content_type="application/json")
