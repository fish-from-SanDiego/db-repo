CREATE TABLE IF NOT EXISTS employee_phone_numbers(
    phone_number_id INTEGER NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    phone_number VARCHAR(15) NOT NULL CHECK (phone_number ~ '^\+7\d{10}$')
);