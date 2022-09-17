FROM ubuntu:20.04

WORKDIR /usr/src/app

RUN apt-get update -y
RUN apt-get install python3-pip -y

# to install psycopg2:
RUN apt-get install gcc libpq-dev -y 

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

WORKDIR /usr/src/app/app

CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app", "--workers=5"]