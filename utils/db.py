import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
HOST = os.environ.get('HOST')
USER = os.environ.get('POSTGRESUSER')
PASSWORD = os.environ.get('POSTGRESPASSWORD')
DATABASE = os.environ.get('DATABASE')

class PostgresDB:

    def __init__(self, user: str=USER, password: str=PASSWORD, database: str=DATABASE, port: str=None, host: str=HOST):
        try:
            self.connection = psycopg2.connect(user = user,
                                    password = password,
                                    host = host,
                                    port = port,
                                    database = database)
            
            cursor = self.connection.cursor()
            cursor.execute("SELECT version();")

            record = cursor.fetchone()
            print("Successfully connected to - ", record,"\n")
            cursor.close()
        
        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL", error)

    def get_table_from_sql(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        
        return records
    
    def execute_sql(self, sql: str):
        """Executes SQL query

        Args:
            sql (str): sql query string
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            cursor.close()
            self.connection.commit()
        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL", error)
            
        
    def create_cron_history_table(self, schema_name: str="cron", table_name: str="history"):
        """Creates cron.history table if it doesn't already exists.
        
        Args:
            schema_name: (str): name of the schema. Defaults to "cron".
            table_name (str): name of the table. Defaults to "history".
        """
        sql = f"""
            CREATE SCHEMA IF NOT EXISTS {schema_name};
            CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} (
                id SERIAL PRIMARY KEY,
                request_time TIMESTAMPTZ NOT NULL,
                tag VARCHAR(2000),
                url VARCHAR(2000) NOT NULL,
                is_up BOOLEAN NOT NULL,
                status_code INT,
                response_url VARCHAR(2000)
        );
        """
        self.execute_sql(sql)
    
    
    def insert_cron_history_table(self, request_time, tag, url, is_up, status_code, response_url, 
                                  schema_name: str="cron", table_name: str="history"):
        """Inserts record into cron.history table.
        
        Args:
            schema_name(str): name of the schema. Defaults to "cron".
            table_name(str): name of the table. Defaults to "history".
            request_time(str): time of when the request was made.
            tag(str): webpage tag.
            url(str): URL of the web page.
            is_up(bool): True if webpage is up. Else False.
            status_code(int): HTTP status code.
            response_url(str): URL returned from http request.
        """
        
        sql = f"""
            INSERT INTO "{schema_name}"."{table_name}" ("request_time", "tag", "url", "is_up", "status_code", "response_url")
            VALUES ('{request_time}', '{tag}', '{url}', {is_up}, {status_code}, '{response_url}');
        """
        self.execute_sql(sql)
        
        
    def drop_table(self, schema_name: str, table_name: str):
        """Drop the specified table from the database

        Args:
            schema_name (str): schema name of table to drop.
            table_name (str): table name to drop.
        """
        sql = f"DROP TABLE IF EXISTS {schema_name}.{table_name};"
        self.execute_sql(sql)
        