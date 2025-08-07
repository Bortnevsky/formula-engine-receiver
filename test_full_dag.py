import requests
import json

def test_full_dag():
    """Тестирует построение полного графа зависимостей от Net Profit"""
    
    print("=== ТЕСТ ПОЛНОГО ГРАФА ЗАВИСИМОСТЕЙ ===\n")
    
    # 1. Загружаем Excel файл
    print("1. Загружаем Excel файл...")
    with open("data/test.xlsx", "rb") as f:
        response = requests.post(
            "http://localhost:8001/snapshot",
            files={"file": ("test.xlsx", f, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
        )
    
    # Собираем все ячейки
    cells = []
    for line in response.iter_lines():
        if line:
            cells.append(json.loads(line))
    
    print(f"✓ Загружено {len(cells)} ячеек\n")
    
    # Показываем структуру Excel файла
    print("2. Структура Excel файла:")
    sheets = {}
    for cell in cells:
        sheet = cell['sheet']
        if sheet not in sheets:
            sheets[sheet] = {'values': 0, 'formulas': 0}
        sheets[sheet]['values'] += 1
        if cell.get('formula'):
            sheets[sheet]['formulas'] += 1
    
    for sheet, stats in sheets.items():
        print(f"   Лист '{sheet}': {stats['values']} ячеек, {stats['formulas']} формул")
    
    # 3. Тестируем построение графа от Net Profit
    print("\n3. Строим граф зависимостей от Net Profit (Profit!B9)...")
    
    dag_request = {
        "seed_addr": "Profit!B9",  # Net Profit
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
        print(f"\n   Статистика:")
        print(f"   - Начальная ячейка: {result['seed']}")
        print(f"   - Узлов в графе: {result['stats']['total_nodes']}")
        print(f"   - Рёбер в графе: {result['stats']['total_edges']}")
        print(f"   - Глубина графа: {result['stats']['depth']}")
        
        # Показываем полный граф зависимостей
        print(f"\n   Полный граф зависимостей:")
        
        # Группируем зависимости по уровням
        edges = result['edges']
        levels = {}
        
        # Создаем обратный граф для определения уровней
        reverse_graph = {}
        for from_node, to_node in edges:
            if to_node not in reverse_graph:
                reverse_graph[to_node] = []
            reverse_graph[to_node].append(from_node)
        
        # BFS для определения уровней
        visited = set()
        queue = [(node, 0) for node in result['nodes'] if node not in reverse_graph]
        
        while queue:
            node, level = queue.pop(0)
            if node in visited:
                continue
            visited.add(node)
            
            if level not in levels:
                levels[level] = []
            levels[level].append(node)
            
            # Добавляем зависимые узлы
            for edge in edges:
                if edge[1] == node:
                    queue.append((edge[0], level + 1))
        
        # Выводим по уровням
        for level in sorted(levels.keys()):
            print(f"\n   Уровень {level}:")
            for node in levels[level]:
                # Находим формулу для узла
                cell_data = next((c for c in cells if c['addr'] == node), None)
                if cell_data and cell_data.get('formula'):
                    print(f"     {node}: {cell_data['formula']}")
                else:
                    print(f"     {node}: {cell_data['value'] if cell_data else 'N/A'}")
        
        # Показываем все связи
        print(f"\n   Все зависимости:")
        for from_node, to_node in edges:
            print(f"     {from_node} ← {to_node}")
            
    else:
        print(f"✗ Ошибка при построении графа: {response.text}")
    
    # 4. Тестируем построение графа от Total Revenue
    print("\n4. Строим граф зависимостей от Total Revenue (Revenue!D5)...")
    
    dag_request['seed_addr'] = "Revenue!D5"
    response = requests.post(
        "http://localhost:8003/build",
        json=dag_request
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✓ Граф построен!")
        print(f"   - Узлов: {result['stats']['total_nodes']}")
        print(f"   - Глубина: {result['stats']['depth']}")
    
    print("\n✅ Тестирование завершено!")

if __name__ == "__main__":
    test_full_dag()
