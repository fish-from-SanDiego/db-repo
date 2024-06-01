CREATE TABLE IF NOT EXISTS client_accounts(
    account_id INTEGER PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    owner_client_id INTEGER NOT NULL REFERENCES clients(client_id)
);