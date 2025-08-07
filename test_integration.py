import requests

# 1. Загружаем Excel
with open('data/test.xlsx', 'rb') as f:
    files = {'file': ('test.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
    excel_data = requests.post('http://localhost:8001/snapshot', files=files)

# 2. Извлекаем ссылки из формулы
refs = requests.post('http://localhost:8002/extract', params={'formula': '=B1-B2'})

# 3. Строим граф с тестовыми данными
# Сначала извлекаем ссылки для A3
refs_a3 = requests.post('http://localhost:8002/extract', params={'formula': '=A1+A2'})
refs_a3_data = refs_a3.json()

dag_data = [
    {"addr": "A1", "value": 100},
    {"addr": "A2", "value": 200},
    {"addr": "A3", "formula": "=A1+A2", "refs": refs_a3_data.get('refs', [])}
]
print("Sending to DAG:", dag_data)
dag = requests.post('http://localhost:8003/build_dag', json=dag_data)

print("\nExcel:", excel_data.status_code)
print("Refs test B1-B2:", refs.json())
print("Refs for A3:", refs_a3_data)
print("DAG response:", dag.status_code)
print("DAG:", dag.json())
