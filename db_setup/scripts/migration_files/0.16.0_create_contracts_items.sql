CREATE TABLE IF NOT EXISTS contracts_items(
    contract_id INTEGER REFERENCES contracts(contract_id),
    item_id INTEGER REFERENCES items(item_id),
    PRIMARY KEY(contract_id, item_id)
);