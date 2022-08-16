from sysconfig import is_python_build
import psycopg2

class PostgresDB:
    def __init__(self, user: str, password: str, database: str, port: str="5432", host: str="127.0.0.1"):
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

    def execute_sql(self, sql):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        cursor.close()
        self.connection.commit()
        
    def create_cron_history_table(self, schema_name: str="cron", table_name: str="history"):
        # create_table if not exists
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
        sql = f"""
            INSERT INTO "cron"."history" ("request_time", "tag", "url", "is_up", "status_code", "response_url")
            VALUES ('{request_time}', '{tag}', '{url}', {is_up}, {status_code}, '{response_url}');
        """
        self.execute_sql(sql)
        
    def drop_table(self, schema_name: str, table_name: str):
        sql = f"DROP TABLE IF EXISTS {schema_name}.{table_name};"
        self.execute_sql(sql)
        
    


# try:
#     connection = psycopg2.connect(user = "postgres",
#                                   password = "postgres",
#                                   host = "127.0.0.1",
#                                   port = "5433",
#                                   database = "isitdown_db")

#     cursor = connection.cursor()
#     # Print PostgreSQL Connection properties
#     print ( connection.get_dsn_parameters(),"\n")

#     # Print PostgreSQL version
#     cursor.execute("SELECT version();")
#     record = cursor.fetchone()
#     print("You are connected to - ", record,"\n")





# except (Exception, psycopg2.Error) as error :
#     print ("Error while connecting to PostgreSQL", error)
# finally:
#     #closing database connection.
#         if(connection):
#             cursor.close()
#             connection.close()
#             print("PostgreSQL connection is closed")