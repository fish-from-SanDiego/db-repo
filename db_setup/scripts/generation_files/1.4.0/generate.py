import psycopg2
import os
import random
from faker import Faker
from fill_model_categories import fill_model_categories
from fill_models import fill_models
from fill_items import fill_items
from fill_clients import fill_clients
from fill_company_accounts import fill_company_accounts
from fill_employee_occupations import fill_employee_occupations
from fill_employees import fill_employees
from fill_employee_phone_numbers import fill_employee_phone_numbers
from fill_contracts import fill_contracts

db_creator_password = os.getenv('DB_CREATOR_PASSWORD')
main_db_name = os.getenv('MAIN_DB_NAME')
db_creator_name = os.getenv('DB_CREATOR_NAME')
max_migration_version = os.getenv('MAX_MIGRATION_VERSION')
hostname=os.getenv('DB_HOSTNAME')
port=int(os.getenv('HAPROXY_PRIMARY_PORT'))
script_location=os.path.dirname(os.path.realpath(__file__))
files_location = f"{script_location}/migration_files"
connection = psycopg2.connect(
dbname=main_db_name,
    user=db_creator_name,
    password=db_creator_password,
    host=hostname,
    port=port
)
connection.autocommit = False

try:
    fill_model_categories(connection, int(os.getenv('CATEGORIES_COUNT')))
    print('fill categories done')
    fill_models(connection, int(os.getenv('MODELS_COUNT')), int(os.getenv('MIN_CATEGORIES_PER_MODEL')), int(os.getenv('MAX_CATEGORIES_PER_MODEL')))
    print('fill models (and models_model_categories) done')
    fill_items(connection, int(os.getenv('ITEMS_COUNT')))
    print('fill items done')
    fill_clients(connection, int(os.getenv('CLIENTS_COUNT')), int(os.getenv('MIN_ACCOUNTS_PER_CLIENT')), int(os.getenv('MAX_ACCOUNTS_PER_CLIENT')))
    print('fill clients (and client accounts) done')
    fill_company_accounts(connection, int(os.getenv('COMPANY_ACCOUNTS_COUNT')))
    print('fill company_accounts done')
    fill_employee_occupations(connection, int(os.getenv('EMPLOYEE_OCCUPATIONS_COUNT')))
    print('fill employee_occupations done')
    fill_employees(connection, int(os.getenv('EMPLOYEES_COUNT')))
    print('fill employees done')
    fill_employee_phone_numbers(connection, int(os.getenv('PHONE_NUMBERS_COUNT')), int(os.getenv('MIN_PHONE_NUMBER_OWNERS')), int(os.getenv('MAX_PHONE_NUMBER_OWNERS')))
    print('fill employee_phone_numbers (and employees_employee_phone_numbers) done')
    fill_contracts(connection, int(os.getenv('CONTRACTS_COUNT')), int(os.getenv('MIN_TRANSACTIONS_PER_CONTRACT')), int(os.getenv('MAX_TRANSACTIONS_PER_CONTRACT')), int(os.getenv('MIN_ITEMS_PER_CONTRACT')), int(os.getenv('MAX_ITEMS_PER_CONTRACT')), int(os.getenv('MIN_EMPLOYEES_PER_CONTRACT')), int(os.getenv('MAX_EMPLOYEES_PER_CONTRACT')))
    print('fill contracts (and all referencing tables) done')
finally:
    connection.close()