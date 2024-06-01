import random
import psycopg2
from psycopg2.extras import execute_values
from gen_utils import get_random_string

def fill_clients(connection, target_entries_count, min_accounts_per_client, max_accounts_per_client):
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM clients")
        existing_items_count = cursor.fetchone()[0]
    try:
        entries_to_add = target_entries_count - existing_items_count
        if entries_to_add <= 0:
            return
        entries_to_insert=list()
        for _ in range(entries_to_add):
                entries_to_insert.append((get_random_string(1, 40),))
        with connection.cursor() as cursor:
            execute_values(cursor, "INSERT INTO clients (client_name) VALUES %s", entries_to_insert)
            cursor.execute("SELECT client_id FROM clients ORDER BY client_id DESC LIMIT %s", [entries_to_add])
            inserted_ids = reversed([entry[0] for entry in cursor.fetchall()])
        owner_ids=list()
        for inserted_id in inserted_ids:
            for _ in range(random.randint(min_accounts_per_client, max_accounts_per_client)):
                owner_ids.append((inserted_id,))
        random.shuffle(owner_ids)
        with connection.cursor() as cursor:
            execute_values(cursor, "INSERT INTO client_accounts (owner_client_id) VALUES %s", owner_ids)
    except Exception as e:
        print(f"An error occurred: {e}")
        connection.rollback()
        raise e
    connection.commit()