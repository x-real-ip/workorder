FROM python:3.10

# Install Cron
RUN apt-get update
RUN apt-get -y install cron

WORKDIR /app/worker

# Add crontab file in the cron directory
COPY /app/worker .

# Give execution rights on the cron job
RUN chmod 0644 crontab

# Apply cron job
RUN /usr/bin/crontab /app/worker/crontab

CMD ["cron", "-f"]