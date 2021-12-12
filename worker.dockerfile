FROM python:3.10

RUN pip install --upgrade pip

ENV PYTHONUNBUFFERED=1

WORKDIR /app/worker

COPY /app/worker/requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app/worker .

RUN apt-get -y update \
    && apt-get install -y \
    cron

RUN /usr/bin/crontab /app/worker/crontab

CMD /usr/sbin/crond -f -l 8