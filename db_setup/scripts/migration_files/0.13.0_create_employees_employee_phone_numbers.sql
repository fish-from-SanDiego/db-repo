CREATE TABLE IF NOT EXISTS employees_employee_phone_numbers(
    owner_employee_id INTEGER NOT NULL REFERENCES employees(employee_id),
    owner_phone_number_id INTEGER NOT NULL REFERENCES employee_phone_numbers(phone_number_id),
    PRIMARY KEY(owner_employee_id, owner_phone_number_id)
);