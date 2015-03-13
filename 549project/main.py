#!/usr/bin/python

import sys
import subprocess
from weather import *
from date import *
from audio import *

user = ""

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
        
        user = check_audio("dude.flac")

	subprocess.call(["./text2speech.sh", 
		"%s what can I do for you" % (user)])

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
	
	response = "%s I do not know what to say" % (user)
	
	# Check authencity
	if ("my" == request[0] and 
	    "name" == request[1] and
	    "is" == request[2]):
		user = request[3]
 		insert_audio(user, "dude.flac")
		response = "hello %s" % (user)
	
	# Check weather
	if ("weather" in request or
	    "temperature" in request):
		response = "%s %s" % (user, check_weather(request))
	
	# Check time
	if ("time" in request or
	    "date" in request):
		response = "%s %s" % (user, check_date(request))
		
	subprocess.call(["./text2speech.sh", response])

