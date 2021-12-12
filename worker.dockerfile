FROM python:3.10-alpine

WORKDIR /app/worker

COPY ./app/worker /app/worker

COPY /app/worker/crontab /var/spool/cron/crontabs/crontab

RUN chmod +x /app/worker/test.py

CMD crond -l 2 -f