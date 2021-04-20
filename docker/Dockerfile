FROM python:3.8

RUN mkdir -p /usr/src/hr-test-bot/
WORKDIR /usr/src/hr-test-bot

ADD ../requirements.txt /usr/src/hr-test-bot/requirements.txt
RUN apt update
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
