#!/usr/bin/python

import sys
import string
import subprocess
import optparse
#from weather import *
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

parser.add_option("-c", "--camera",
    action="store_true", dest="camera",
    help="enable camera", default=False)

options, args = parser.parse_args()

# import camera
if (options.camera):
    from facial_recognition import *
    from takeSample import *

# set receive alarm
signal.signal(signal.SIGALRM, receive_alarm)

setupPCB()

# setup facial recognition
if (options.camera):
    train_data()

while (True):
    keyword = []
    # Check for the keyword teddy
    while ("teddy" not in keyword and
	   "Teddy" not in keyword):
        # Check for incoming message
        if (user != ''):
            packet = check_message(user, options.host, options.port)
            for p in packet:
                message = "%s, you have a message from %s." % (user, p['user'])
                subprocess.call(["./text2speech.sh", message])
                subprocess.call(["./text2speech.sh", p['message']])

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
        check_alarms("http://" + options.host + ":" + options.port, options.device)
        
    user = get_recognition('teddy.wav', options.device, options.host, options.port)

    if (user == ""):
        subprocess.call(["./text2speech.sh", 
            "hi, I'm teddy. Who are you?"])
        subprocess.call("./speech2text_long.sh")
        f5 = open("stt.txt", "rw+")

        # Get splitted words
        line = f5.read().strip('\n')
        request = line.split()
        f5.close()

        # Find "name" in the sentence
        nameStart = 0
        for i in xrange(len(request)):
            if request[i] == 'name':
                nameStart = i + 2

        if (nameStart == 0):
            subprocess.call(["./text2speech.sh", 
                "fine, don't tell me. i dont want to know it anyway."])            
            continue

        name = ' '.join(request[i:])
        post_recognition(name, 'teddy.wav', 
		options.device, options.host, options.port)
        if (options.camera):
            takePhoto(name)
            train_data()
	user = name

    subprocess.call(["./text2speech.sh", 
        "hi, %s" % (user)])

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
        post_recognition(user, 'teddy.wav',
		options.device, options.host, options.port)
        if (options.camera):
            takPhoto(user)
            train_data()
        response = "hello, %s" % (user)
    
    # Check temperature
    if ("temperature" in request):
        temperatures = get_temperature(options.host, options.port)
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
        brightnesses = get_brightness(options.host, options.port)
        success = 0
        for b in brightnesses:
            if (b['name'] == options.device):
                response = "%s, the current brightness is %f" % (user, b['brightness'])
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
    #if ("weather" in request):
    #    response = "%s, %s" % (user, check_weather(request))

    # Recognize person
    if (options.camera):
        if ("recognize" in request):
            name, confidence = facial_recognition()
            if (confidence > 6000):
                response = "%s, I don't know this guy" % user
            else:
                response = "%s, this is %s" % (user, name)

    # Check time
    if ("time" in request or
        "date" in request):
        response = "%s, %s" % (user, check_date(request))
    
    # Set alarm
    if ("alarm" in request):
        response = "%s, %s" % (user, alarm(request))
        update_alarms("http://" + options.host + ":" + options.port, request, options.device)

    # Check Wiki
    if ("what" == request[0] and
        "is" == request[1]):
        response = "%s, %s" % (user, check_wiki(request, 2))
    if ("how" == request[0] and
        "do" == request[1] and
        "I" == request[2]):
        response = "%s, %s" % (user, check_wiki(request, 3))

    # Check the user of the other device
    for r in request:
        if "home" in r:
            last_users = get_last_user(options.host, options.port)
            response = "%s, I don't know who's at the other side" % user
            for last_user in last_users:
                if (last_user['name'] != options.device):
                    response = "%s, %s is" % (user, last_user['last_user'])
                    break

    # Bad language
    for r in request:
        if ("*" in r or "bitch" in r):
            response = "You cursed! You no-manor stupid piece of poo-poo %s" % user
            break

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

