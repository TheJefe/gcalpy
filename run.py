from __future__ import print_function
import configparser
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import re
import os
from subprocess import call
import sys
DIRNAME = os.path.dirname(__file__)

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
SERVICE_ACCOUNT_FILE = 'client_secrets.json'

urlregex = 'https?://(?:[-/?=&\w.])+'

def read_calendar_id():
    try:
        config = configparser.ConfigParser()
        config.read(os.path.join(DIRNAME, 'properties.ini'))
    except FileNotFoundError:
        raise "Must have a properties.ini file, with \n[DEFAULT]\ncalendar_id="
    return config['DEFAULT']['calendar_id']

def get_creds():
    store = file.Storage(os.path.join(DIRNAME, 'token.json'))
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(os.path.join(DIRNAME, 'credentials.json'), SCOPES)
        creds = tools.run_flow(flow, store)
    return creds

def get_time_window():
    now = datetime.datetime.utcnow()
    time_min = now.isoformat() + 'Z' # 'Z' indicates UTC time
    time_max = (now + datetime.timedelta(hours=2)).isoformat() + 'Z' # 'Z' indicates UTC time
    return time_min, time_max

def get_events(creds, calendar_id, time_min, time_max):
    service = build('calendar', 'v3', credentials=creds)
    results = service.events().list(
        calendarId=calendar_id,
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime',
    ).execute()
    return results['items']

def get_next_event(creds, calendar_id):
    time_min, time_max = get_time_window()
    events = get_events(creds, calendar_id, time_min, time_max)
    # Sort out all-day events
    events = [event for event in events if 'date' not in event['start']]
    if len(events) < 1:
        print('No events found')
        exit()
    return events[0]

calendar_id = read_calendar_id()
creds = get_creds()
event = get_next_event(creds, calendar_id)

htmlLink = event['htmlLink']
location = event.get('location')
summary = event['summary']

print(u''.format(summary))
call(['open', htmlLink])

if location:
    location_urls = re.findall(urlregex, location)

if len(location_urls) >= 1:
    location = location_urls[0]
    print(location)
    if(len(sys.argv) == 1):
        call(['open', location])
else:
    print('no location url found')
