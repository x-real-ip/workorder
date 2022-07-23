FROM joyzoursky/python-chromedriver:3.9

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    cron

RUN mkdir -p /app/log

WORKDIR /app/worker

COPY /src/app/worker .

COPY /src/app/logging.ini .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN chmod -R 755 /app/worker

RUN crontab /app/worker/crontab

CMD ["./entry.sh"]