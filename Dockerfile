FROM ubuntu:20.04

WORKDIR /usr/src/app

RUN apt-get update -y
RUN apt-get install python3-pip python3-wheel -y
RUN apt-get install cron -y

# to install psycopg2:
RUN apt-get install gcc libpq-dev -y 


COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD python3 main.py && cron -f