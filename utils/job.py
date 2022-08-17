import http_request
import mail
import argparse
from dotenv import load_dotenv
import os
import datetime
import pytz
from db import PostgresDB

# Get environment variables from .env
load_dotenv()
SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
APP_PASSWORD = os.environ.get('APP_PASSWORD')
TIME_ZONE = os.environ.get('TIME_ZONE')
RECEIVER_EMAIL = os.environ.get('RECEIVER_EMAIL')
tzone = pytz.timezone(TIME_ZONE)

# SendEmail instance
email_sender = mail.SendEmail(SENDER_EMAIL, APP_PASSWORD, RECEIVER_EMAIL)

# CLI arguments
parser = argparse.ArgumentParser(description="Check if website is up and sends email")

parser.add_argument('url', type=str, nargs=1, help="Webpage URL")
parser.add_argument('tag', type=str, nargs=1, help="Webpage name and/or description")

args = parser.parse_args()
url = args.url[0]
tag = args.tag[0]

# check if webpage is up
is_up, status_code, response_url = http_request.status(url)
current_time = datetime.datetime.now(tzone)


# save response to database
conn = PostgresDB()
conn.insert_cron_history_table(current_time, tag, url, is_up, status_code, response_url)


# send email
if not is_up:
    subject = f"Webpage Down: {tag} ({url})"
    body=f"Could not reach {url}.\n\nURL: {url}\nTag: {tag}\nTimestamp: {current_time}"
    email_sender.send(subject, body)
    