# #!/bin/bash
set -e

# Print env to globally environment for cron
printenv | grep -v "no_proxy" >> /etc/environment

# Start cron
cron -f

# echo "The following crontab is set:"

# cat /app/worker/crontab