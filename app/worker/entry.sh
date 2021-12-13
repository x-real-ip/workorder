#!/bin/bash

# store env globally for cron.
printenv | > /etc/environment

# start cron
cron -f