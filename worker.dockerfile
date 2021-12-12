# FROM python:3.9.0b4-alpine3.12

# COPY ./app/worker /app/worker

# RUN /usr/bin/crontab /app/worker/crontab

# CMD /usr/sbin/crond -f -l 8

# ################################# 

# FROM python:3.10

# RUN apt-get -y update \
#     && apt-get install -y \
#     cron

# COPY ./app/worker /app/worker

# RUN /usr/bin/crontab /app/worker/crontab

# # CMD /usr/sbin/crond -f -l 8
# CMD ["cron", "-f"]


#####################################
FROM python:3.10

# Install Cron
RUN apt-get update
RUN apt-get -y install cron

# Add crontab file in the cron directory
COPY /app/worker/crontab /etc/cron.d/crontab
COPY /app/worker/test.py /app/worker/test.py

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/crontab /app/worker/test.py

# Apply cron job
RUN /usr/bin/crontab /etc/cron.d/crontab

CMD ["cron", "-f"]