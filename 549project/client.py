#!/usr/bin/python

import tornado.ioloop
import tornado.concurrent
from tornado.httpclient import HTTPClient
from tornado.httputil import url_concat
import requests
import string
#from alarm import *

def synchronous_fetch(url, user, name):
    http_client = HTTPClient()
    params = {"user": user, "name": name, "method":"fetch"}
    url = url_concat(url, params)
    response = http_client.fetch(url)
    return response.body

def synchronous_update(url, user, name, value):
    http_client = HTTPClient()
    params = {"user": user, "name": name, "value":value, "method":"update"}
    url = url_concat(url, params)
    response = http_client.fetch(url)
    return response.body

def synchronous_upload(url, filename):
    f = open(filename, 'rb')
    files = {'file': open(filename, 'rb'), }
    #response = requests.post(url, files=files)
    http_client = HTTPClient()
    response = http_client.fetch(url, body=f.read(), method='POST')
    return response.body

def check_alarms(url):
    http_client = HTTPClient()
    params = {"method":"check_alarms"}
    url = url_concat(url, params)
    response = http_client.fetch(url)
    print response.body
    alarms = response.body.split("$")
    for alarm_request in alarms:
        alarm(alarm_request)

def update_alarms(url, request):
    http_client = HTTPClient()
    params = {"method":"update_alarm", "request":"alarm!!!"}
    url = url_concat(url, params)
    response = http_client.fetch(url)
    return response.body

#synchronous_upload("http://localhost:8888", 'camera-shutter-click-01.wav')
#synchronous_upload("http://localhost:8888", 'song.wav')

#synchronous_update("http://localhost:8888", "Amy", "hobby", "reading")

#print synchronous_fetch("http://localhost:8888", "Amy", "hobby")



# returns response text
def check_server(request):
    response = synchronous_fetch(request)
    return response

def update_server(request):
    response = synchronous_update(request)
    return response


import subprocess

def post_recognition(name, audio, host, port):
    print("Posting user %s's audio file %s" % (name, audio))
    if (not host):
        host = 'localhost'
    if (not port):
        port = '8888'
    output = subprocess.check_output(['curl', '-X', 'POST', 'http://%s:%s/wav?user=%s' % (host, port, user), '--data-binary', "@%s" % audio])
   
def get_recognition(audio, host, port):
    print("Getting voice recognition result with audio file %s" % audio)
    if (not host):
        host = 'localhost'
    if (not port):
        port = '8888'
    output = subprocess.check_output(['curl', '-X', 'GET', 'http://%s:%s/wav' % (host, port), '--data-binary', "@%s" % audio])
    return output

def check_message(user, host, port):
    # Check server and fetch message for user
    print("Check user %s's messages" % user)
    if (not host):
        host = 'localhost'
    if (not port):
        port = '8888'
    output = subprocess.check_output(['curl', '-X', 'GET', 'http://%s:%s/message?orig_user=%s' 
        % (host, port, user)])
    return output

def send_message(message, orig_user, dest_user, host, port):
    # Convert I to user name
    message = message.replace("i ", "%s " % (orig_user))
    message = message.replace("I ", "%s " % (orig_user))

    # Send the message to server (orig_user -> dest_user)
    print("Post message to user %s from user %s" % (dest_user, orig_user))
    if (not host):
        host = 'localhost'
    if (not port):
        port = '8888'
    output = subprocess.check_output(['curl', '-X', 'POST', 'http://%s:%s/message?orig_user=%s?dest_user=%s' 
        % (host, port, orig_user, dest_user), '--data', "%s" % message])
    return output
