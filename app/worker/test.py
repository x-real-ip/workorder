#!/usr/bin/python

import os

# Check os env variables
if "WEB_URL" in os.environ:
    web_url = os.environ.get("WEB_URL")
    print(web_url)
else:
    print("no env")
