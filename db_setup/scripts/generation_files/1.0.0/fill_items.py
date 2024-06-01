import random
from psycopg2.extras import execute_values

def fill_items(connection, target_entries_count):
    conditions = ['new', 'used', 'slightly damaged', 'damaged', 'repaired', 'broken']
    with connection.cursor() as cursor:
        cursor.execute("SELECT item_model_id FROM item_models")
        model_ids = [entry[0] for entry in cursor.fetchall()]
        cursor.execute("SELECT COUNT(*) FROM items")
        existing_items_count = cursor.fetchone()[0]
    try:
        entries_to_add = target_entries_count - existing_items_count
        if entries_to_add <= 0:
            return
        entries_to_insert=list()
        for _ in range(entries_to_add):
                entries_to_insert.append((random.choice(model_ids), random.choice(conditions)))
        with connection.cursor() as cursor:
            execute_values(cursor, "INSERT INTO items (item_model_id, condition) VALUES %s", entries_to_insert)
    except Exception as e:
        print(f"An error occurred: {e}")
        connection.rollback()
        raise e
    connection.commit()