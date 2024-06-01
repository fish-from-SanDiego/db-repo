import random
import psycopg2
from psycopg2.extras import execute_values
from gen_utils import get_random_string
from faker import Faker

def fill_employee_occupations(connection, target_entries_count):
    faker_jobs_number=639
    with connection.cursor() as cursor:
        cursor.execute("SELECT occupation_name FROM employee_occupations")
        existing_occupations = {entry[0] for entry in cursor.fetchall()}
        existing_occupations_count = len(existing_occupations)
    try:
        entries_to_add = target_entries_count - existing_occupations_count
        if entries_to_add <= 0:
            return
        if target_entries_count > faker_jobs_number:
            print(f"maximum number of occupations is {faker_jobs_number} due to python faker's limit")
            return
        entries_to_insert=list()
        fake = Faker()
        while len(entries_to_insert) < entries_to_add:
            occupation_name = fake.unique.job()
            if occupation_name not in existing_occupations:
                entries_to_insert.append((occupation_name,))
                existing_occupations.add(occupation_name)
                
        with connection.cursor() as cursor:
            execute_values(cursor, "INSERT INTO employee_occupations (occupation_name) VALUES %s", entries_to_insert)
    except Exception as e:
        print(f"An error occurred: {e}")
        connection.rollback()
        raise e
    connection.commit()