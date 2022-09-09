# syntax=docker/dockerfile:1
FROM python:3.8-bullseye

WORKDIR /build

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD gunicorn -w 4 --bind  0.0.0.0:$PORT app:app
