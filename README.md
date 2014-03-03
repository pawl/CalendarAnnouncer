#### Description
This application will pull events from Dallas Makerspace's public Google Calendar and announce those events when they occur. It uses Google's TTS webservice for the announcement audio. 

<b>Warning:</b> Due to the use of Mp3play library, this only works on Windows currently.

#### Dependencies
* pytz
* icalendar
* beautifulsoup
* apscheduler
* mp3play

#### Setup
Install dependencies and run main.py

#### Credits
Original Google TTS Code From: https://github.com/yozel/talking-bots

The iCal file is being parsed with: https://github.com/oblique63/Python-GoogleCalendarParser
