import os
import re
import sys
import statistics
import psycopg2
script_location=os.path.dirname(os.path.realpath(__file__))
queries_location = f"{script_location}/queries"
results_location = f"{script_location}/results"
# attempts_per_query = int(sys.argv[1])
# if attempts_per_query <= 0:
#     sys.exit(1)
password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
user = os.getenv('DB_USER')
attempts = int(os.getenv('ATTEMPTS_PER_QUERY'))
hostname=os.getenv('DB_HOSTNAME')
port=int(os.getenv('DB_PORT'))
connection = psycopg2.connect(
    dbname=db_name,
    user=user,
    password=password,
    host=hostname,
    port=port
)
connection.autocommit = False
with os.scandir(queries_location) as entries:
    for entry in entries:
        filename = entry.name
        print(f"{queries_location}/{filename}")
        with open(f"{queries_location}/{filename}", 'r') as file:
            sql = f"EXPLAIN ANALYZE {file.read()}"
        cost_results = list()
        time_results = list()
        for _ in range(attempts):
            with connection.cursor() as cursor:
                cursor.execute(sql)
                query_result = ''.join([entry[0] for entry in cursor.fetchall()])
                print(query_result)
                cost_pattern = r"cost=[\d\.]+\.\.([\d\.]+)"
                time_pattern = r"msExecution Time: ([\d\.]+)"
                cost_match = re.findall(cost_pattern, query_result)
                time_match = re.findall(time_pattern, query_result)
                if cost_match:
                    cost_results.append(sum([float(match) for match in cost_match]))
                    print(cost_results[-1])
                else:
                     sys.exit(1)
                if time_match:
                    time_results.append(float(time_match[-1]))
                    print(time_results[-1])
                else:
                     sys.exit(1)
        best_c = min(cost_results)
        worst_c = max(cost_results)
        average_c = statistics.mean(cost_results)
        best_t = min(time_results)
        worst_t = max(time_results)
        average_t = statistics.mean(time_results)
        results_dir =f"{results_location}/{filename}"
        os.makedirs(results_dir, exist_ok=True)
        entries = os.scandir(results_dir)
        present_file_nums=[int(entry.name) for entry in entries]
        if len(present_file_nums) == 0:
            number = 1
        else:
            number = max(present_file_nums) + 1
        with open(f"{results_dir}/{number}", 'w') as file:
            file.write(f"best_cost:{best_c}\nworst_cost:{worst_c}\navg_cost:{average_c}\nbest_time:{best_t}\nworst_time:{worst_t}\navg_time:{average_t}")
