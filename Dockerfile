FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

EXPOSE 8000

WORKDIR /code/app

CMD ["uvicorn", "app_api:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]