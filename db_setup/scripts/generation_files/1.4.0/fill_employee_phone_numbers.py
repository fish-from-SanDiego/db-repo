import random
import psycopg2
import phonenumbers
from faker import Faker
from psycopg2.extras import execute_values

def normalize_phone_number(phone_number, region):
    try:
        parsed_number = phonenumbers.parse(phone_number, region)
        return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
    except:
        return None
def fill_employee_phone_numbers(connection, target_entries_count, min_phone_number_owners, max_phone_number_owners):
    with connection.cursor() as cursor:
        cursor.execute("SELECT phone_number FROM employee_phone_numbers")
        existing_phone_numbers = {entry[0] for entry in cursor.fetchall()}
        existing_phone_numbers_count = len(existing_phone_numbers)
        cursor.execute("SELECT employee_id FROM employees")
        employee_ids = [entry[0] for entry in cursor.fetchall()]
    try:
        entries_to_add = target_entries_count - existing_phone_numbers_count
        if entries_to_add <= 0:
            return
        numbers_to_insert=list()
        fake = Faker('ru_RU')
        while len(numbers_to_insert) < entries_to_add:
            phone_number = normalize_phone_number(fake.unique.phone_number(), 'RU')
            if not phone_number or len(phone_number) != 12:
                continue
            if phone_number not in existing_phone_numbers:
                numbers_to_insert.append((phone_number,))
                existing_phone_numbers.add(phone_number)
        with connection.cursor() as cursor:
            execute_values(cursor, "INSERT INTO employee_phone_numbers (phone_number) VALUES %s", numbers_to_insert)
            cursor.execute("SELECT phone_number_id FROM employee_phone_numbers ORDER BY phone_number_id DESC LIMIT %s", [entries_to_add])
            inserted_ids = reversed([entry[0] for entry in cursor.fetchall()])
        many_to_many_tuples = list()
        for inserted_id in inserted_ids:
            cur_employee_ids = random.sample(employee_ids, random.randint(min_phone_number_owners, max_phone_number_owners))
            for employee_id in cur_employee_ids:
                many_to_many_tuples.append((employee_id, inserted_id))
        random.shuffle(many_to_many_tuples)
        with connection.cursor() as cursor:
            execute_values(cursor, "INSERT INTO employees_employee_phone_numbers (owner_employee_id, owner_phone_number_id) VALUES %s", many_to_many_tuples)

            
    except Exception as e:
        print(f"An error occurred: {e}")
        connection.rollback()
        raise e
    connection.commit()