from django.http import HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@require_http_methods(["GET"])
def ping(req):
    return HttpResponse()