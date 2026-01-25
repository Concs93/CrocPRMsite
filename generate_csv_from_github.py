#!/usr/bin/env python3
"""
Gera CSV e XLSX a partir do arquivo luna_votes_data.json do GitHub
"""

import json
import csv
import os
from collections import defaultdict

try:
    from openpyxl import Workbook
    HAS_XLSX = True
except ImportError:
    HAS_XLSX = False
    print("⚠️  openpyxl não instalado. Instale com: pip install openpyxl")
    print("   Por enquanto, apenas CSV será gerado.")

# Configuração
GITHUB_REPO = 'concs93/CrocPRMsite'
GITHUB_BRANCH = 'main'
VOTES_FILE = 'luna_votes_data.json'
CSV_FILE = 'luna_votes.csv'
XLSX_FILE = 'luna_votes.xlsx'
SUMMARY_FILE = 'luna_votes_summary.json'

def download_from_github():
    """Baixa arquivo do GitHub"""
    import urllib.request
    
    url = f'https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}/{VOTES_FILE}'
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data
    except Exception as e:
        print(f"❌ Erro ao baixar do GitHub: {e}")
        # Tenta arquivo local
        if os.path.exists(VOTES_FILE):
            print(f"📁 Usando arquivo local: {VOTES_FILE}")
            with open(VOTES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

def generate_csv(votes):
    """Gera arquivo CSV"""
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'item_name', 'vote_type', 'action'])
        for vote in votes:
            writer.writerow([
                vote.get('timestamp', ''),
                vote.get('item_name', ''),
                vote.get('vote_type', ''),
                vote.get('action', '')
            ])
    print(f"✅ CSV gerado: {CSV_FILE}")

def generate_xlsx(votes):
    """Gera arquivo XLSX"""
    if not HAS_XLSX:
        return
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Votos"
    
    # Cabeçalho
    ws.append(['Timestamp', 'Item', 'Tipo de Voto', 'Ação'])
    
    # Dados
    for vote in votes:
        ws.append([
            vote.get('timestamp', ''),
            vote.get('item_name', ''),
            vote.get('vote_type', ''),
            vote.get('action', '')
        ])
    
    wb.save(XLSX_FILE)
    print(f"✅ XLSX gerado: {XLSX_FILE}")

def generate_summary(votes):
    """Gera resumo de votos"""
    summary = defaultdict(lambda: {'positive': 0, 'neutral': 0, 'negative': 0})
    
    for vote in votes:
        item = vote.get('item_name')
        vote_type = vote.get('vote_type')
        action = vote.get('action')
        
        if not item or not vote_type or not action:
            continue
        
        if action == 'add':
            summary[item][vote_type] += 1
        elif action == 'remove':
            summary[item][vote_type] = max(0, summary[item][vote_type] - 1)
    
    # Converte para dict normal
    summary_dict = dict(summary)
    
    with open(SUMMARY_FILE, 'w', encoding='utf-8') as f:
        json.dump(summary_dict, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Resumo gerado: {SUMMARY_FILE}")
    
    # Mostra estatísticas
    total_items = len(summary_dict)
    total_votes = sum(sum(v.values()) for v in summary_dict.values())
    print(f"\n📊 Estatísticas:")
    print(f"   - Itens votados: {total_items}")
    print(f"   - Total de votos: {total_votes}")

def main():
    print("🚀 Gerando CSV/XLSX dos votos...")
    print(f"📥 Baixando {VOTES_FILE} do GitHub...")
    
    votes = download_from_github()
    
    if not votes:
        print("❌ Nenhum voto encontrado!")
        return
    
    print(f"✅ {len(votes)} votos encontrados")
    
    generate_csv(votes)
    if HAS_XLSX:
        generate_xlsx(votes)
    generate_summary(votes)
    
    print("\n✅ Concluído!")

if __name__ == '__main__':
    main()
