CREATE TABLE IF NOT EXISTS clients(
    client_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    client_name VARCHAR(60) NOT NULL
);