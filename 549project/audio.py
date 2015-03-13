#!/usr/bin/python

from scipy.io import wavfile
from scipy import signal
import matplotlib.pyplot as plt
from utility import pcm2float
from numpy import *
import subprocess

database = []
target = ""

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
    
    sig1Norm = pcm2float(sig1, 'float32')
    sig2Norm = pcm2float(sig2, 'float32')

    lags, c, line, b = plt.xcorr(sig1Norm, sig2Norm)
    return (amax(line) > 0.5)

def match(elem):
    name = elem[0]
    addr = elem[1]
    
    # if the audio matches, return name of the user
    if (correlate(target, addr)):
        return name
    else:
        return ""

def find(elem):
    # filter out the empty strings
    return (elem != "")

def check_audio(audio):
    if (database == []):
        # database is empty
        return ""
    
    global target 
    target = audio
    matches = map(match, database)
    result = filter(find, matches)
    if (result == []):
        # cannot find a match
        return ""
    else:
        # return the first name matched
        # there should be only one name theoretically
        return result[0]

