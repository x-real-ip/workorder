# FROM python:3.9.0b4-alpine3.12

# COPY ./app/worker /app/worker

# RUN /usr/bin/crontab /app/worker/crontab

# CMD /usr/sbin/crond -f -l 8

# ################################# 

FROM python:3.10

RUN apt-get -y update \
    && apt-get install -y \
    cron

COPY ./app/worker /app/worker

RUN /usr/bin/crontab /app/worker/crontab

# CMD /usr/sbin/crond -f -l 8
CMD ["cron", "-f -l 8"]