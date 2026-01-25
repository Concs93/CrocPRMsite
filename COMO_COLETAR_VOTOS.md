# 📥 Como Coletar Votos - Guia Completo

## Como Funciona Atualmente

### ✅ O que acontece quando alguém vota:

1. **Pessoa acessa o site:** `https://concs93.github.io/CrocPRMsite/luna-items`
2. **Pessoa vota:** Clica em ✓, ○, ou ✗ em um item
3. **Voto é salvo:** 
   - No navegador da pessoa (localStorage)
   - Em um arquivo JSON local (para exportação)
   - **NÃO vai automaticamente para o GitHub** (por segurança)

### 📊 Onde ficam os votos:

- **localStorage do navegador:** Cada pessoa tem seus próprios votos
- **Arquivo JSON local:** Acumula todos os votos da pessoa (para exportar)

## 🔄 Como Coletar os Votos

### Opção 1: Botão de Exportação (Mais Fácil)

1. **Pessoa acessa o site e vota**
2. **Pessoa clica no botão "📥 Exportar Meus Votos"**
3. **Arquivo JSON é baixado** automaticamente
4. **Pessoa envia o arquivo para você** (Discord, email, etc.)
5. **Você junta todos os arquivos** usando o script Python

### Opção 2: Você Coleta Manualmente

1. **Você acessa o site** e vota também
2. **Você clica em "📥 Exportar Meus Votos"**
3. **Você recebe o arquivo JSON**
4. **Você faz commit no GitHub** usando o script

### Opção 3: Script Automático (Futuro)

Posso criar um script que:
- Lê vários arquivos JSON exportados
- Junta tudo em um único arquivo
- Faz commit automático no GitHub

## 📋 Processo Completo

### Passo 1: Pessoas Votam

- Acessam o site
- Votam nos itens
- Clicam em "Exportar Meus Votos"
- Enviam o arquivo JSON para você

### Passo 2: Você Coleta

Você recebe vários arquivos JSON, tipo:
- `luna_votes_2025-01-24_pessoa1.json`
- `luna_votes_2025-01-24_pessoa2.json`
- etc.

### Passo 3: Você Junta os Arquivos

**Opção A - Manual:**
1. Abra cada arquivo JSON
2. Copie os votos
3. Cole tudo em um único `luna_votes_data.json`

**Opção B - Script Python (Vou criar):**
```bash
python merge_votes.py arquivo1.json arquivo2.json arquivo3.json
```

### Passo 4: Fazer Commit no GitHub

```bash
python commit_votes_to_github.py
```

Isso vai:
- Ler `luna_votes_data.json`
- Fazer commit no GitHub
- Atualizar `luna_votes_summary.json`

### Passo 5: Gerar CSV/XLSX

```bash
python generate_csv_from_github.py
```

## 🎯 Exemplo Prático

1. **João vota** → Exporta → Envia `joao_votes.json`
2. **Maria vota** → Exporta → Envia `maria_votes.json`
3. **Você junta** os dois arquivos
4. **Você faz commit** no GitHub
5. **Site atualiza** automaticamente com os votos

## 💡 Dica

**Para facilitar, você pode:**
- Criar um canal no Discord só para receber os arquivos JSON
- Ou um Google Form onde as pessoas fazem upload
- Ou você mesmo acessa o site e vota (seus votos ficam salvos)

## ❓ Perguntas Frequentes

**P: Os votos vão automaticamente para o GitHub?**
R: Não, por segurança. Cada pessoa precisa exportar e você faz commit.

**P: Posso ver os votos de outras pessoas?**
R: Não diretamente. Cada pessoa precisa exportar e enviar para você.

**P: E se alguém votar várias vezes?**
R: O sistema permite mudar o voto, mas cada navegador só tem 1 voto por item.

**P: Como sei quantos votos tem?**
R: Depois de fazer commit, o `luna_votes_summary.json` mostra os totais.

---

## 🚀 Próximos Passos

Quer que eu crie um script que:
- Junta vários arquivos JSON automaticamente?
- Ou uma solução mais automática?

Me avise! 😊
