# 🤖 Suporte.AI — Assistente de Suporte Técnico com IA e Voz

## 🎯 Objetivo Geral
Automatizar o atendimento técnico de 1º nível em empresas usando inteligência artificial, com foco em acessibilidade, linguagem simples e integração por voz, otimizando o tempo da equipe de suporte e melhorando a experiência do usuário.

---

## 🚀 Tech Voice Support IA: A Revolução no Atendimento Técnico
Descubra como o Suporte.AI está transformando o atendimento ao cliente, tornando-o mais rápido, eficiente e inteligente.

### ❌ O Problema do Suporte Tradicional
- 🕒 Filas longas, esperas intermináveis e frustração dos usuários.
- 🐢 Suporte técnico tradicional é lento, ineficiente e caro.
- ⏳ **Demora:** Longos tempos de espera e resolução.
- 😠 **Frustração:** Usuários perdidos e insatisfeitos.
- 💸 **Custo:** Operações caras e repetitivas.

### ✅ A Solução Tech Voice Support IA
O Suporte.AI é um assistente de voz inteligente que entende problemas técnicos comuns, resolve automaticamente ou registra chamados de forma eficiente.
- 🗣️ Assistente de voz intuitivo
- 🤓 Entendimento de problemas simples
- 📝 Resolução automática ou registro de chamados

### 🧠 Como Funciona: O Fluxo Inteligente
1. 🎤 **Voz do Utilizador:** O usuário descreve o problema por voz
2. 🧩 **Diagnóstico por IA:** A inteligência artificial compreende o problema
3. ⚡ **Ação Inteligente:** A IA resolve ou abre um chamado automaticamente

### 🛠️ Recursos Avançados
- 🔄 **Fallback Textual:** Transição para texto quando necessário
- 🔗 **Integrações Robustas:** REST APIs

### 💰 Impacto Financeiro e Operacional
- 📉 **Redução de Tickets:** Menos chamados rotineiros
- 🌐 **Disponibilidade:** Atendimento 24/7
- 🚀 **Maior agilidade = maior satisfação do cliente**

### ⚡ Agilidade e Escalabilidade
- ⚡ Atendimento imediato com interação por voz
- 🔌 Integração fácil com plataformas existentes

### 🏆 Diferenciais Competitivos
- 📚 **Aprendizado Contínuo:** Evolui com logs e interações
- 🔄 **Feedback Loop:** Aprimoramento constante da IA
- 🧬 **Adaptabilidade:** Ajusta-se a cada negócio

---

## 🧩 Componentes Principais

### 🗣️ VAP.AI (Voz Inteligente)
- 🎙️ Conversão de voz para texto (entrada do usuário)
- 🗨️ Conversão de texto para voz (resposta natural da IA)
- 🙋‍♂️ Permite que usuários falem com o assistente sem digitar.

### 🖥️ API com FastAPI + GLPI
- 📋 Registra automaticamente os chamados no sistema GLPI.
- 🗄️ Alternativa de integração com banco de dados ou sistemas internos.

### 🖥️ Interface
- 🌐 Navegador ou totem de atendimento
- 💬 Suporte a voz ou chat

### 📊 Dashboard (futuro)
- 📈 Métricas de atendimento, satisfação, tempo médio e temas recorrentes

---

## 💡 Casos de Uso
- 🖨️ **Impressora não imprime:** IA orienta os passos e, se necessário, registra o chamado.
- 🔑 **Problemas de login:** IA verifica etapas básicas antes de abrir chamado.
- ❓ **Dúvidas sobre como abrir um chamado:** IA orienta ou faz isso por voz.

---

## 🎁 Benefícios
- 📉 Redução de até 40% dos chamados manuais
- ⚡ Atendimento mais acessível, rápido e natural
- 🧑‍💻 Liberação da equipe de TI para tarefas mais estratégicas
- 📝 Registro automático de atendimentos

---

## 🏗️ Arquitetura Técnica
- 🗣️ **VAP.AI:** Módulo de entrada e saída por voz
- 🚀 **FastAPI:** API REST para criação de chamados
- ☁️ **Render:** Deploy gratuito do backend com render.yaml

---

## 📂 Arquivos Desenvolvidos
- `main.py` — API com FastAPI para integração com GLPI
- `glpi_api.py` — Cliente Python para comunicação com a API REST do GLPI
- `chamado_api.py` — API para criação automática de chamados no GLPI a partir de texto livre, com classificação automática de categoria
- `criar_categorias_glpi.py` — Script para criação automática da árvore de categorias no GLPI
- `requirements.txt` — Dependências do projeto
- `render.yaml` — Configuração para deploy no Render

---

## ⚙️ Como usar o chamado_api.py

1. **Configure o arquivo `.env`**
   - Copie o arquivo `.env.example` para `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edite o arquivo `.env` e preencha as variáveis necessárias:
     ```env
     GLPI_APP_TOKEN=seu_token_de_api_aqui
     GLPI_URL=sua_url_do_glpi_aqui
     GLPI_USER=seu_usuario_aqui
     GLPI_PASSWORD=sua_senha_aqui
     ```

2. **Execute a API**
   ```bash
   uvicorn chamado_api:app --reload
   ```

3. **Endpoint disponível:**
   - `POST /chamado`
     - Parâmetro: `texto` (str)
     - Exemplo de uso:
       ```json
       {
         "texto": "Preciso de ajuda com a impressora, está sem toner."
       }
       ```
     - O endpoint irá classificar automaticamente a categoria e criar o chamado no GLPI.

4. **Boas práticas de segurança**
   - Nunca exponha seu `GLPI_APP_TOKEN` ou outras credenciais publicamente.
   - Use variáveis de ambiente e arquivos `.env` para manter segredos fora do código-fonte.
   - Sempre use o arquivo `.env.example` como modelo, sem incluir credenciais reais.
   - Certifique-se de que o arquivo `.env` está no `.gitignore` para evitar que seja enviado ao repositório.

---

## 🛠️ Como Executar Localmente

1. **Clone o repositório:**
   ```bash
   git clone <URL_DO_SEU_REPOSITORIO>
   cd Suporte.AI
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate  # Windows
   # ou
   source venv/bin/activate  # Linux/Mac
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o arquivo `.env`:**
   - Copie o arquivo `.env.example` para `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edite o arquivo `.env` e preencha as variáveis de ambiente necessárias:
     - `GLPI_URL` - URL da sua instalação GLPI
     - `GLPI_USER` - Usuário do GLPI
     - `GLPI_PASSWORD` - Senha do usuário GLPI
     - `GLPI_APP_TOKEN` - Token de aplicação do GLPI

5. **Execute a API:**
   ```bash
   uvicorn main:app --reload
   ```

6. **Acesse a documentação interativa:**
   - [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## ☁️ Deploy no Render

- O arquivo `render.yaml` já está pronto para deploy gratuito no Render.com.
- Basta conectar o repositório e seguir as instruções da plataforma.