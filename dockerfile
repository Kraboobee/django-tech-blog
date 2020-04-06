FROM python:3.8-slim-buster

ADD . /usr/src/app

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt ./

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD exec gunicorn coded_nineteen.wsgi:application --bind 0.0.0.0:8000 --workers 3