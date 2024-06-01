CREATE TABLE IF NOT EXISTS employees(
    employee_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    employee_full_name VARCHAR(60) NOT NULL,
    employee_occupation_id INTEGER NOT NULL REFERENCES employee_occupations(occupation_id),
    salary DECIMAL(14,2) NOT NULL CHECK (salary >= 0)
);
