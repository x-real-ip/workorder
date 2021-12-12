FROM python:3.10-alpine

RUN pip install --upgrade pip

ENV PYTHONUNBUFFERED=1

WORKDIR /app/worker

COPY /app/worker/requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app/worker .

RUN /usr/bin/crontab /app/worker/crontab

CMD /usr/sbin/crond -f -l 8