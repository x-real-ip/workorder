FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app/api /code/app

ENV PYTHONUNBUFFERED=1

WORKDIR /code/app

ENTRYPOINT ["python", "api_main.py"]