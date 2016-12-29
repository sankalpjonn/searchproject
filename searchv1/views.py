from django.shortcuts import render
from search import *
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from models import Image
import json
import redis
from process_images import ProcessFiles
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
def fetch_images(request):
    if not request.user.is_authenticated():
        return HttpResponse(json.dumps({"status": "failure","message": "user not logged in"}, indent=4, sort_keys=True), content_type="application/json")
    data = json.loads(request.body)
    r_server = redis.StrictRedis(host='localhost', port=6379, db=2)
    if not r_server.exists("THROT:{}".format(request.user)):
        r_server.incr("THROT:{}".format(request.user))
        r_server.expire("THROT:{}".format(request.user), 5 * 60 * 60)
    p = ProcessFiles(data['images'], request.user, 100, r_server)
    res = p.run()
    return HttpResponse(json.dumps({"status": "success", "result": res}, indent=4, sort_keys=True), content_type="application/json")
