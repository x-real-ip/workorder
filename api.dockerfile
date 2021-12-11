FROM python:3.10

COPY /app/api /code

WORKDIR /code

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

ENV PYTHONUNBUFFERED=1

CMD ["python", "api_main.py"]