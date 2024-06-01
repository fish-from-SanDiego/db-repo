CREATE TABLE IF NOT EXISTS models_model_categories(
    item_model_id INTEGER REFERENCES item_models(item_model_id),
    model_category_id INTEGER REFERENCES model_categories(model_category_id),
    PRIMARY KEY(item_model_id, model_category_id)
);