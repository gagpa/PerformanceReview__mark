FROM python:3.9.5
ENV TZ=Europe/Moscow
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt
CMD python main.py