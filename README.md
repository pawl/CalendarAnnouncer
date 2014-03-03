This application will pull events from Dallas Makerspace's public calendar and announce those events when they occur. It uses Google's TTS webservice for the announcement audio. 

Due to the use of Mp3play, this only works on Windows currently.

Dependencies:
* pytz
* icalendar
* beautifulsoup
* apscheduler
* mp3play

Original Google TTS Code From: https://github.com/yozel/talking-bots

The iCal file is being parsed with: https://github.com/oblique63/Python-GoogleCalendarParser
