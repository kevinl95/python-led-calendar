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
from dateutil import tz, parser
from httplib2 import Http
from oauth2client import file, client, tools
from pywinauto.application import Application
import datetime
import subprocess
import time

# Path to PowerLed installation directory
power_led_dir = 'C:\Program Files (x86)\PowerLed\PowerLed.exe'
# PowerLed window name
window_name = 'display.ledprj - PowerLed V2.88.0'
# Sign WiFi name
sign_wifi_name = 'TF-WIFI_8BE602'
# Your WiFi name
your_wifi_name = 'FILLTHISIN'
# Your timezone
t_zone = tz.gettz('America/Denver')
# Update time in seconds
updateTime = 60*3

while True:
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
    to_Display = []
    if not events:
        print('No upcoming events found.')
        while len(to_Display) < 6:
            to_Display.append('No event found - enjoy your day!')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        parsedDate = parser.parse(start)
        print(start)
        convertDate = parsedDate.astimezone(t_zone)
        milTime = convertDate.time()
        milTimeStrp = datetime.datetime.strptime(str(milTime), "%H:%M:%S")
        normTime = milTimeStrp.strftime("%I:%M %p")
        date = convertDate.date()
        fDate = date.strftime("%m/%d")
        display_string = str(fDate) + ' ' + normTime + ' ' + event['summary']
        print('String to display: ' + display_string)
        spaces = '-' * 10
        to_Display.append(display_string + spaces)
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
    # Need to connect to the LED sign
    # Assumes you have already connected to it before!
    process = subprocess.Popen(
            'netsh wlan connect {0}'.format(sign_wifi_name),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    # Open PowerLed
    app = Application().start(power_led_dir)
    window = app.window(best_match=window_name)
    window.menu_select("Tools(T)->Search Panel")
    time.sleep(5)
    okWindow = app.window(best_match='Progress')
    okWindow.Ok.click()
    window.menu_select("Tools(T)->Send All")
    time.sleep(5)
    window.menu_select("File(F)->Quit(X)")
    exitWindow = app.window(best_match='PowerLed')
    exitWindow.Yes.click()
    # Need to connect back to your WiFI network
    # Assumes you have already connected to it before!
    ReconnectProcess = subprocess.Popen(
            'netsh wlan connect \"{0}\"'.format(your_wifi_name),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    stdout, stderr = ReconnectProcess.communicate()
    time.sleep(updateTime)
