from fastapi import FastAPI
import re

app = FastAPI(title="Static Refs", version="0.1.0")

@app.get("/health")
def health():
    return {"status": "healthy", "service": "static_refs"}

@app.post("/extract")
def extract(formula: str):
    """
    Извлекает ссылки на ячейки из формулы Excel.
    Поддерживает форматы: A1, Sheet1!A1, 'Sheet Name'!A1
    """
    refs = []
    
    # Паттерн для ссылок с именем листа
    # Поддерживает: Sheet1!A1, 'Sheet Name'!A1
    sheet_refs = re.findall(r"(?:'([^']+)'|([A-Za-z_]\w*))!([A-Z]+[0-9]+(?::[A-Z]+[0-9]+)?)", formula)
    for match in sheet_refs:
        sheet = match[0] if match[0] else match[1]
        cell_ref = match[2]
        if ':' in cell_ref:
            # Обрабатываем диапазоны (например, A1:A3)
            start, end = cell_ref.split(':')
            refs.append(f"{sheet}!{start}")
            refs.append(f"{sheet}!{end}")
        else:
            refs.append(f"{sheet}!{cell_ref}")
    
    # Паттерн для простых ссылок без имени листа (A1, B2 и т.д.)
    # Исключаем ссылки, которые уже найдены с именем листа
    simple_refs = re.findall(r'(?<![!:])\b([A-Z]+[0-9]+)\b(?!:)', formula)
    
    # Добавляем простые ссылки, если они не были найдены как часть ссылки с листом
    formula_without_sheet_refs = formula
    for ref in sheet_refs:
        formula_without_sheet_refs = formula_without_sheet_refs.replace(f"{ref[0] if ref[0] else ref[1]}!{ref[2]}", '')
    
    for ref in simple_refs:
        if ref in formula_without_sheet_refs:
            refs.append(ref)
    
    # Убираем дубликаты, сохраняя порядок
    seen = set()
    unique_refs = []
    for ref in refs:
        if ref not in seen:
            seen.add(ref)
            unique_refs.append(ref)
    
    return {"formula": formula, "refs": unique_refs}