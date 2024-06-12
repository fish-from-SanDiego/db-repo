def fill_company_accounts(connection, target_entries_count):
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM company_accounts")
        existing_items_count = cursor.fetchone()[0]
    try:
        entries_to_add = target_entries_count - existing_items_count
        if entries_to_add <= 0:
            return
        with connection.cursor() as cursor:
            for _ in range(entries_to_add):
                cursor.execute("INSERT INTO company_accounts DEFAULT VALUES")
    except Exception as e:
        print(f"An error occurred: {e}")
        connection.rollback()
        raise e
    connection.commit()