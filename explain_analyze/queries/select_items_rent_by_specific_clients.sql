SELECT DISTINCT it.item_id FROM items it JOIN contracts_items cit ON it.item_id = cit.item_id JOIN contracts c ON cit.contract_id = c.contract_id WHERE c.client_id IN (SELECT client_id FROM clients WHERE client_name ~ '^\d{2}.{5,50}$')