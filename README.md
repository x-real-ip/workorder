# Workorder

[![Build Status](https://drone.theautomation.nl/api/badges/theautomation/workorder/status.svg)](https://drone.theautomation.nl/theautomation/workorder)
![GitHub repo size](https://img.shields.io/github/repo-size/theautomation/workorder?logo=Github)
![GitHub commit activity](https://img.shields.io/github/commit-activity/y/theautomation/workorder?logo=github)
![GitHub last commit (branch)](https://img.shields.io/github/last-commit/theautomation/workorder/main?logo=github)

## Requirements

- A server, PC, or other device running [Docker](https://www.docker.com/).
- Android device to run [Tasker](https://play.google.com/store/apps/details?id=net.dinglisch.android.taskerm).

## How it works

Tasker is an application for Android which performs tasks (sets of actions) based on contexts (application, time, date, location, event, gesture) in user-defined profiles or in clickable or timer home screen widgets.
In this project Tasker will monitor if you are on your work location or home location based on near or connected wifi SSID signal.

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

## To Do

- [Take loglevel from env consol and file](https://gist.github.com/juanpabloaj/3e6a41f683c1767c17824811db01165b#file-logging_env-py)
- Notification when workorder has completed
- How many days back in time to use (db query and selenium workorder text to find)
