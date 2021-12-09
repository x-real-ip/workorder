# Workorder

## Requirements

- a server running docker.
- a Android device to run Tasker.

## How it works

On your Android device tasker will monitor if you are on your work location or home location based on near or connected wifi SSID signal.

## Setup

1. Pull this repository to your docker host.

```bash
git clone https://github.com/theautomation/workorder.git
```

2. Change "prd-workorder-app.env.example to Change "prd-workorder-app.env".

```bash
mv ./prd-workorder-app.env.example ./prd-workorder-app.env

```

3. Fill in the URL, username and password in the "prd-workorder-app.env" file.
