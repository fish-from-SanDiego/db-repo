import os
import psycopg2
import re
import sys
from packaging.version import Version

db_creator_password = os.getenv('DB_CREATOR_PASSWORD')
main_db_name = os.getenv('MAIN_DB_NAME')
db_creator_name = os.getenv('DB_CREATOR_NAME')
max_migration_version = os.getenv('MAX_MIGRATION_VERSION')
hostname=os.getenv('DB_HOSTNAME')
port=int(os.getenv('HAPROXY_PRIMARY_PORT'))
script_location=os.path.dirname(os.path.realpath(__file__))
files_location = f"{script_location}/migration_files"
connection = psycopg2.connect(
    dbname=main_db_name,
    user=db_creator_name,
    password=db_creator_password,
    host=hostname,
    port=port
)
connection.autocommit = False
filenames = []
if max_migration_version is None:
    filenames = sorted(
        [f for f in os.listdir(files_location) if re.match(r'.*\.sql', f)],
        key=lambda x: Version(x.split('_')[0])
    )
    max_migration_version=filenames[-1].split('_')[0]
else:
    temp_filenames = sorted(
        [f for f in os.listdir(files_location) if re.match(r'.*\.sql', f)],
        key=lambda x: Version(x.split('_')[0])
    )
    for filename in temp_filenames:
        version = filename.split('_')[0]
        if not Version(version) <= Version(max_migration_version):
            break
        filenames.append(filename)
for filename in filenames:
    path_to_command = os.path.join(files_location, filename)
    with open(path_to_command, 'r') as file:
        with connection.cursor() as cursor:
            sql = file.read()
            try:
                cursor.execute(sql)
            except Exception as e:
                connection.rollback()
                print(f"Failed to execute {filename}: {e}")
                sys.exit(1)
            connection.commit()
            print(f"{filename} executed")

connection.close()
with open(f"{os.path.abspath(os.path.join(script_location, os.pardir))}/util_files/max_migration_version.txt", 'w') as f:
    print(max_migration_version, file = f)