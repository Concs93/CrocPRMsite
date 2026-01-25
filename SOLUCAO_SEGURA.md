# 🔒 Solução Segura - Votação sem Expor Token

## ⚠️ Problema

GitHub bloqueia tokens no código público por segurança. Não podemos colocar o token no `luna-items.html`.

## ✅ Solução

**Sistema híbrido:**
1. **Pessoas votam** → Votos salvos em `localStorage` (navegador)
2. **Você processa** → Roda script local que faz commit no GitHub

## 📋 Como Funciona

### 1. Pessoas Votam (Site)

- Acessam: `https://concs93.github.io/CrocPRMsite/luna-items`
- Votam normalmente
- Votos ficam salvos no navegador delas (localStorage)

### 2. Você Coleta os Votos

**Opção A - Manual (Mais Simples):**
1. Pede para as pessoas exportarem seus votos
2. Ou você acessa o site e vota também (seus votos ficam no seu navegador)

**Opção B - Script Automático (Recomendado):**
1. Roda o script que exporta votos do localStorage
2. Script faz commit no GitHub usando seu token (local)

### 3. Processar e Fazer Commit

```bash
python commit_votes_to_github.py
```

Isso vai:
- Ler `luna_votes_data.json` local
- Fazer commit no GitHub
- Atualizar `luna_votes_summary.json`

## 🔧 Configuração

### 1. Token no Script Local

O token está em `commit_votes_to_github.py` (linha ~12):
```python
GITHUB_TOKEN = 'seu_token_aqui'
```

**Este arquivo NÃO vai para o GitHub!** (já está no .gitignore)

### 2. Coletar Votos

**Método 1 - Exportar do Navegador:**
1. Abra o site
2. Abra Console (F12)
3. Cole este código:
```javascript
// Exporta votos do localStorage
const votes = [];
for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    if (key.startsWith('luna_votes_')) {
        const itemName = key.replace('luna_votes_', '');
        const data = JSON.parse(localStorage.getItem(key));
        votes.push({
            timestamp: new Date().toISOString(),
            item_name: itemName,
            vote_type: data.userVote || 'positive',
            action: 'add'
        });
    }
}
console.log(JSON.stringify(votes, null, 2));
// Copie o resultado e cole em luna_votes_data.json
```

**Método 2 - Script Automático (Futuro):**
Posso criar um script que faz isso automaticamente.

## 📊 Gerar CSV/XLSX

Depois de fazer commit, gere os arquivos:

```bash
python generate_csv_from_github.py
```

## 🎯 Fluxo Completo

1. **Pessoas votam** no site → localStorage
2. **Você coleta** os votos (manual ou script)
3. **Salva** em `luna_votes_data.json` local
4. **Roda** `commit_votes_to_github.py`
5. **Votos** são commitados no GitHub
6. **Gera** CSV/XLSX quando quiser

## 🔒 Segurança

✅ Token fica apenas no seu computador  
✅ Não exposto no código público  
✅ GitHub não bloqueia  
✅ Você controla quando fazer commit  

---

## 💡 Alternativa Mais Automática (Futuro)

Se quiser algo mais automático, posso criar:
- GitHub Action que processa votos periodicamente
- Ou webhook que recebe votos

Mas a solução atual é a mais segura! 🔒
