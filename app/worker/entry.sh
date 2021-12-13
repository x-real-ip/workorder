#!/bin/bash

# print env to globally environment for cron.
printenv | grep -v "no_proxy" >> /etc/environment

# start cron
cron -f