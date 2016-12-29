import requests
import urllib
import json
from multiprocessing import Process, Queue
import threading
from requests_oauthlib import OAuth1
import os
import sys
import string
import random
from models import Image
from subprocess import check_output
from django.db import IntegrityError


class ProcessFiles():
    def __init__(self, images, username, throttle_rate, r_server):
        self.images = images
        self.username = username
        self.q = Queue()
        self.throttle_rate = throttle_rate
        self.r_server = r_server

    def save_image(self, url):
        # import pdb; pdb.set_trace()
        lst = [random.choice(string.ascii_letters + string.digits) for n in xrange(40)]
        local_filename = "".join(lst) + "." + url.split(".")[-1]
        urllib.urlretrieve(url, "images/" + local_filename)
        c = check_output("identify -verbose images/{}".format(local_filename).split())
        d = {}
        for line in c.splitlines()[:-1]:
            if not line:
                continue
            spl = line.split(":",1)
            if not spl:
                continue
            k, v = spl
            if v.strip():
                d[k.lstrip()] = v.strip()
        imgObj = {"url": url, "local_filename": local_filename, "meta_data": d}
        Image.objects.create(**imgObj)
        self.q.put(imgObj)

    def run(self):
        thread_list = []
        for url in self.images:
            if self.r_server.incr("THROT:{}".format(self.username)) > self.throttle_rate:
                result = {
                    "error": "throttle rate exceeded"
                }
                return result
            t = threading.Thread(target=self.save_image, args=(url,))
            t.start()
            thread_list.append(t)
        for t in thread_list:
            t.join()
        result = []
        while not self.q.empty():
            result.append(self.q.get())
        return result
