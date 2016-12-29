import redis
import json
from django.http import HttpResponse

def throttling(r_server, time_period, limit):
    def real_decorator(f):
        def wrapper(request):
            if not r_server.exists("THROT:{}".format(request.user)):
                r_server.incr("THROT:{}".format(request.user))
                r_server.expire("THROT:{}".format(request.user), time_period * 60 * 60)
            else:
                print "incrementing counter"
                r = r_server.incr("THROT:{}".format(request.user))
                print r, limit
                if r > limit:
                    return HttpResponse(json.dumps({"status": "failure", "message": "throttle rate exceeded"}))
            x = f(request)
            return x
        return wrapper
    return real_decorator
