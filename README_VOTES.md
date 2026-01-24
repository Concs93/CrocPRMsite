# Sistema de Votação - Itens Luna Obscura

Este sistema permite coletar votos dos itens e salvar em arquivos CSV e XLSX.

## 📋 Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

## 🚀 Como usar

### 1. Instalar dependências

```bash
pip install -r requirements_votes.txt
```

### 2. Iniciar o servidor

```bash
python server_votes.py
```

O servidor ficará rodando em `http://localhost:5000`

### 3. Acessar a página

Abra `luna-items.html` no navegador. A página tentará se conectar ao servidor automaticamente.

## 📁 Arquivos gerados

O servidor cria automaticamente os seguintes arquivos:

- **luna_votes.csv** - Histórico completo de todos os votos (timestamp, item, tipo, ação)
- **luna_votes.xlsx** - Mesmo conteúdo em formato Excel
- **luna_votes_summary.json** - Resumo atualizado com contadores de cada item

## 🔧 Configuração

### Alterar porta do servidor

Edite `server_votes.py` e altere a linha:
```python
app.run(host='0.0.0.0', port=5000, debug=True)
```

### Alterar URL do servidor no frontend

Edite `luna-items.html` e altere:
```javascript
const SERVER_URL = 'http://localhost:5000';
```

Para usar em produção, altere para a URL do seu servidor:
```javascript
const SERVER_URL = 'https://seu-servidor.com';
```

## 📊 Estrutura dos dados

### CSV/XLSX
Cada linha contém:
- **Timestamp**: Data e hora do voto
- **Item**: Nome do item
- **Tipo de Voto**: `positive`, `neutral` ou `negative`
- **Ação**: `add` (adicionar) ou `remove` (remover)

### JSON Summary
```json
{
  "Belt Whip": {
    "positive": 5,
    "neutral": 2,
    "negative": 1
  },
  ...
}
```

## 🌐 Deploy em produção

Para usar em produção, você pode:

1. **Servidor próprio**: Deploy o `server_votes.py` em um servidor (Heroku, DigitalOcean, etc.)
2. **Google Apps Script**: Adaptar para usar Google Sheets como backend
3. **Firebase**: Usar Firebase Realtime Database

## ⚠️ Notas

- O servidor precisa estar rodando para que os votos sejam salvos
- Se o servidor estiver offline, os votos ficam apenas no navegador (localStorage)
- Os arquivos CSV/XLSX são criados na mesma pasta onde o servidor está rodando
- O servidor atualiza os arquivos em tempo real a cada voto
