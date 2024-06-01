CREATE TABLE IF NOT EXISTS item_models(
    item_model_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    item_model_name VARCHAR(60) NOT NULL UNIQUE
);