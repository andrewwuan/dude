#!/usr/bin/python
import tornado.ioloop
import tornado.concurrent
from tornado.httpclient import HTTPClient
from tornado.httputil import url_concat
import requests

def synchronous_fetch(url, user, name):
    http_client = HTTPClient()
    params = {"user": user, "name": name}
    url = url_concat(url, params)
    response = http_client.fetch(url)
    return response.body

def synchronous_update(url, user, name, value):
    http_client = HTTPClient()
    params = {"user": user, "name": name, "value":value}
    url = url_concat(url, params)
    response = http_client.fetch(url)
    return response.body

def synchronous_upload(url, filename):
    files = {'file': open(filename, 'rb'), }
    response = requests.post(url, files=files)
    return response.text

synchronous_upload("http://localhost:8888", 'hello.txt')

synchronous_update("http://localhost:8888", "Amy", "hobby", "reading")

print synchronous_fetch("http://localhost:8888", "Amy", "hobby")

# returns response text
def check_server(request):
    response = synchronous_fetch(request)
    return response

def update_server(request):
    response = synchronous_update(request)
    return response

