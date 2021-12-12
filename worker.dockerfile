FROM python:3.10

# Install Cron
RUN apt-get update
RUN apt-get -y install cron

# Add crontab file in the cron directory
COPY /app/worker/crontab /etc/cron.d/crontab
COPY /app/worker/test.py /app/worker/test.py

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/crontab /app/worker/test.py

# Apply cron job
RUN /usr/bin/crontab /etc/cron.d/crontab

CMD ["cron", "-f"]