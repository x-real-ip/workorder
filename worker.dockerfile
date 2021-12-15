FROM python:3.10

ENV PYTHONUNBUFFERED=1

RUN apt-get update \
 && apt-get install -y \
    cron \
    unzip

RUN mkdir -p /app/log

WORKDIR /app/worker

COPY /app/worker .

COPY /app/logging.ini .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get update \
 && apt-get install -y \
    google-chrome-stable

# set display port to avoid crash
ENV DISPLAY=:99

RUN chmod -R 755 /app/worker

RUN crontab /app/worker/crontab

CMD ["./entry.sh"]