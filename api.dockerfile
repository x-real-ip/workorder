FROM python:3.10

WORKDIR /app/api

RUN mkdir -p /app/db /app/log

COPY ./app/api /app/api

RUN pip install --no-cache-dir --upgrade -r /app/api/requirements.txt

ENV PYTHONUNBUFFERED=1

CMD ["python", "api_main.py"]