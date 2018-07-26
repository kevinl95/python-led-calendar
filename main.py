"""
Python LED Google Calendar
K. M. Loeffler, 2018
kevinmloeffler.com

An application to demonstrate how LED displays that use the PowerLed software
can be automated to display dynamic content from the internet. This is best
run on an idle PC, like an old laptop you are upcycling. Personally, I run this
on an Intel Atom compute stick. Follow the instructions in the README as far as
how to create your credentials and how to get started.
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime
import time

# Update time in seconds
updateTime = 60*5

# Setup the Calendar API. We only need read access.
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
# The Google Calendar API creates this automatically.
store = file.Storage('token.json')
creds = store.get()
# You will save your credentials from the tutorial as credentials.json.
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))

# Call the Calendar API and get the first 5 events available.
now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
print('Getting the upcoming 5 events')
events_result = service.events().list(calendarId='primary', timeMin=now,
                                      maxResults=5, singleEvents=True,
                                      orderBy='startTime').execute()
events = events_result.get('items', [])

if not events:
    print('No upcoming events found.')
to_Display = []
for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    display_string = start + ' ' +event['summary']
    print('String to display: ' + display_string)
    to_Display.append(display_string)
# Open the template and read it in, then replace keywords with our display
# strings so that we can use this file in PowerLed
with open('template.ledprj') as fin:
    with open("display.ledprj", "w") as fout:
        for line in fin:
            if 'REPLACE1' in line:
                fout.write(line.replace('REPLACE1', to_Display[0]))
            elif 'REPLACE2' in line:
                fout.write(line.replace('REPLACE2', to_Display[1]))
            elif 'REPLACE3' in line:
                fout.write(line.replace('REPLACE3', to_Display[2]))
            elif 'REPLACE4' in line:
                fout.write(line.replace('REPLACE4', to_Display[3]))
            elif 'REPLACE5' in line:
                fout.write(line.replace('REPLACE5', to_Display[4]))
            else:
                fout.write(line)
