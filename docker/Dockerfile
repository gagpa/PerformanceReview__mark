FROM python:3.8

RUN mkdir -p /usr/src/hr-test-bot/
WORKDIR /usr/src/hr-test-bot
COPY requirements.txt /usr/src/hr-test-bot/
RUN pip install -r requirements.txt

RUN pip install --upgrade pip
RUN apt update
