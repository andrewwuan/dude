#!/usr/bin/python

import datetime

def check_date(request):
	now = datetime.datetime.now()
	
	# Get year
	year = "%d" % (now.year)
	
	# Get month
	month = ""
	if (now.month == 1):
		month = "January"
	if (now.month == 2):
		month = "February"
	if (now.month == 3):
		month = "March"
	if (now.month == 4):
		month = "April"
	if (now.month == 5):
		month = "May"
	if (now.month == 6):
		month = "June"
	if (now.month == 7):
		month = "July"
	if (now.month == 8):
		month = "August"
	if (now.month == 9):
		month = "September"
	if (now.month == 10):
		month = "October"
	if (now.month == 11):
		month = "November"
	if (now.month == 12):
		month = "December"
	
	# Get day
	day = "%d" % (now.day)
	
	# Get hour
	hour = ""
	foo = "pm"
	if (now.hour == 24 or 
	    now.hour < 12):
		foo = "am"
	if (now.hour % 12 == 0):
		hour = "12" 
	else:
		hour = "%d" % (now.hour % 12);
	
	# Get minute
	minute = "%d" % (now.minute)
	
	return "Now is %s %s %s %s %s%s" % (year, month, day, hour, minute, foo)

