#!/usr/bin/python

import tornado.ioloop
import tornado.concurrent
from tornado.httpclient import HTTPClient
from tornado.httputil import url_concat
import requests
from alarm import *
import string
import urllib

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

def check_alarms(url, device):
    http_client = HTTPClient()
    params = {"method":"check_alarms", "device":device}
    url = url_concat(url, params)
    response = http_client.fetch(url)
    print response.body
    alarm_request = response.body
    if (alarm != "No alarm"):
        alarm(alarm_request)

def update_alarms(url, request, device):
    http_client = HTTPClient()
    params = {"method":"update_alarm", "request":request, "device":device}
    url = url_concat(url, params)
    response = http_client.fetch(url)
    return response.body

#synchronous_upload("http://localhost:8888", 'camera-shutter-click-01.wav')
#synchronous_upload("http://localhost:8888", 'song.wav')

#synchronous_update("http://localhost:8888", "Amy", "hobby", "reading")

#print synchronous_fetch("http://localhost:8888", "Amy", "hobby")


#update_alarms("http://localhost:8888", "Set alarm at 2:38 p.m.", "device0")
#check_alarms("http://localhost:8888", "device1")

# returns response text
def check_server(request):
    response = synchronous_fetch(request)
    return response

def update_server(request):
    response = synchronous_update(request)
    return response

import subprocess

def post_recognition(name, audio, device, host, port):
    print("Posting user %s's audio file %s" % (name, audio))
    if (not host):
        host = 'localhost'
    if (not port):
        port = '8888'
    output = subprocess.check_output(['curl', '-X', 'POST', 'http://%s:%s/wav?%s' % 
        (host, port, urllib.urlencode({'user': name, 'device': device})), '--data-binary', "@%s" % audio])
   
def get_recognition(audio, device, host, port):
    print("Getting voice recognition result with audio file %s" % audio)
    if (not host):
        host = 'localhost'
    if (not port):
        port = '8888'
    output = subprocess.check_output(['curl', '-X', 'GET', 'http://%s:%s/wav?%s' % (host, port, urllib.urlencode({'device': device})), '--data-binary', "@%s" % audio])
    return output

def check_message(user, host, port):
    # Check server and fetch message for user
    print("Check user %s's messages" % user)
    if (not host):
        host = 'localhost'
    if (not port):
        port = '8888'
    output = subprocess.check_output(['curl', '-X', 'GET', 'http://%s:%s/message?%s' 
        % (host, port, urllib.urlencode({'orig_user': user}))])
    return eval(output)['messages']

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
    output = subprocess.check_output(['curl', '-X', 'POST', 'http://%s:%s/message?%s' 
        % (host, port, urllib.urlencode({'orig_user': orig_user, 'dest_user': dest_user})), '--data', "%s" % message])
    return output

def get_brightness(host, port):
    print("Getting brightness")
    if (not host):
        host = 'localhost'
    if (not port):
        port = '8888'

    output = subprocess.check_output(['curl', '-X', 'GET', 'http://%s:%s/brightness' %
        (host, port)])
    return eval(output)['brightness']

def set_brightness(device, brightness, host, port):
    print("Setting device %s's brightness to %f" % (device, brightness))
    if (not host):
        host = 'localhost'
    if (not port):
        port = '8888'

    output = subprocess.check_output(['curl', '-X', 'POST', 'http://%s:%s/brightness?%s' %
        (host, port, urllib.urlencode({'device': device})), '--data', "%f" % brightness])
    return output

def get_temperature(host, port):
    print("Getting temperature")
    if (not host):
        host = 'localhost'
    if (not port):
        port = '8888'

    output = subprocess.check_output(['curl', '-X', 'GET', 'http://%s:%s/temperature' %
        (host, port)])
    return eval(output)['temperature']

def set_temperature(device, temperature, host, port):
    print("Setting device %s's temperature to %f" % (device, temperature))
    if (not host):
        host = 'localhost'
    if (not port):
        port = '8888'

    output = subprocess.check_output(['curl', '-X', 'POST', 'http://%s:%s/temperature?%s' %
        (host, port, urllib.urlencode({'device': device})), '--data', "%f" % temperature])
    return output

def get_last_user(host, port):
    print("Getting last user")
    if (not host):
        host = 'localhost'
    if (not port):
        port = '8888'

    output = subprocess.check_output(['curl', '-X', 'GET', 'http://%s:%s/last_user' %
        (host, port)])
    return eval(output)['last_user']


