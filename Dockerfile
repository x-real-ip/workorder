FROM ubuntu:21.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    cron \
    wget \
    google-chrome-stable \
    unzip

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

ENV DISPLAY=:99

EXPOSE 8000

WORKDIR /code/app

COPY ./cronjob /etc/cron.d/cronjob

RUN chmod 0644 /etc/cron.d/cronjob \
    && crontab /etc/cron.d/cronjob

# CMD ["python", "app_main.py"]
