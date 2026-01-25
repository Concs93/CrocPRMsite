# ⚡ Teste Rápido - 5 Minutos

## Passo a Passo para Testar AGORA

### 1. Abrir terminal na pasta do projeto

```bash
cd e:\PRM\CrocPRMsite
```

### 2. Instalar dependências (só na primeira vez)

```bash
pip install flask flask-cors openpyxl
```

Ou:
```bash
pip install -r requirements_votes.txt
```

### 3. Rodar o servidor

```bash
python server_votes.py
```

Você deve ver:
```
🚀 Iniciando servidor de votos...
📁 Arquivos de dados:
   - CSV: luna_votes.csv
   - XLSX: luna_votes.xlsx
   - JSON: luna_votes_summary.json

🌐 Servidor rodando em: http://0.0.0.0:5000
```

### 4. Abrir a página

**Opção A - Abrir direto:**
- Abra `luna-items.html` no navegador
- O status deve mudar para "Servidor conectado" (verde)

**Opção B - Servidor local (melhor):**
- Em outro terminal:
```bash
cd e:\PRM\CrocPRMsite
python -m http.server 8000
```
- Acesse: `http://localhost:8000/luna-items.html`

### 5. Testar votação

1. Clique em um botão de voto (✓, ○, ou ✗)
2. O contador deve atualizar
3. Verifique se apareceu "Servidor conectado" (verde)

### 6. Verificar arquivos gerados

Na pasta `e:\PRM\CrocPRMsite`, você deve ver:
- ✅ `luna_votes.csv` - Histórico de votos
- ✅ `luna_votes.xlsx` - Planilha Excel
- ✅ `luna_votes_summary.json` - Resumo

### 7. Parar o servidor

No terminal onde está rodando, pressione: `Ctrl+C`

---

## ✅ Se funcionou:

- Status verde apareceu
- Contadores atualizaram
- Arquivos foram criados

**Próximo passo:** Fazer deploy em produção (ver `GUIA_DEPLOY.md`)

---

## ❌ Se não funcionou:

### Erro: "python não é reconhecido"
- Instale Python: https://www.python.org/downloads/
- Marque "Add Python to PATH" na instalação

### Erro: "ModuleNotFoundError: No module named 'flask'"
- Execute: `pip install flask flask-cors openpyxl`

### Status continua vermelho/laranja
- Verifique se o servidor está rodando
- Verifique se a porta 5000 está livre
- Tente abrir: `http://localhost:5000/api/health` no navegador
- Deve retornar: `{"status":"ok","has_xlsx":true}`

### CORS Error no navegador
- Verifique se `flask-cors` está instalado
- Reinicie o servidor

---

## 🎯 Pronto para Produção?

Depois de testar localmente, veja `GUIA_DEPLOY.md` para fazer deploy no Render.com (gratuito).
