#!/usr/bin/python

import string
import wikipedia

def check_wiki(request, pop_count):
	for i in xrange(pop_count):
		request.pop(0)
	question = string.join(request)                     
	answer = wikipedia.summary(question, sentences=1)
	start = string.find(answer, "(")
	end = string.find(answer, ")")    
	answer = string.replace(answer, answer[start-1:end+1], "")
	return answer

