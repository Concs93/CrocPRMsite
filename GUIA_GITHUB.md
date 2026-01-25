# 🚀 Guia Simples - Votação com GitHub

## Como Funciona

1. **Pessoas votam** no site `https://concs93.github.io/CrocPRMsite/luna-items`
2. **Votos são salvos** em `luna_votes_data.json` no repositório GitHub
3. **Resumo é atualizado** em `luna_votes_summary.json`
4. **Você pode gerar CSV/XLSX** rodando um script Python localmente

## ⚙️ Configuração Inicial

### 1. Criar Personal Access Token no GitHub

1. Vá em: https://github.com/settings/tokens
2. Clique em **"Generate new token"** → **"Generate new token (classic)"**
3. Dê um nome: `Luna Items Votes`
4. Marque a permissão: **`repo`** (acesso completo ao repositório)
5. Clique em **"Generate token"**
6. **COPIE O TOKEN** (você só vê ele uma vez!)

### 2. Configurar Token no Código

1. Abra `luna-items.html`
2. Procure a linha (por volta da linha 340):
   ```javascript
   const GITHUB_TOKEN = null;
   ```
3. Cole seu token:
   ```javascript
   const GITHUB_TOKEN = 'seu_token_aqui';
   ```
4. **⚠️ IMPORTANTE:** Não commite o token no GitHub!
   - Adicione no `.gitignore`:
   ```
   # Tokens
   *token*
   *TOKEN*
   ```

### 3. Fazer Commit e Push

```bash
git add luna-items.html
git commit -m "Add voting system with GitHub integration"
git push
```

## 📊 Gerar CSV/XLSX dos Votos

### Opção 1: Script Python Automático

1. **Instalar dependências:**
   ```bash
   pip install openpyxl
   ```

2. **Rodar o script:**
   ```bash
   python generate_csv_from_github.py
   ```

   Isso vai:
   - Baixar `luna_votes_data.json` do GitHub
   - Gerar `luna_votes.csv` e `luna_votes.xlsx`
   - Criar `luna_votes_summary.json` atualizado

### Opção 2: Manual

1. Baixe `luna_votes_data.json` do repositório
2. Abra no Excel/Google Sheets
3. Exporte como CSV/XLSX

## 🔒 Segurança do Token

**⚠️ NUNCA compartilhe seu token!**

Se o token vazar:
1. Vá em: https://github.com/settings/tokens
2. Revogue o token antigo
3. Crie um novo
4. Atualize no código

## 📁 Arquivos Gerados

- **`luna_votes_data.json`** - Histórico completo de todos os votos
- **`luna_votes_summary.json`** - Resumo com contadores (usado pelo site)
- **`luna_votes.csv`** - Gerado pelo script Python
- **`luna_votes.xlsx`** - Gerado pelo script Python

## 🎯 Como Usar

1. **Pessoas acessam:** `https://concs93.github.io/CrocPRMsite/luna-items`
2. **Pessoas votam:** Clicam em ✓, ○, ou ✗
3. **Votos são salvos:** Automaticamente no GitHub
4. **Você vê os votos:** 
   - No arquivo `luna_votes_data.json` no repositório
   - Ou gera CSV/XLSX rodando o script

## ❓ Problemas Comuns

### Token não funciona
- Verifique se tem permissão `repo`
- Verifique se o token não expirou
- Tente criar um novo token

### Votos não aparecem
- Verifique se o arquivo `luna_votes_summary.json` está sendo atualizado
- Verifique o console do navegador (F12) para erros
- Verifique se o token está correto

### CORS Error
- GitHub API permite CORS, mas verifique se o token está correto
- Se usar token, deve funcionar normalmente

---

## ✅ Pronto!

Agora o sistema salva votos diretamente no seu repositório GitHub! 🎉
