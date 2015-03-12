#!/usr/bin/python

import subprocess

database = []
target = ""

def insert_audio(name, audio):
    # [audio] is the address of sound file by user [name]
    # 1. change [audio] to a new address to avoid overwrite
    new_addr = "%.flac" % (name)
    subprocess.call("mv file.flac %" % (new_addr))
    # 2. store data to database
    database.append((name, new_addr))

def correlate(audio1, audio2):

    return True

def match(elem):
    name = elem[0]
    addr = elem[1]
     
    if (correlate(target, addr)):
        return name
    else:
        return ""

def find(elem):
    return (elem != "")

def check_audio(audio):
    if (database == []):
        return ""
    
    global target 
    target = audio
    matches = map(match, database)
    result = filter(find, matches)
    if (result == []):
        return ""
    else:
        return result[0]

