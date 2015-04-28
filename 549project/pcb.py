#!/usr/bin/env python

# Written by Limor "Ladyada" Fried for Adafruit Industries, (c) 2015
# This code is released into the public domain

# Modified by team14 for CMU 18-549 project "dude"

import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
DEBUG = 1

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

# temperature sensor connected to adc #0, photocell connected to adc #1
temperature_adc = 0
brightness_adc = 1

# setting last value & tolerance
# if change is less than tolerance, don't report changed
temperature_last = 0
temperature_tolerance = 0

brightness_last = 0
brightness_tolerance = 0


while True:

    # Temperature
    temperature_changed = False

    temperature_value = readadc(temperature_adc, SPICLK, SPIMOSI,SPIMISO, SPICS)
    temperature_adjust = abs(temperature_value - temperature_last)

    if ( temperature_adjust > temperature_tolerance ):
        temperature_changed = True

    if ( temperature_changed ):
        set_temperature = temperature_value / 10.24     # convert 10bit adc0 (0-1024) to percent
        set_temperature = round(set_temperature)
        set_temperature = int(set_temperature)

        print 'Temperature = {temperature}%' .format(temperature = set_temperature)

        temperature_last = temperature_value


    # Brightness
    brightness_changed = False

    brightness_value = readadc(brightness_adc, SPICLK, SPIMOSI,SPIMISO, SPICS)
    brightness_adjust = abs(brightness_value - brightness_last)

    if ( brightness_adjust > brightness_tolerance ):
        brightness_changed = True

    if ( brightness_changed ):
        set_brightness = brightness_value / 10.24     # convert 10bit adc0 (0-1024) to percent
        set_brightness = round(set_brightness)
        set_brightness = int(set_brightness)

        print 'Brightness = {brightness}%' .format(brightness = set_brightness)

        brightness_last = brightness_value

    time.sleep(0.5)
