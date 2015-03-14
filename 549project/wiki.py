#!/usr/bin/python

import wikipedia

def check_wiki(request):
    request.pop(0)
    request.pop(0)
    question = string.join(request)                     
    answer = wikipedia.summary(question, sentences=2)
    return answer
