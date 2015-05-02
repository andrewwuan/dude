#!/usr/bin/python

import sys
import string
import subprocess
import optparse
from weather import *
from date import *
from wiki import *
from client import *
from pcb import *
#from temperature import *

user = ""

parser = optparse.OptionParser()

parser.add_option('-u', '--url',
    action="store", dest="host",
    help="host name", default="localhost")

parser.add_option('-p', '--port',
    action="store", dest="port",
    help="port number", default="8888")

parser.add_option('-d', '--device',
    action="store", dest="device",
    help="device name", default="Teddy")

options, args = parser.parse_args()

# set receive alarm
signal.signal(signal.SIGALRM, receive_alarm)

setupPCB()

while (True):
    keyword = []
    # Check for the keyword dude
    while ("dude" not in keyword):
        # Check for incoming message
        packet = check_message(user, options.host, options.port)
        if (len(packet) != 0):            
            message = "%s, you have a message from %s." % (user, packet[0])
            subprocess.call(["./text2speech.sh", message])
            subprocess.call(["./text2speech.sh", packet[1]])

        # Post temperature & brightness data
        set_temperature(options.device, readTemperature(), options.host, options.port)
        set_brightness(options.device, readBrightness(), options.host, options.port)
            
        print "No input..."
        subprocess.call("./speech2text_short.sh")
        f1 = open("stt.txt", "rw+")
        noise = f1.read().strip('\n')
        f1.close()
        if (noise != ""):
            print "Just heard %s" % (noise)
            keyword = noise.split()
        # Check for alarms
        check_alarms(options.url, options.device)
        
    user = get_recognition('dude.wav', options.device, options.host, options.port)

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
        post_recognition(user, 'dude.wav', options.device, options.host, options.port)
        response = "hello, %s" % (user)
    
    # Check temperature
    if ("temperature" in request):
        temperatures = get_temperature()
        success = 0
        for t in temperatures:
            if (t['name'] == options.device):
                response = "%s, the current temperature is %f" % (user, t['temperature'])
            success = 1
            break
        if (not success):
            response = "%s, I cannot get the temperature from server" % user

    # Check brightness
    if ("brightness" in request):
        brightnesses = get_brightness()
        success = 0
        for b in brightnesses:
            if (b['name'] == options.device):
                response = "%s, the current brightness is %f" % (user, t['brightness'])
            success = 1
            break
        if (not success):
            response = "%s, I cannot get the brightness from server" % user

    # Leave message
    if ("message" in request):
        user2 = request[-1]
        response = "Okay, %s" % (user)
        subprocess.call(["./text2speech.sh", response])
        subprocess.call("./speech2text_long.sh")
        f3 = open("stt.txt", "rw+")
        message = f3.read().strip('\n')
        f3.close()
        if (message != ""):
            print "Your message for %s is %s" % (user2, message)
            send_message(message, user, user2, options.host, options.port)
            response = "Your message for %s is sent, %s" % (user2, user)
        else:
            response = "I did not hear your message, %s" % (user)

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
        update_alarms(options.url, request, options.device)

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

