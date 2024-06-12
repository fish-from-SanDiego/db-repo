WITH cte AS (SELECT * FROM employees e JOIN employees_employee_phone_numbers ep ON e.employee_id = ep.owner_employee_id JOIN employee_phone_numbers p ON ep.owner_phone_number_id = p.phone_number_id)
SELECT DISTINCT * FROM cte WHERE cte.phone_number ~ '^\+7999.*$' AND cte.employee_full_name ~ '^.{5,12}$';