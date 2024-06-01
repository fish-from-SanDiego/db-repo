import random
import psycopg2
from faker import Faker
from psycopg2.extras import execute_values

def fill_employees(connection, target_entries_count):
    with connection.cursor() as cursor:
        cursor.execute("SELECT occupation_id FROM employee_occupations")
        occupation_ids = [entry[0] for entry in cursor.fetchall()]
        cursor.execute("SELECT COUNT(*) FROM employees")
        existing_employees_count = cursor.fetchone()[0]

    try:
        entries_to_add = target_entries_count - existing_employees_count
        if entries_to_add <= 0:
            return
        entries_to_insert=list()
        fake = Faker()
        for _ in range(entries_to_add):
                name = fake.name()
                occupation_id = random.choice(occupation_ids)
                salary = fake.pydecimal(left_digits = random.randint(1,12), right_digits = 2, min_value = 0)
                entries_to_insert.append((name, occupation_id, salary))
        with connection.cursor() as cursor:
            execute_values(cursor, "INSERT INTO employees (employee_full_name, employee_occupation_id, salary) VALUES %s", entries_to_insert)

            
    except Exception as e:
        print(f"An error occurred: {e}")
        connection.rollback()
        raise e
    connection.commit()