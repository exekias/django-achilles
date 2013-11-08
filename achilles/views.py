from django.http import HttpResponseBadRequest, HttpResponse

from achilles.common import achilles_renders
from achilles.actions import run_actions

import json


def endpoint(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    data = json.loads(request.body)
    run_actions(request, data)

    result = {}
    for (namespace, render) in achilles_renders().iteritems():
        result[namespace] = render(request)

    return HttpResponse(json.dumps(result), content_type="application/json")
