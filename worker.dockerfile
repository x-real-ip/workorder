FROM python:3.9.0b4-alpine3.12

COPY ./app/worker /app/worker

RUN /usr/bin/crontab /app/worker/crontab

CMD /usr/sbin/crond -f -l 8