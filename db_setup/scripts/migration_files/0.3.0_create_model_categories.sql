CREATE TABLE IF NOT EXISTS model_categories(
    model_category_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    model_category_name VARCHAR(60) NOT NULL UNIQUE
);