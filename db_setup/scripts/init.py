import os
import psycopg2
import re
import sys
import time
pg_user=os.getenv('POSTGRES_USER')
pg_password=os.getenv('POSTGRES_PASSWORD')
pg_db_name=os.getenv('POSTGRES_DB')
db_creator_password = os.getenv('DB_CREATOR_PASSWORD')
main_db_name = os.getenv('MAIN_DB_NAME')
db_creator_name = os.getenv('DB_CREATOR_NAME')
hostname=os.getenv('DB_HOSTNAME')
port=int(os.getenv('HAPROXY_PRIMARY_PORT'))
max_try_attempts=int(os.getenv('MAX_INIT_ATTEMPTS'))
cooldown_time=int(os.getenv('INIT_COOLDOWN_ON_FAILURE'))
for i in range(max_try_attempts):
    print(f"attempt {i+1} to connect to database")
    try:
        connection = psycopg2.connect(
            dbname=pg_db_name,
            user=pg_user,
            password=pg_password,
            host=hostname,
            port=port
        )
    except Exception as e:
        print(e)
        print(f"attempt {i+1} to connect failed")
        connection = None
    if connection != None:
        print(f"attempt {i+1} to connect succeeded")
        break
    time.sleep(cooldown_time)
if connection == None:
    sys.exit(1)
connection.autocommit = True

with connection.cursor() as cursor:
    try:
        cursor.execute(f"""DO
$do$
BEGIN
   IF EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE rolname = '{db_creator_name}') THEN
      RAISE NOTICE 'Role {db_creator_name} already exists. Skipping.';
   ELSE
      CREATE ROLE {db_creator_name} WITH LOGIN PASSWORD '{db_creator_password}' CREATEDB;
   END IF;
END
$do$;""")
    except Exception as e:
        print("failed to execute init file")
        sys.exit(1)

connection = psycopg2.connect(
            dbname=pg_db_name,
            user=db_creator_name,
            password=db_creator_password,
            host=hostname,
            port=port
        )
connection.autocommit=True

with connection.cursor() as cursor:
    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (main_db_name,))
    exists = cursor.fetchone()
    if not exists:
        cursor.execute(f"CREATE DATABASE {main_db_name};")