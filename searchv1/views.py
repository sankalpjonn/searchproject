from django.shortcuts import render
from search import *
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from models import Image
import json
import redis
from process_images import ProcessFiles
from decorators import throttling
# Create your views here.

@csrf_exempt
def search(request):
    if not request.user.is_authenticated():
        return HttpResponse(json.dumps({"status": "failure","message": "user not logged in"}, indent=4, sort_keys=True), content_type="application/json")
    s = Search(source=request.GET.get("source"), limit=int(request.GET.get("limit", 5)))
    response = s.run_search(request.GET.get("q"))
    return HttpResponse(json.dumps(response, indent=4, sort_keys=True), content_type="application/json")


@csrf_exempt
def userlogin(request):
    data = json.loads(request.body)
    user = authenticate(username=data.get("username"), password=data.get("password"))
    if user:
        login(request, user)
        return HttpResponse(json.dumps({"status": "success"}, indent=4, sort_keys=True), content_type="application/json")
    return HttpResponse(json.dumps({"status": "failure", "message": "Incorrect username/password"}, indent=4, sort_keys=True), content_type="application/json")


@csrf_exempt
@throttling(10, 5)
def fetch_images(request):
    import pdb; pdb.set_trace()
    if not request.user.is_authenticated():
        return HttpResponse(json.dumps({"status": "failure","message": "user not logged in"}, indent=4, sort_keys=True), content_type="application/json")
    data = json.loads(request.body)
    p = ProcessFiles(data['images'])
    res = p.run()
    return HttpResponse(json.dumps({"status": "success", "result": res}, indent=4, sort_keys=True), content_type="application/json")
