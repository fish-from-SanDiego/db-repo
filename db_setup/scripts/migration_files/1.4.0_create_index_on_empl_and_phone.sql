CREATE INDEX IF NOT EXISTS emp_index ON employees USING GIN(employee_full_name);
CREATE INDEX IF NOT EXISTS ph_index ON employee_phone_numbers USING GIN(phone_number);