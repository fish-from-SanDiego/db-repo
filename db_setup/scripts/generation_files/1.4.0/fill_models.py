import random
from psycopg2.extras import execute_values
from gen_utils import get_random_string

def fill_models(connection, target_entries_count, min_categories_per_model, max_categories_per_model):
    with connection.cursor() as cursor:
        cursor.execute("SELECT model_category_id FROM model_categories")
        category_ids = [entry[0] for entry in cursor.fetchall()]
        cursor.execute("SELECT item_model_name FROM item_models")
        existing_names = {entry[0] for entry in cursor.fetchall()}
        existing_names_count = len(existing_names)
    try:
        entries_to_add = target_entries_count - existing_names_count
        if entries_to_add <= 0:
            return
        names_to_insert=list()
        while len(names_to_insert) < entries_to_add:
            model_name = get_random_string(1, 40)
            if model_name not in existing_names:
                names_to_insert.append((model_name,))
                existing_names.add(model_name)
        with connection.cursor() as cursor:
            execute_values(cursor, "INSERT INTO item_models (item_model_name) VALUES %s", names_to_insert)
            cursor.execute("SELECT item_model_id FROM item_models ORDER BY item_model_id DESC LIMIT %s", [entries_to_add])
            inserted_ids = reversed([entry[0] for entry in cursor.fetchall()])
        many_to_many_tuples = list()
        for inserted_id in inserted_ids:
            cur_category_ids = random.sample(category_ids, random.randint(min_categories_per_model, max_categories_per_model))
            for category_id in cur_category_ids:
                many_to_many_tuples.append((inserted_id, category_id))
        with connection.cursor() as cursor:
            execute_values(cursor, "INSERT INTO models_model_categories (item_model_id, model_category_id) VALUES %s", many_to_many_tuples)
    except Exception as e:
        print(f"An error occurred: {e}")
        connection.rollback()
        raise e
    connection.commit()