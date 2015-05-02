import signal
import time
import datetime
import subprocess

alarms = {}

def receive_alarm(signum, stack):
    t = datetime.datetime.now()
    t += datetime.timedelta(minutes=1)
    t = t.replace(second=0, microsecond=0)
    if (alarms[t]):
        subprocess.call(['afplay', '-t', '15', 'alarm.wav'])
    else:
        print "Alarm canceled"

def alarm(request):
    request = ' '.join(request)
    if ("set" in request or "Set" in request):
        return set_alarm(request) 
    elif ("cancel" in request or "Cancel" in request):
        return cancel_alarm(request)
    else:
        pass

def set_alarm(request):
    time_now = datetime.datetime.now()
    alarm_time = extract_time(request)
    if (alarm_time == "Wrong time format"):
        return "Sorry I didn't hear the time clearly, say again"
    t = int((alarm_time - time_now).total_seconds())
    if (t < 0):
        return "Alarm time should be in the future"
    signal.alarm(t)
    print 'Alarm set at ', alarm_time
    alarms[alarm_time] = True
    return "Alarm is set"

def cancel_alarm(request):
    alarm_time = extract_time(request)
    if (alarm_time == "Wrong time format"):
        return "Sorry I didn't hear the time clearly, say again"
    if (alarm_time in alarms.keys()):
        alarms[alarm_time] = False
        return "Alarm is cancelled"
    return "There is no alarm set at this time"    

def extract_time(request):
    start = request.find('at')+3
    end = request.find(' ', start)
    t = request[start:end]+':00'
    if ('a.m.' in request or 'in the morning' in request):
        t += ' AM'
    else:
        t += ' PM'
    if ('on' in request):
        start = request.find('on')+3
        timeList = request[start:].split()
        m = timeList[0]
        d = timeList[1][0:-2]
        if (len(timeList) >= 3):
            y = timeList[2]
        else:
            y = str(datetime.datetime.now().year)
        t += ' '+ m + ' ' + d + ' ' + y
        try:
            alarm_time = datetime.datetime.strptime(t, '%I:%M:%S %p %B %d %Y')
        except:
            return "Wrong time format"
    elif ('for' in request):
        if ('next' in request):
            start = request.find('next')+5
            end = request.find(' ', start)
            dayOfW = request[start:end]
            d = dateFromDayOfWeek(dayOfW, True)
        else:
            start = request.find('for')+4
            end = request.find(' ', start)
            dayOfW = request[start:end]
            d = dateFromDayOfWeek(dayOfW, False)
        try:
            t = datetime.datetime.strptime(t, '%I:%M:%S %p').time()
            alarm_time = datetime.datetime.combine(d, t)
        except:
            return "Wrong time format"
    elif ('tomorrow' in request):
        m = str(datetime.datetime.now().month)
        d = str(datetime.datetime.now().day+1)
        y = str(datetime.datetime.now().year)
        t += ' '+ m + ' ' + d + ' ' + y
        try:
            alarm_time = datetime.datetime.strptime(t, '%I:%M:%S %p %m %d %Y')
        except:
            return "Wrong time format"
    else:
        m = str(datetime.datetime.now().month)
        d = str(datetime.datetime.now().day)
        y = str(datetime.datetime.now().year)
        t += ' '+ m + ' ' + d + ' ' + y
        try:
            alarm_time = datetime.datetime.strptime(t, '%I:%M:%S %p %m %d %Y')
        except:
            return "Wrong time format"
    return alarm_time

def dateFromDayOfWeek(dayOfW, next, ):
    dayOfWeek_now = datetime.datetime.now().weekday()
    if (dayOfW == 'Monday'):
        d = 0
    elif (dayOfW == 'Tuesday'):
        d = 1
    elif (dayOfW == 'Wednesday'):
        d = 2
    elif (dayOfW == 'Thursday'):
        d = 3
    elif (dayOfW == 'Friday'):
        d = 4
    elif (dayOfW == 'Saturday'):
        d = 5
    elif (dayOfW == 'Sunday'):
        d = 6
    else:
        print "Error, dayOfWeek is not valid: %s", dayOfW
        return -1
    print d, dayOfWeek_now
    if (dayOfWeek_now < d):
        if (next == False):
            gapDate = d - dayOfWeek_now
        else:
            gapDate = d - dayOfWeek_now + 7
    else:
        gapDate = 7 - dayOfWeek_now + d
    date = datetime.datetime.now() + datetime.timedelta(days=gapDate)
    return date
