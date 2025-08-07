"""
Демонстрация работы Formula Engine - первые 3 микросервиса
"""
import requests
import json
from pprint import pprint

def print_separator():
    print("=" * 60)

def demo_formula_engine():
    print_separator()
    print("FORMULA ENGINE - ДЕМОНСТРАЦИЯ")
    print("Микросервисы: excel-reader, static-refs, dag-builder")
    print_separator()
    
    # Проверка здоровья сервисов
    print("\n1. ПРОВЕРКА МИКРОСЕРВИСОВ:")
    services = [
        ("excel-reader", "http://localhost:8001/health", "Чтение Excel файлов"),
        ("static-refs", "http://localhost:8002/health", "Парсинг формул"),
        ("dag-builder", "http://localhost:8003/health", "Построение графа зависимостей")
    ]
    
    all_healthy = True
    for name, url, description in services:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"   ✓ {name}: OK - {description}")
            else:
                print(f"   ✗ {name}: FAIL")
                all_healthy = False
        except Exception as e:
            print(f"   ✗ {name}: НЕДОСТУПЕН - {e}")
            all_healthy = False
    
    if not all_healthy:
        print("\n❌ Не все сервисы доступны. Запустите: docker-compose up -d")
        return
    
    # Загрузка Excel
    print("\n2. ЗАГРУЗКА EXCEL ФАЙЛА (data/test.xlsx):")
    try:
        with open("data/test.xlsx", "rb") as f:
            response = requests.post(
                "http://localhost:8001/snapshot",
                files={"file": ("test.xlsx", f, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
            )
        
        cells = []
        for line in response.iter_lines():
            if line:
                cells.append(json.loads(line))
        
        print(f"   ✓ Загружено {len(cells)} ячеек")
        
        # Показываем примеры формул
        formulas = [c for c in cells if c.get("formula")]
        print(f"   ✓ Найдено {len(formulas)} формул")
        
        print("\n   Примеры формул:")
        for f in formulas[:5]:
            print(f"   • {f['addr']}: {f['formula']} = {f['value']}")
    
    except Exception as e:
        print(f"   ✗ Ошибка: {e}")
        return
    
    # Парсинг формул
    print("\n3. ПАРСИНГ ФОРМУЛ (static-refs):")
    test_formulas = [
        "=B2*C2",
        "=SUM(D2:D3)",
        "=Revenue!D5",
        "=B5-B7"
    ]
    
    for formula in test_formulas:
        response = requests.post(
            "http://localhost:8002/extract",
            params={"formula": formula}
        )
        result = response.json()
        print(f"   {formula} → {result['refs']}")
    
    # Построение графа зависимостей
    print("\n4. ПОСТРОЕНИЕ ГРАФА ЗАВИСИМОСТЕЙ:")
    
    # Net Profit - самая важная ячейка
    seed = "Profit!B9"
    print(f"   Начальная ячейка: {seed} (Net Profit)")
    
    dag_request = {
        "seed_addr": seed,
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
        
        print(f"\n   РЕЗУЛЬТАТ:")
        print(f"   • Узлов в графе: {result['stats']['total_nodes']}")
        print(f"   • Связей: {result['stats']['total_edges']}")
        print(f"   • Глубина: {result['stats']['depth']}")
        
        print(f"\n   ГРАФ ЗАВИСИМОСТЕЙ:")
        print(f"   {seed} (Net Profit)")
        
        # Визуализация дерева зависимостей
        edges = result['edges']
        tree = {}
        
        # Строим дерево
        for from_node, to_node in edges:
            if from_node not in tree:
                tree[from_node] = []
            tree[from_node].append(to_node)
        
        # Рекурсивный вывод дерева
        def print_tree(node, level=1, printed=None):
            if printed is None:
                printed = set()
            
            if node in printed:
                return
            printed.add(node)
            
            if node in tree:
                for child in tree[node]:
                    # Находим данные ячейки
                    cell_data = next((c for c in cells if c['addr'] == child), None)
                    if cell_data:
                        value = f" = {cell_data['value']}" if cell_data['value'] is not None else ""
                        formula = f" ({cell_data['formula']})" if cell_data.get('formula') else ""
                        print(f"   {'  ' * level}└─ {child}{formula}{value}")
                    else:
                        print(f"   {'  ' * level}└─ {child}")
                    print_tree(child, level + 1, printed)
        
        print_tree(seed)
        
    else:
        print(f"   ✗ Ошибка: {response.text}")
    
    print_separator()
    print("\n✅ FORMULA ENGINE ГОТОВ К РАБОТЕ!")
    print("   Следующие шаги:")
    print("   • dynamic-trace (8004) - трассировка динамических формул")
    print("   • excel-verify (8005) - проверка вычислений") 
    print("   • unit-normalizer (8006) - нормализация единиц измерения")
    print("   • semantic-tagger (8007) - семантическая разметка")
    print("   • scenario-runner (8008) - запуск сценариев")
    print("   • audit-reporter (8009) - генерация отчетов")
    print("   • api-gateway (8010) - единая точка входа")
    print_separator()

if __name__ == "__main__":
    demo_formula_engine()
