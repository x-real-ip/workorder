FROM python:3.9.0b4-alpine3.12

WORKDIR /app/worker

COPY ./app/worker .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN /usr/bin/crontab /app/worker/crontab

CMD /usr/sbin/crond -f -l 8