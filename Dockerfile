FROM ubuntu:21.04

# install wget to set up the PPA and xvfb to have a virtual screen and unzip to install the Chromedriver
RUN apt-get update && apt-get install -y \
    wget \
    xvfb \
    gnupg2 \
    unzip

# Set up the Chrome PPA
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

# Run non interactive to aviod tzdata geographical location
ENV DEBIAN_FRONTEND="noninteractive" TZ="Europe/Amsterdam"

# Update the package list and install chrome
RUN apt-get update -y
RUN apt-get install -y google-chrome-stable

# Set up Chromedriver Environment variables
ENV CHROMEDRIVER_VERSION 2.19
ENV CHROMEDRIVER_DIR /chromedriver
RUN mkdir $CHROMEDRIVER_DIR

# Download and install Chromedriver
RUN wget -q --continue -P $CHROMEDRIVER_DIR "http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
RUN unzip $CHROMEDRIVER_DIR/chromedriver* -d $CHROMEDRIVER_DIR

# Put Chromedriver into the PATH
ENV PATH $CHROMEDRIVER_DIR:$PATH

# Install Python and cron
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    cron 

COPY ./requirements.txt /code/requirements.txt

WORKDIR /code

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

ENV DISPLAY=:99

EXPOSE 8000

WORKDIR /code/app

COPY ./cronjob /etc/cron.d/cronjob

RUN chmod 0644 /etc/cron.d/cronjob \
    && crontab /etc/cron.d/cronjob

CMD ["python3", "app_main.py"]
