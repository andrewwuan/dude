#!/usr/bin/python

import pywapi
import string

result = pywapi.get_weather_from_weather_com('15289')

def check_weather(request):
	cond = result['current_conditions']['text']
	temp = result['current_conditions']['temperature']
	
	weather = "Pittsburgh is %s and %s degree celcius now" % (cond, temp)
	return weather

