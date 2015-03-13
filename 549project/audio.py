#!/usr/bin/python

import subprocess

database = []
target = ""

def insert_audio(name, audio):
    # [audio] is the address of sound file by user [name]
    # 1. change [audio] to a new address to avoid overwrite
    new_addr = "%s.flac" % (name)
    subprocess.call(["mv", audio, new_addr])
    # 2. store data to database
    global database
    database.append((name, new_addr))

def correlate(audio1, audio2):
    # TODO find out whether audio1 highly correlates with audio2
    return True

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

