FROM ubuntu:20.04

WORKDIR /usr/src/app

RUN apt-get update -y
RUN apt-get install python3-pip -y
RUN apt-get install cron -y

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

RUN python3 main.py

CMD cron -f