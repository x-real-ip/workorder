FROM python:3.10

RUN apt-get update && apt-get install -y \
    cron \
    unzip 

WORKDIR /app/worker

COPY /app/worker .

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod 0644 crontab

RUN /usr/bin/crontab /app/worker/crontab

CMD ["cron", "-f"]
