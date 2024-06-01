CREATE TABLE IF NOT EXISTS employees_contracts(
    employee_id INTEGER REFERENCES employees(employee_id),
    contract_id INTEGER REFERENCES contracts(contract_id),
    PRIMARY KEY(employee_id, contract_id)
);