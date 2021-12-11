FROM python:3.10

RUN mkdir -p /app/db

COPY ./app/api /app/api

WORKDIR /app/api

RUN pip install --no-cache-dir --upgrade -r /app/api/requirements.txt

ENV PYTHONUNBUFFERED=1

CMD ["python", "api_main.py"]