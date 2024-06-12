SELECT at.transaction_sum FROM account_transactions at WHERE at.transaction_time >= timestamp '2022-07-15 00:00:00' AND at.is_income IS true AND at.client_account_id <= 100000;
