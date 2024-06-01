CREATE TABLE IF NOT EXISTS contracts(
    contract_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    begin_date DATE NOT NULL CHECK (begin_date >= to_date('2020-01-01','YYYY-MM-DD') AND begin_date <= CURRENT_DATE),
    end_date DATE NOT NULL,
    actual_end_date DATE,
    supposed_total_sum DECIMAL(14,2) NOT NULL CHECK (supposed_total_sum > 0),
    contract_type type_of_contract NOT NULL,
    client_id INTEGER NOT NULL REFERENCES clients(client_id), 
    CONSTRAINT end_date_should_be_after_begin_date CHECK (begin_date <= end_date),
    CONSTRAINT actual_end_date_should_be_after_begin_date CHECK (actual_end_date IS NULL OR begin_date <= actual_end_date AND actual_end_date <= CURRENT_DATE)
);