import requests
import json

def test_dag_builder():
    """Тестирует работу всех трёх сервисов вместе"""
    
    print("1. Проверяем health всех сервисов...")
    services = [
        ("excel-reader", "http://localhost:8001/health"),
        ("static-refs", "http://localhost:8002/health"),
        ("dag-builder", "http://localhost:8003/health")
    ]
    
    for name, url in services:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"✓ {name} работает: {response.json()}")
            else:
                print(f"✗ {name} не отвечает")
        except Exception as e:
            print(f"✗ {name} недоступен: {e}")
    
    print("\n2. Загружаем Excel файл...")
    try:
        with open("data/test.xlsx", "rb") as f:
            response = requests.post(
                "http://localhost:8001/snapshot",
                files={"file": ("test.xlsx", f, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
            )
        
        # Собираем все ячейки из потокового ответа
        cells = []
        for line in response.iter_lines():
            if line:
                cells.append(json.loads(line))
        
        print(f"✓ Загружено {len(cells)} ячеек")
        
        # Показываем первые несколько ячеек с формулами
        formulas_found = [c for c in cells if c.get("formula")]
        print(f"✓ Найдено {len(formulas_found)} формул")
        
        if formulas_found:
            print("\nПримеры формул:")
            for cell in formulas_found[:3]:
                print(f"  {cell['addr']}: {cell['formula']}")
    
    except Exception as e:
        print(f"✗ Ошибка при загрузке Excel: {e}")
        return
    
    print("\n3. Тестируем парсинг формул...")
    if formulas_found:
        test_formula = formulas_found[0]["formula"]
        response = requests.post(
            "http://localhost:8002/extract",
            params={"formula": test_formula}
        )
        print(f"✓ Формула: {test_formula}")
        print(f"✓ Найденные ссылки: {response.json()['refs']}")
    
    print("\n4. Строим граф зависимостей...")
    # Выбираем seed - первую ячейку с формулой
    if formulas_found:
        seed_addr = formulas_found[0]["addr"]
        
        # Подготавливаем данные для DAG builder
        dag_request = {
            "seed_addr": seed_addr,
            "cells": [
                {
                    "addr": c["addr"],
                    "value": c["value"],
                    "formula": c.get("formula")
                }
                for c in cells
            ]
        }
        
        response = requests.post(
            "http://localhost:8003/build",
            json=dag_request
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Граф построен успешно!")
            print(f"  - Начальная ячейка: {result['seed']}")
            print(f"  - Узлов: {result['stats']['total_nodes']}")
            print(f"  - Рёбер: {result['stats']['total_edges']}")
            print(f"  - Глубина: {result['stats']['depth']}")
            
            if result['edges']:
                print("\n  Примеры зависимостей:")
                for edge in result['edges'][:5]:
                    print(f"    {edge[0]} → {edge[1]}")
        else:
            print(f"✗ Ошибка при построении графа: {response.text}")
    
    print("\n✅ Тестирование завершено!")

if __name__ == "__main__":
    test_dag_builder()
