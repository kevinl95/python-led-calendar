# Automating Updating an LED Scrolling Sign with Python

This project demonstrates how an off-the-shelf LED scrolling display with no programmable interfaces can be automated using Python and the proprietary software (PowerLed) that came with the unit! We accomplish this via the use of pywinauto, a set of Python modules for automating Windows GUIs, the use of subprocess calls to connect to the device's wifi, and the use of the Google Calendar API to show how you can get your display to show content pulled from the internet.

This project will display the first five events off your Google Calendar on a LED display that is supported by the common PowerLed software. This software comes bundled with a lot of signs as far as I can tell that come off of eBay, Alibaba, Amazon, etc. and can be frustrating to work with since there is no programmable interface with which to update the signs with dynamic content pulled from the internet, like from a Google Calendar. Pywinauto is awesome for automating using GUIs on Windows, and I was originally investigating it for use in automated testing when I realized that I could use an old Intel compute stick to update my LED sign on a regular interval and pull down the latest information from my Google Calendar! In just a few lines we evade the challenge of reverse engineering some proprietary software and provide a new use for an older PC that otherwise could have become e-waste.

## Getting Started

These instructions will help you deploy this project and help you get up and running quickly.

1. Clone this project somewhere on a Windows machine (I recommend an old laptop or compute stick, since this project will run in a loop forever.)
2. Set up your LED display and install the included PowerLed software (if you have another program for your sign you will need to modify the code in main.py to automate using your software)
3. Install the prerequisites. You must have Python 3 and pip installed. Afterwards, install the packages listed in requirements.txt
4. Fill in the information at the top of main.py with your network name, the version of PowerLed you are using, and your time zone.
5. [Follow the instructions in the Google Calendar Python Quickstart](https://developers.google.com/calendar/quickstart/python) to generate the required credentials file and to enable the Google Calendar API using your Google account.
6. Open display.ledproj in PowerLed. Close PowerLed
7. Run main.py. You should see the closest five events from your Google Calendar scrolling across the screen! The information displayed will update every three minutes, but you can make this more frequent or infrequent at the top of main.py.

### Prerequisites

This project requires that you are running Windows and have PowerLed installed. Additionally, this project was written in Python 3.

You can install all Python prerequisites at once using requirements.txt and pip. From inside the project directory, run:

```
pip install -r requirements.txt
```

## Authors

* **Kevin Loeffler** - [My Website](www.kevinmloeffler.com)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
