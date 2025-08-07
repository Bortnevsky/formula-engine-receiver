# Formula Engine Receiver

## Статус проекта

### ✅ Готовые сервисы (3/10)

1. **Excel Reader** - Чтение Excel файлов
   - Порт: 8001
   - Endpoint: `/snapshot`
   - Статус: ✅ Работает

2. **Static Refs** - Извлечение ссылок из формул
   - Порт: 8002
   - Endpoint: `/extract`
   - Статус: ✅ Работает

3. **DAG Builder** - Построение графа зависимостей
   - Порт: 8003
   - Endpoint: `/build_dag`
   - Статус: ✅ Работает с edges!

### ⏳ Оставшиеся сервисы (7/10)

4. **Formula Parser** - Парсинг формул
5. **Calculator** - Вычисление формул
6. **Orchestrator** - Управление процессом
7. **Cache Manager** - Кэширование результатов
8. **Error Handler** - Обработка ошибок
9. **API Gateway** - Единая точка входа
10. **Result Aggregator** - Сборка результатов

## Тестирование

```bash
# Запуск сервисов
docker-compose up -d --build

# Интеграционный тест
python test_integration.py
```

## Результат теста

```
DAG: {
  'total_cells': 3, 
  'nodes': ['A1', 'A2', 'A3'], 
  'edges': [['A1', 'A3'], ['A2', 'A3']], 
  'status': 'graph_with_edges'
}
```

Граф успешно строит зависимости между ячейками!
