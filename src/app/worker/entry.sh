#!/bin/bash

# Print env to globally environment for cron
printenv | grep -v "no_proxy" >> /etc/environment

# Start cron
cron -f