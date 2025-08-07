from fastapi import FastAPI
from typing import List, Dict, Any
import networkx as nx

app = FastAPI(title="DAG Builder", version="0.1.0")

@app.get("/health")
def health():
    return {"status": "healthy", "service": "dag_builder"}

@app.post("/build_dag")
def build_dag(cells: List[Dict[str, Any]]):
    G = nx.DiGraph()
    
    # Добавляем узлы и связи
    for cell in cells:
        if 'addr' in cell:
            G.add_node(cell['addr'], value=cell.get('value'))
            
            # Если есть формула с ссылками
            if 'refs' in cell and cell['refs']:
                for ref in cell['refs']:
                    G.add_edge(ref, cell['addr'])
    
    return {
        "total_cells": len(cells),
        "nodes": list(G.nodes()),
        "edges": list(G.edges()),
        "status": "graph_with_edges"
    }