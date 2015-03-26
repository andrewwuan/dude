#!usr/bin/python

import Adafruit_MCP9808.MCP9808 as MCP9808

# Must call this file with 'sudo'
sensor = MCP9808.MCP9808()
sensor.begin()

def check_temperature(request):
    temp = sensor.readTempC()
    response = "temperature in the current room is {0:0.3F} degree celcius".format(temp)
    return response

