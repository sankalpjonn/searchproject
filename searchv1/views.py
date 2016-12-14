from django.shortcuts import render
from search import *
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


@csrf_exempt
def search(request):
    s = Search(source=request.GET.get("source"), limit=int(request.GET.get("limit", 5)))
    response = s.run_search(request.GET.get("q"))
    return HttpResponse(json.dumps(response, indent=4, sort_keys=True), content_type="application/json")
