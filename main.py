import urllib2
import urllib
import time
import os
import sys
import pprint
import datetime
import mp3play # only works on windows
from calendar_parser import CalendarParser
from time import sleep
from apscheduler.scheduler import Scheduler

sched = Scheduler()
sched.start()

# url for calendar
ics_url = 'http://www.google.com/calendar/ical/dallasmakerspace.org_6ipmavoef85vn59hlsbhgei4ok%40group.calendar.google.com/public/basic.ics'

# class for finding the differences between old and new event dictionary
# http://stackoverflow.com/questions/1165352/fast-comparison-between-two-python-dictionary
class DictDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    """
    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)
    def added(self):
        return self.set_current - self.intersect 
    def removed(self):
        return self.set_past - self.intersect 
    def changed(self):
        return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])
    def unchanged(self):
        return set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])

def playMp3(filename):
    mp3 = mp3play.load(filename)
    mp3.play()
    while mp3.isplaying():
        sleep(1)
   
# https://github.com/yozel/talking-bots/blob/master/tts_google.py
def speak(text='hello', lang='en', fname='result.mp3'):
    """ Send text to Google's text to speech service
    and returns created speech (wav file). """
    print text
    limit = min(100, len(text))#100 characters is the current limit.
    text = text[0:limit]
    url = "http://translate.google.com/translate_tts"
    values = urllib.urlencode({"q": text, "textlen": len(text), "tl": lang})
    hrs = {"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7"}
    #TODO catch exceptions
    req = urllib2.Request(url, data=values, headers=hrs)
    p = urllib2.urlopen(req)
    f = open(fname, 'wb')
    f.write(p.read())
    f.close()
    playMp3("begin.mp3")
    playMp3(fname)

# gets newest events from the google calendar ical feed
def getCalendarEvents():
	cal = CalendarParser(ics_url=ics_url)
	eventsDict = {} # ensure uniqueness by using a dict
	for event in cal.parse_calendar():
		if event["start_time"] > datetime.datetime.now():
			eventsDict[event["name"] + str(event["start_time"])] = {"name": event["name"], "start_time": event["start_time"]}
	return eventsDict

# checks for new events and adds them to the scheduler
def updateEvents(oldEvents):
	newEvents = getCalendarEvents()
	d = DictDiffer(newEvents, oldEvents)
	for eventKey in d.added():
		addEvent(newEvents[eventKey]["name"] + " will begin in 5 minutes", newEvents[eventKey]["start_time"] - datetime.timedelta(minutes=5))
		addEvent(newEvents[eventKey]["name"] + " is starting now", newEvents[eventKey]["start_time"])
	#TODO: remove jobs after they are removed from the calendar
	#for event in d.removed():
	return newEvents

def addEvent(eventName, eventStartTime):
	#TODO: if two events have the same time, one of the events will not play - need to use a queue instead
	#TODO: handle all day events differently, possibly by announcing every few hours
	# without lambda, there is an error about the function not being callable
	job = sched.add_date_job(lambda: speak(text=eventName), eventStartTime)
	if job:
		print "event added: ", eventName, eventStartTime
                        
def main():
	events = getCalendarEvents()
	for key, event in events.iteritems(): # initial loading of events into scheduler
		addEvent(event["name"] + " will begin in 5 minutes", event["start_time"] - datetime.timedelta(minutes=5))
		addEvent(event["name"] + " is starting now", event["start_time"])
	secondsFromNow = datetime.datetime.now() + datetime.timedelta(seconds=5)
	addEvent("Calendar announcer has started", secondsFromNow)
	while True:
		sleep(10800) # update every 3 hours
		events = updateEvents(events)

# debug, print events
#pprint.pprint(getCalendarEvents())
main()

