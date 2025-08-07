import requests

# Ждем запуска сервиса
import time
time.sleep(3)

# Тестируем health endpoint
try:
    response = requests.get("http://localhost:8001/health")
    print("Health check:", response.json())
except Exception as e:
    print("Ошибка подключения к health:", e)

# Тестируем загрузку файла
try:
    with open("data/test.xlsx", "rb") as f:
        files = {"file": ("test.xlsx", f, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
        response = requests.post("http://localhost:8001/snapshot", files=files)
        
    print("\nОтвет сервера:")
    print("-" * 50)
    
    # Разбираем NDJSON ответ
    for line in response.text.strip().split('\n'):
        if line:
            print(line)
    
    print("-" * 50)
    print(f"Статус: {response.status_code}")
    print(f"Всего строк: {len(response.text.strip().split('\n'))}")
    
except Exception as e:
    print("Ошибка при загрузке файла:", e)