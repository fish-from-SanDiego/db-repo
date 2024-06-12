from collections import defaultdict
from datetime import datetime, timedelta
import random
import psycopg2
from psycopg2.extras import execute_values
from psycopg2.extras import execute_batch
from faker import Faker

def fill_contracts(connection, target_entries_count, min_transactions_per_contract, max_transactions_per_contract,
                    min_items_per_contract, max_items_per_contract, min_employees_per_contract, max_employees_per_contract):
    # max_batch_size = 100000
    min_start_date = datetime(2020, 1, 1)
    max_end_date = datetime.now() + timedelta(days = 365 * 10)
    contract_types = ['rent', 'purchase', 'sale']
    is_income_options = [False, True]
    with connection.cursor() as cursor:
        cursor.execute("SELECT owner_client_id, account_id FROM client_accounts")
        client_account_ids = defaultdict(list)
        for entry in cursor.fetchall():
            client_account_ids[entry[0]].append(entry[1])
        cursor.execute("SELECT company_account_id FROM company_accounts")
        company_account_ids = [entry[0] for entry in cursor.fetchall()]
        cursor.execute("SELECT employee_id FROM employees")
        employee_ids = [entry[0] for entry in cursor.fetchall()]
        cursor.execute("SELECT item_id FROM items")
        item_ids = [entry[0] for entry in cursor.fetchall()]
    with connection.cursor() as cursor:
        cursor.execute("PREPARE insert_contract (DATE, DATE, DATE, DECIMAL(14,2), type_of_contract, INTEGER) AS INSERT INTO contracts(begin_date, end_date, actual_end_date, supposed_total_sum, contract_type, client_id) VALUES($1, $2, $3, $4, $5, $6) RETURNING contract_id")
        cursor.execute("PREPARE insert_contract_item (INTEGER, INTEGER) AS INSERT INTO contracts_items(contract_id, item_id) VALUES($1, $2)")
        cursor.execute("PREPARE insert_contract_employee (INTEGER, INTEGER) AS INSERT INTO employees_contracts(employee_id, contract_id) VALUES($1, $2)")
        cursor.execute("SELECT COUNT(*) FROM contracts")
        existing_items_count = cursor.fetchone()[0]
    
    entries_to_add = target_entries_count - existing_items_count
    if entries_to_add <= 0:
        return
    fake = Faker()
    client_ids = list(client_account_ids.keys())
    print(entries_to_add)
    for i in range(entries_to_add):
        try:
            if i % 10000 == 0:
                print(i)
                connection.commit()
            begin_date = fake.date_between(start_date=min_start_date)
            end_date = fake.date_between(start_date=datetime.now(), end_date = max_end_date)
            actual_end_date = random.choice([None, fake.date_between(start_date=begin_date, end_date = datetime.now())])
            if actual_end_date is None:
                real_end_date = end_date
            else:
                real_end_date = actual_end_date
            supposed_total_sum = fake.pydecimal(left_digits = random.randint(1,12), right_digits = 2, positive = True)
            client_id = random.choice(client_ids)
            contract_type = random.choice(contract_types)
            item_ids_for_contract = random.sample(item_ids, random.randint(min_items_per_contract, max_items_per_contract))
            employee_ids_for_contract = random.sample(employee_ids, random.randint(min_employees_per_contract, max_employees_per_contract))
            with connection.cursor() as cursor:
                cursor.execute("EXECUTE insert_contract (%s, %s, %s, %s, %s, %s)", (begin_date, end_date, actual_end_date, supposed_total_sum, contract_type, client_id))
                cur_contract_id = cursor.fetchone()[0]
                item_entries = [(cur_contract_id, item_id) for item_id in item_ids_for_contract]
                employee_entries = [(employee_id, cur_contract_id) for employee_id in employee_ids_for_contract]
                if len(item_entries) > 0:
                    execute_batch(cursor,"EXECUTE insert_contract_item (%s, %s)", item_entries)
                if len(employee_entries) > 0:
                    execute_batch(cursor,"EXECUTE insert_contract_employee (%s, %s)", employee_entries)
            transactions_count = random.randint(min_transactions_per_contract, max_transactions_per_contract)
            if transactions_count > 0:
                transaction_entries=list()
                for _ in range(transactions_count):
                    is_income = random.choice(is_income_options)
                    transaction_time = fake.date_time_between(start_date = begin_date, end_date = real_end_date).replace(microsecond=0)
                    company_account_id = random.choice(company_account_ids)
                    client_account_id = random.choice(client_account_ids[client_id])
                    transaction_sum = fake.pydecimal(left_digits = random.randint(1,12), right_digits = 2, positive = True)
                    transaction_entries.append((transaction_time, transaction_sum, company_account_id, client_account_id, cur_contract_id, is_income))
                with connection.cursor() as cursor:
                    execute_values(cursor, "INSERT INTO account_transactions(transaction_time, transaction_sum, company_account_id,     client_account_id, transaction_contract_id, is_income) VALUES %s", transaction_entries)

        except Exception as e:
            print(f"An error occurred: {e}")
            connection.rollback()
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM contracts")
                existing_items_count = cursor.fetchone()[0]
                entries_to_add = target_entries_count - existing_items_count
                i = 0


    connection.commit()