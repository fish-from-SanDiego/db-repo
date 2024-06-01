from psycopg2.extras import execute_values
from gen_utils import get_random_string

def fill_model_categories(connection, target_entries_count):
    with connection.cursor() as cursor:
        cursor.execute("SELECT model_category_name FROM model_categories")
        existing_names = {entry[0] for entry in cursor.fetchall()}
        existing_names_count = len(existing_names)
    try:
        entries_to_add = target_entries_count - existing_names_count
        if entries_to_add <= 0:
            return
        names_to_insert=list()
        while len(names_to_insert) < entries_to_add:
            category_name = get_random_string(1, 40)
            if category_name not in existing_names:
                names_to_insert.append((category_name,))
                existing_names.add(category_name)
                
        with connection.cursor() as cursor:
            execute_values(cursor, "INSERT INTO model_categories (model_category_name) VALUES %s", names_to_insert)
    except Exception as e:
        print(f"An error occurred: {e}")
        connection.rollback()
        raise e
    connection.commit()