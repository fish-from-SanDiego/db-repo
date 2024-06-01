CREATE TABLE IF NOT EXISTS account_transactions(
    transaction_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    transaction_time TIMESTAMP(0) NOT NULL,
    transaction_sum DECIMAL(14,2) NOT NULL CHECK (transaction_sum > 0),
    company_account_id INTEGER NOT NULL REFERENCES company_accounts(company_account_id),
    client_account_id INTEGER NOT NULL REFERENCES client_accounts(account_id),
    transaction_contract_id INTEGER NOT NULL REFERENCES contracts(contract_id),
    is_income BOOLEAN NOT NULL
);
