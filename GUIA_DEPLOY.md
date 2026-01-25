# 🚀 Guia de Deploy - Sistema de Votação

## ⚠️ Importante: GitHub Pages é Estático

GitHub Pages **NÃO roda servidores Python**. Você precisa hospedar o backend separadamente.

## 📋 Opções de Deploy

### Opção 1: Testar Localmente (Rápido para testar)

**Passo a passo:**

1. **Instalar Python e dependências:**
   ```bash
   pip install -r requirements_votes.txt
   ```

2. **Rodar o servidor:**
   ```bash
   python server_votes.py
   ```

3. **Abrir a página localmente:**
   - Abra `luna-items.html` no navegador
   - Ou use um servidor local: `python -m http.server 8000`
   - Acesse: `http://localhost:8000/luna-items.html`

4. **Configurar URL no frontend:**
   - Já está configurado para `http://localhost:5000`
   - Funciona automaticamente!

✅ **Pronto!** Agora você pode testar localmente.

---

### Opção 2: Deploy Gratuito (Render.com - RECOMENDADO)

**Render.com oferece hospedagem gratuita para Flask.**

#### Passo a passo:

1. **Criar conta em [Render.com](https://render.com)** (gratuito)

2. **Criar arquivo `render.yaml` na raiz do projeto:**
   ```yaml
   services:
     - type: web
       name: luna-votes-server
       runtime: python
       buildCommand: pip install -r requirements_votes.txt
       startCommand: python server_votes.py
       envVars:
         - key: PYTHON_VERSION
           value: 3.11.0
   ```

3. **Criar arquivo `Procfile` na raiz:**
   ```
   web: python server_votes.py
   ```

4. **Ajustar `server_votes.py` para produção:**
   - Render usa porta dinâmica, precisa ajustar

5. **No Render.com:**
   - New → Web Service
   - Conecte seu repositório GitHub
   - Render detecta automaticamente
   - Deploy!

6. **Atualizar URL no frontend:**
   - Render dá uma URL tipo: `https://luna-votes-server.onrender.com`
   - Atualize `luna-items.html` linha 340:
   ```javascript
   const SERVER_URL = 'https://seu-app.onrender.com';
   ```

✅ **Pronto!** Servidor rodando na nuvem.

---

### Opção 3: Railway.app (Alternativa)

Similar ao Render, mas com interface diferente.

1. Criar conta em [Railway.app](https://railway.app)
2. New Project → Deploy from GitHub
3. Selecionar repositório
4. Railway detecta Python automaticamente
5. Adicionar variável de ambiente: `PORT` (Railway define automaticamente)
6. Ajustar `server_votes.py` para usar `PORT` do ambiente

---

### Opção 4: Google Apps Script (Mais Simples, mas limitado)

**Vantagem:** Não precisa de servidor separado, usa Google Sheets.

Vou criar uma versão adaptada se você quiser.

---

## 🔧 Ajustes Necessários para Produção

### 1. Ajustar `server_votes.py` para usar porta do ambiente:

```python
import os

# No final do arquivo, substituir:
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port, debug=False)
```

### 2. Ajustar CORS se necessário:

Já está configurado com `CORS(app)`, mas se tiver problemas:

```python
CORS(app, resources={r"/api/*": {"origins": "https://concs93.github.io"}})
```

### 3. Atualizar URL no frontend:

```javascript
// Para produção
const SERVER_URL = 'https://seu-servidor.onrender.com';

// Para desenvolvimento local
// const SERVER_URL = 'http://localhost:5000';
```

---

## 🧪 Testar se está funcionando

1. **Testar servidor:**
   ```bash
   curl http://localhost:5000/api/health
   ```
   Deve retornar: `{"status":"ok","has_xlsx":true}`

2. **Testar votação:**
   ```bash
   curl -X POST http://localhost:5000/api/vote \
     -H "Content-Type: application/json" \
     -d '{"item_name":"Belt Whip","vote_type":"positive","action":"add"}'
   ```

3. **Verificar arquivos gerados:**
   - `luna_votes.csv` deve ter uma linha nova
   - `luna_votes_summary.json` deve ter o contador atualizado

---

## 📝 Checklist de Deploy

- [ ] Servidor rodando e testado localmente
- [ ] Conta criada no Render/Railway
- [ ] Repositório conectado
- [ ] Deploy realizado
- [ ] URL do servidor atualizada no `luna-items.html`
- [ ] Testado votação no site em produção
- [ ] Arquivos CSV/XLSX sendo gerados

---

## 🆘 Problemas Comuns

### CORS Error
- Verificar se `flask-cors` está instalado
- Verificar se `CORS(app)` está no código

### Servidor não responde
- Verificar se porta está correta
- Verificar logs do Render/Railway
- Testar endpoint `/api/health`

### Votos não salvam
- Verificar permissões de escrita no servidor
- Verificar logs de erro
- Verificar se arquivos estão sendo criados

---

## 💡 Recomendação

**Para começar rápido:**
1. Teste localmente primeiro (Opção 1)
2. Depois faça deploy no Render.com (Opção 2) - é gratuito e fácil

**Quer ajuda com alguma opção específica?** Me avise qual você prefere!
