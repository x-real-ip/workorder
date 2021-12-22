# Workorder

[![Build Status](https://drone.theautomation.nl/api/badges/theautomation/workorder/status.svg)](https://drone.theautomation.nl/theautomation/workorder)
![GitHub repo size](https://img.shields.io/github/repo-size/theautomation/workorder?logo=Github)
![GitHub commit activity](https://img.shields.io/github/commit-activity/y/theautomation/workorder?logo=github)
![GitHub last commit (branch)](https://img.shields.io/github/last-commit/theautomation/workorder/main?logo=github)

Table of contents:

- [Requirements](#Requirements)

- [How it works](#How-it-works)

- [Setup](#Setup)
  - [Docker host](#Docker-host)
  - [Android](#Android)

## Requirements

- A server, PC, or other device running [Docker](https://www.docker.com/).
- Android device to run [Tasker](https://play.google.com/store/apps/details?id=net.dinglisch.android.taskerm).

## How it works

1. Tasker (your phone) monitors whether you arrive at work :office: based on the WiFi signal that your phone receives and stores the date and start time locally in a tasker variable, the same happens when you leave work, an end time will be stored. A notification with the saved time appears after a trigger <img src="https://github.com/theautomation/workorder/blob/951f223d4b21501b629758aaaa5f81fd2cefe7a4/images/starttime.jpg" height="200">

2. If new data is stored in Tasker the saved times will be sent to the API and stored in a database only if the phone is connected to the home :house: WiFi network because the API can only be accessed from the locale network. This will be executed at fixed time 04:00 in the morning, the time can be changed in the Tasker XML or in the Tasker App. (Docker API container)

3. At 07:00 data is retrieved from the database, entered into the workorder and sent. A python script take care of this part. (Docker Worker container)

Tasker is an application for Android which performs tasks (sets of actions) based on contexts (application, time, date, location, event, gesture) in user-defined profiles or in clickable or timer home screen widgets.
In this project Tasker will monitor if you are on your work location or home location based on near or connected wifi SSID signal. More info [here](https://tasker.joaoapps.com/)

## Setup

### Docker host

1. Clone this repository to your docker host.

```bash
git clone https://github.com/theautomation/workorder.git
```

2. Change "prd-workorder-app.env.example to "prd-workorder-app.env".

```bash
mv ./prd-workorder-app.env.example ./prd-workorder-app.env
```

3. Fill in the URL, username and password in the "prd-workorder-app.env" file.

```dosini
# URL to open
WEB_URL="https://example.com"

# Credentials for WEB_URL login
WEB_USERNAME="username"
WEB_PASSWORD="password"

# All workorders have text, to find and fill in the correct workorder, make a comma separated list of words to search for.
# The words may be part of text for e.g. if the word "dienst" is in the list it will find "Weekenddienst", "Avonddienst" and "Dagdienst"
# The rule is, if it contains {word} case sensitive
WORKORDER_WORDS="dienst, Operator, motorkap"

# Save a .png image of the workorder with filled in time
# Set true to save a image or set false or empty to not save a image
# The path where images will be saved in the 'worker' docker container is '/app/log'
SAVE_IMAGE=true
```

### Android

1. Install [Tasker](https://play.google.com/store/apps/details?id=net.dinglisch.android.taskerm).
2. Download or copy the Tasker project XML on your device [Link](https://github.com/theautomation/workorder/blob/338ae2deb2da5e7adcc8147920e9896fe62d7ce7/tasker/workday.prj.xml)
