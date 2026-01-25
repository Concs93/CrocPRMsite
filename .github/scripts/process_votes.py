#!/usr/bin/env python3
"""
Processa votos do arquivo JSON e gera CSV/XLSX
Roda via GitHub Actions
"""

import json
import csv
import os
from datetime import datetime
from collections import defaultdict

try:
    from openpyxl import Workbook, load_workbook
    HAS_XLSX = True
except ImportError:
    HAS_XLSX = False

# Arquivos
VOTES_QUEUE = 'luna_votes_queue.json'
CSV_FILE = 'luna_votes.csv'
XLSX_FILE = 'luna_votes.xlsx'
SUMMARY_FILE = 'luna_votes_summary.json'

def load_queue():
    """Carrega fila de votos"""
    if os.path.exists(VOTES_QUEUE):
        with open(VOTES_QUEUE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def load_existing_votes():
    """Carrega votos existentes do CSV"""
    votes = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            votes = list(reader)
    return votes

def load_summary():
    """Carrega resumo existente"""
    if os.path.exists(SUMMARY_FILE):
        with open(SUMMARY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def process_votes():
    """Processa votos da fila"""
    queue = load_queue()
    if not queue:
        print("Nenhum voto na fila")
        return
    
    # Carrega votos existentes
    existing_votes = load_existing_votes()
    summary = load_summary()
    
    # Processa cada voto da fila
    for vote_data in queue:
        timestamp = vote_data.get('timestamp', datetime.now().isoformat())
        item_name = vote_data.get('item_name')
        vote_type = vote_data.get('vote_type')
        action = vote_data.get('action')
        
        if not all([item_name, vote_type, action]):
            continue
        
        # Adiciona ao CSV
        existing_votes.append({
            'timestamp': timestamp,
            'item_name': item_name,
            'vote_type': vote_type,
            'action': action
        })
        
        # Atualiza resumo
        if item_name not in summary:
            summary[item_name] = {'positive': 0, 'neutral': 0, 'negative': 0}
        
        if action == 'add':
            summary[item_name][vote_type] = summary[item_name].get(vote_type, 0) + 1
        elif action == 'remove':
            summary[item_name][vote_type] = max(0, summary[item_name].get(vote_type, 0) - 1)
    
    # Salva CSV
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['timestamp', 'item_name', 'vote_type', 'action']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing_votes)
    
    # Salva XLSX
    if HAS_XLSX:
        wb = Workbook()
        ws = wb.active
        ws.title = "Votos"
        ws.append(['Timestamp', 'Item', 'Tipo de Voto', 'Ação'])
        for vote in existing_votes:
            ws.append([vote['timestamp'], vote['item_name'], vote['vote_type'], vote['action']])
        wb.save(XLSX_FILE)
    
    # Salva resumo
    with open(SUMMARY_FILE, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    # Limpa fila
    with open(VOTES_QUEUE, 'w', encoding='utf-8') as f:
        json.dump([], f)
    
    print(f"Processados {len(queue)} votos")

if __name__ == '__main__':
    process_votes()
