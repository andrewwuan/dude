#!/usr/bin/python

import sys
import string
import subprocess
import optparse
from weather import *
from date import *
from wiki import *
from client import *
#from temperature import *

user = ""

parser = optparse.OptionParser()

parser.add_option('-q', '--query',
    action="store", dest="host",
    help="host name", default="localhost")

parser.add_option('-p', '--port',
    action="store", dest="port",
    help="port number", default="8888")

options, args = parser.parse_args()

# set receive alarm
signal.signal(signal.SIGALRM, receive_alarm)

while (True):
    keyword = []
    # Check for the keyword dude
    while ("dude" not in keyword):
        print "No input..."
        subprocess.call("./speech2text_short.sh")
        f1 = open("stt.txt", "rw+")
        noise = f1.read().strip('\n')
        f1.close()
        if (noise != ""):
            print "Just heard %s" % (noise)
            keyword = noise.split()
        # Add pulling information
        
    user = get_recognition('dude.wav', options.host, options.port)

    subprocess.call(["./text2speech.sh", 
        "%s, what can I do for you" % (user)])

    # Listen to user's question
    subprocess.call("./speech2text_long.sh")
    f2 = open("stt.txt", "rw+")
    line = f2.read().strip('\n')
    f2.close()
    if (line != ""):
        print "Your question is %s" % (line)
    else:
        print "You did not ask me anything..."
        continue

    # Process request
    request = line.split()

    response = "%s, I do not know what to say" % (user)

    # Check authencity
    if ("my" == request[0] and 
        "name" == request[1] and
        "is" == request[2]):
        user = request[3]
        post_recognition(user, 'dude.wav', options.host, options.port)
        response = "hello, %s" % (user)
    
    # Check temperature
    #if ("temperature" in request):
    #    response = "%s, %s" % (user, check_temperature(request))

    # Check weather
    if ("weather" in request):
        response = "%s, %s" % (user, check_weather(request))

    # Check time
    if ("time" in request or
        "date" in request):
        response = "%s, %s" % (user, check_date(request))
    
    # Set alarm
    if ("alarm" in request):
        response = "%s, %s" % (user, alarm(request))

    # Check Wiki
    if ("what" == request[0] and
        "is" == request[1]):
        response = "%s, %s" % (user, check_wiki(request))

    ############# TODO ###############
    # If the request needs information from server
    #if (False):
    #    response = "%s, %s" % (user, check_server(request))
    ############# END  ###############
     
    # cannot handle too long strings
    if (len(response) > 100):
        response = response[0:101]
        last_space = string.rfind(response, " ") 
        response = response[0:last_space]
    
    print response        
    subprocess.call(["./text2speech.sh", response])

