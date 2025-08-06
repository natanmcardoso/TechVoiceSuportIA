
# 🤖 Suporte.AI — Assistente de Suporte Técnico com IA e Voz

## 🎯 Objetivo Geral
Automatizar o atendimento técnico de 1º nível em empresas usando inteligência artificial, com foco em acessibilidade, linguagem simples e integração por voz, otimizando o tempo da equipe de suporte e melhorando a experiência do usuário.

## 🚀 Tech Voice Support IA: A Revolução no Atendimento Técnico
Descubra como o Suporte.AI está transformando o atendimento ao cliente, tornando-o mais rápido, eficiente e inteligente.

### ❌ O Problema do Suporte Tradicional
- 🕒 Filas longas, esperas intermináveis e frustração dos usuários.
- 🐢 Suporte técnico tradicional é lento, ineficiente e caro.
- ⏳ **Demora:** Longos tempos de espera e resolução.
- 😠 **Frustração:** Usuários perdidos e insatisfeitos.
- 💸 **Custo:** Operações caras e repetitivas.

### ✅ A Solução Tech Voice Support IA
O Suporte.AI é um assistente de voz inteligente que entende problemas técnicos comuns, resolve automaticamente ou registra chamados de forma eficiente:
- 🗣️ Assistente de voz intuitivo
- 🤓 Entendimento de problemas simples
- 📝 Resolução automática ou registro de chamados

## 🧠 Como Funciona: O Fluxo Inteligente
1. 🎤 **Voz do Utilizador:** O usuário descreve o problema por voz.
2. 🧩 **Diagnóstico por IA:** A inteligência artificial compreende o problema.
3. ⚡ **Ação Inteligente:** A IA resolve ou abre um chamado automaticamente.

## 🛠️ Recursos Avançados
- 🔄 **Fallback Textual:** Transição para texto quando necessário.
- 🔗 **Integrações Robustas:** REST APIs com GLPI.
- 🔐 **Autenticação Segura:** Via **App Token** e **User Token**.
- 🎤 **Integração com VAPI.IA:** Sincronização com assistente de voz inteligente.

## 💰 Impacto Financeiro e Operacional
- 📉 **Redução de Tickets:** Menos chamados rotineiros.
- 🌐 **Disponibilidade:** Atendimento 24/7.
- 🚀 **Agilidade:** Maior satisfação do cliente.

## 🏗️ Arquitetura Técnica
- 🗣️ **VAPI.IA:** Captura e processamento de voz.
- 🚀 **FastAPI:** API REST para integração e automação.
- 🔄 **GLPI:** Sistema de chamados com integração via API REST.
- ☁️ **Render:** Deploy do backend com variáveis seguras.

## 🔐 Segurança
- Nenhum token sensível é armazenado no código.
- Variáveis de ambiente via `.env` ou painel do Render.
- Validação de requisições VAPI via `Authorization: Bearer <VAPI_API_KEY>`.

## 📂 Estrutura do Projeto
- `main.py` — API principal com FastAPI.
- `glpi_api.py` — Cliente GLPI com autenticação e abertura de tickets.
- `render.yaml` — Configuração para deploy no Render.
- `.env.example` — Exemplo de variáveis de ambiente.

## ⚙️ Como Configurar Localmente
### 1️⃣ Clone o projeto:
git clone https://github.com/seu-usuario/suporte-ai.git
cd suporte-ai

### 2️⃣ Crie e ative um ambiente virtual:
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

### 3️⃣ Instale as dependências:
pip install -r requirements.txt

### 4️⃣ Crie o arquivo `.env`:
GLPI_URL=http://seu-glpi-url/apirest.php
GLPI_APP_TOKEN=seu_app_token
GLPI_USER_TOKEN=seu_user_token
VAPI_API_KEY=sua_chave_vapi

## ▶️ Executar a API Localmente
uvicorn main:app --reload

Acesse: http://127.0.0.1:8000/docs

## ☁️ Deploy no Render
Use o `render.yaml`:
services:
  - type: web
    name: suporte-ai
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn main:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: GLPI_URL
        sync: false
      - key: GLPI_APP_TOKEN
        sync: false
      - key: GLPI_USER_TOKEN
        sync: false
      - key: VAPI_API_KEY
        sync: false

Configure as variáveis no painel do Render.

## 🔍 Endpoints Principais
### ✅ Criar ticket via VAPI.IA
curl -X POST https://seu-render-url/armazenar-infos \
-H "Authorization: Bearer SUA_CHAVE_VAPI" \
-H "Content-Type: application/json" \
-d '{"name":"João","issue_description":"Computador não liga","contact_email":"joao@email.com"}'

### ✅ Criar ticket manualmente
curl -X POST https://seu-render-url/criar-chamado-glpi \
-H "Content-Type: application/json" \
-d '{"title":"Problema na rede","description":"Usuário sem internet","priority":3}'

## ✅ Integração com VAPI.IA
- Configure um **Webhook** no VAPI.IA apontando para:
POST https://seu-render-url/armazenar-infos

- Use o header:
Authorization: Bearer SUA_CHAVE_VAPI

- Estrutura JSON esperada:
{
  "name": "João",
  "issue_description": "Erro no sistema",
  "contact_email": "joao@email.com"
}

## ✅ Boas Práticas
- Use `.env.example` para documentar variáveis.
- Nunca exponha tokens no GitHub.
- Sempre feche as sessões GLPI (`killSession`) após uso.