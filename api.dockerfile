FROM python:3.10

WORKDIR /app/api

COPY ./app/api /app/api

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

ENV PYTHONUNBUFFERED=1

CMD ["python", "api_main.py"]