#!/usr/bin/env python3
"""
Junta vários arquivos JSON de votos em um único arquivo
"""

import json
import sys
import os
from collections import defaultdict

OUTPUT_FILE = 'luna_votes_data.json'

def load_json_file(filepath):
    """Carrega arquivo JSON"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Erro ao carregar {filepath}: {e}")
        return []

def merge_votes(files):
    """Junta votos de vários arquivos"""
    all_votes = []
    seen_votes = set()  # Para evitar duplicatas
    
    for filepath in files:
        if not os.path.exists(filepath):
            print(f"⚠️  Arquivo não encontrado: {filepath}")
            continue
        
        print(f"📂 Processando: {filepath}")
        votes = load_json_file(filepath)
        
        for vote in votes:
            # Cria chave única para evitar duplicatas
            vote_key = (
                vote.get('item_name'),
                vote.get('vote_type'),
                vote.get('timestamp', '')[:19]  # Apenas data/hora (sem milissegundos)
            )
            
            if vote_key not in seen_votes:
                all_votes.append(vote)
                seen_votes.add(vote_key)
    
    return all_votes

def generate_summary(votes):
    """Gera resumo dos votos"""
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
    
    return dict(summary)

def main():
    if len(sys.argv) < 2:
        print("📋 Uso: python merge_votes.py arquivo1.json arquivo2.json ...")
        print("\nExemplo:")
        print("  python merge_votes.py joao_votes.json maria_votes.json pedro_votes.json")
        print("\nOu use * para juntar todos:")
        print("  python merge_votes.py *.json")
        return
    
    files = sys.argv[1:]
    
    print("🚀 Juntando votos...")
    print(f"📁 {len(files)} arquivo(s) para processar\n")
    
    all_votes = merge_votes(files)
    
    if not all_votes:
        print("❌ Nenhum voto encontrado!")
        return
    
    # Ordena por timestamp
    all_votes.sort(key=lambda x: x.get('timestamp', ''))
    
    # Salva arquivo unificado
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_votes, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ {len(all_votes)} votos juntados!")
    print(f"📄 Salvo em: {OUTPUT_FILE}")
    
    # Gera resumo
    summary = generate_summary(all_votes)
    print(f"\n📊 Resumo:")
    print(f"   - Itens votados: {len(summary)}")
    total_votes = sum(sum(v.values()) for v in summary.values())
    print(f"   - Total de votos: {total_votes}")
    
    # Mostra top 5 itens mais votados
    items_by_votes = sorted(summary.items(), key=lambda x: sum(x[1].values()), reverse=True)
    if items_by_votes:
        print(f"\n🏆 Top 5 itens mais votados:")
        for i, (item, votes) in enumerate(items_by_votes[:5], 1):
            total = sum(votes.values())
            print(f"   {i}. {item}: {total} votos (✓{votes['positive']} ○{votes['neutral']} ✗{votes['negative']})")
    
    print(f"\n💡 Próximo passo: python commit_votes_to_github.py")

if __name__ == '__main__':
    main()
