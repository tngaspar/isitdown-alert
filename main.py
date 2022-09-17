from crontab import CronTab
import yaml
import re
from utils.db import PostgresDB

# if not exists, create schema and table to store crontab jobs execution data
conn = PostgresDB()
conn.create_cron_history_table()

# create dim_webpages_table
with open('sql/DDL/create_dim_webpages.pgsql', 'r') as file:
    sql_str = file.read()
conn.execute_sql(sql_str)

def _insert_dim_webpages(webpage):
    """inserts new record to cron.dim_webpages table
    
    Args:
    webpage: record from webpages.yaml file
    """
    sql_str = f"""
    INSERT INTO cron.dim_webpages (tag, url, interval) 
    VALUES ('{webpage.get('tag')}', '{webpage.get('url')}', '{webpage.get('interval')}');
    """
    conn = PostgresDB()
    conn.execute_sql(sql_str)


def _add_interval(job, item, interval):
    if re.match("[0-9]+m$", interval):
        num = int(interval.replace('m',''))
        job.minute.every(num)
    elif re.match("[0-9]+h$", interval):
        num = int(interval.replace('h',''))
        job.minute.on(0)
        job.hour.every(num)
    elif re.match("[0-9]+d$", interval):
        num = int(interval.replace('d',''))
        job.minute.on(0)
        job.hour.on(10)
        job.day.every(num)
    else:
        raise ValueError(f"'{interval}' is an invalid interval for {item}. Expected #m, #h, #d where # is an integer.")

cron = CronTab(user=True)

cron.remove_all(comment="isitdown")

with open(r'webpages.yaml') as file:
    webpages = yaml.full_load(file).get('webpages')
    
for item, webpage in webpages.items():
    print(item, ":", webpage)
    job = cron.new(command=f'/usr/bin/python3 /usr/src/app/utils/job.py {webpage.get("url")} "{webpage.get("tag")}"', comment='isitdown')
    _add_interval(job, item, webpage.get('interval'))
    _insert_dim_webpages(webpage)
    
cron.write()

for j in cron:
    print(j)
