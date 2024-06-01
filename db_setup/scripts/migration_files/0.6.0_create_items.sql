CREATE TABLE IF NOT EXISTS items(
    item_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    item_model_id INTEGER NOT NULL REFERENCES item_models(item_model_id),
    condition item_condition NOT NULL
);