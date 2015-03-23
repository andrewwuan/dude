#!/usr/bin/python

from scipy.io import wavfile
from scipy import signal
import matplotlib.pyplot as plt
from utility import pcm2float
from numpy import *
import subprocess
import operator

database = []
target = ""
dictionary = {}
def insert_audio(name, audio):
    # [audio] is the address of sound file by user [name]
    # 1. change [audio] to a new address to avoid overwrite
    new_addr = "%s.wav" % (name)
    subprocess.call(["mv", audio, new_addr])
    # 2. store data to database
    global database
    database.append((name, new_addr))

def correlate(audio1, audio2):
    # TODO find out whether audio1 highly correlates with audio2
    fs1, sig1 = wavfile.read(audio1)
    fs2, sig2 = wavfile.read(audio2)
   
    shortWidth = 10
    shortLen = len(sig1) / shortWidth
   
    sig1Short = array([sig1[shortWidth * i] for i in xrange(shortLen)])
    sig2Short = array([sig2[shortWidth * i] for i in xrange(shortLen)])
    
    sig1Norm = pcm2float(sig1Short, 'float32')
    sig2Norm = pcm2float(sig2Short, 'float32')
    
    sig1fft = fft.fft(sig1Norm)
    sig2fft = fft.fft(sig2Norm)
    #lags, c, line, b = plt.xcorr(sig1Norm, sig2Norm, maxlags=None)
    lag, c, line, b = plt.xcorr(absolute(sig1fft),absolute(sig2fft))
    maxC = amax(c)
    print("max correlation is %f" % maxC)
    return maxC
    #return (maxC > 0.66)

def match(elem):
    name = elem[0]
    addr = elem[1]
    global dictionary
    dictionary[name] = correlate(target, addr)
    return
    # if the audio matches, return name of the user
"""
    if (correlate(target, addr)):
        return name
    else:
        return ""
"""
def find(elem):
    # filter out the empty strings
    return (elem != "")

def check_audio(audio):
    if (database == []):
        # database is empty
        return ""
    
    global target 
    target = audio
    map(match, database)
    global dictionary
    print dictionary
    result = max(dictionary.iteritems(), key = operator.itemgetter(1))
    if (result[1]>0.65):
        return result[0]
    else:
        return ""
"""
    matches = map(match, database)
    result = filter(find, matches)
    if (result == []):
        # cannot find a match
        return ""
    else:
        print result
        # return the first name matched
        # there should be only one name theoretically
        return result[0]
"""

