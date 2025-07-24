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

### Componentes Principais
- 🗣️ **VAP.AI:** Módulo de entrada e saída por voz
- 🚀 **FastAPI:** API REST para criação de chamados
- 🔄 **GLPI Integration:** Integração com o sistema de chamados GLPI
- ☁️ **Render:** Deploy gratuito do backend com render.yaml

### Fluxo de Funcionamento
1. O usuário descreve seu problema por voz ou texto
2. O sistema converte a voz em texto (quando aplicável)
3. A API processa o texto e identifica a categoria do problema
4. O sistema cria automaticamente um chamado no GLPI com a categoria correta
5. O usuário recebe confirmação da abertura do chamado

### Classificação Automática de Categorias
O sistema utiliza um algoritmo de classificação baseado em palavras-chave para identificar a categoria mais adequada para cada problema relatado. O processo funciona da seguinte forma:

1. O texto do usuário é convertido para minúsculas
2. O sistema compara o texto com as palavras-chave de cada categoria
3. A categoria com mais correspondências é selecionada
4. Se nenhuma categoria específica for identificada, o sistema usa a categoria padrão "Infraestrutura"

Este método permite uma classificação rápida e eficiente sem a necessidade de modelos complexos de machine learning.

---

## 📂 Arquivos Desenvolvidos

### Arquivos Principais
- `main.py` — API principal com FastAPI para integração com GLPI, incluindo endpoints para criação de chamados e classificação de categorias
- `glpi_api.py` — Cliente Python para comunicação com a API REST do GLPI, responsável por autenticação, criação de chamados e gerenciamento de sessões
- `chamado_api.py` — API para criação automática de chamados no GLPI a partir de texto livre, com classificação automática de categoria baseada em palavras-chave

### Scripts Utilitários
- `criar_categorias_glpi.py` — Script para criação automática da árvore de categorias no GLPI
- `list_glpi_categories.py` — Script para listar categorias existentes no GLPI
- `test_glpi_categories.py` — Script para testar a classificação de categorias

### Arquivos de Configuração
- `requirements.txt` — Dependências do projeto (FastAPI, Uvicorn, Requests, python-dotenv)
- `render.yaml` — Configuração para deploy no Render com variáveis de ambiente seguras
- `.env.example` — Modelo para configuração das variáveis de ambiente necessárias
- `.gitignore` — Configuração para excluir arquivos sensíveis do controle de versão

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
   cd TechVoiceSuportIA
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
     - `GLPI_URL` - URL da sua instalação GLPI (ex: https://glpi.seudominio.com)
     - `GLPI_USER` - Usuário do GLPI com permissões para criar chamados
     - `GLPI_PASSWORD` - Senha do usuário GLPI
     - `GLPI_APP_TOKEN` - Token de aplicação do GLPI (gerado nas configurações do GLPI)

5. **Execute a API principal:**
   ```bash
   uvicorn main:app --reload
   ```
   
   **Ou execute a API de chamados:**
   ```bash
   uvicorn chamado_api:app --reload
   ```

6. **Acesse a documentação interativa:**
   - Para a API principal: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - Para a API de chamados: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

7. **Teste a criação de chamados:**
   - Envie uma requisição POST para `/chamado` com um texto descrevendo o problema
   - A API classificará automaticamente o problema e criará um chamado no GLPI
   - Exemplo usando curl:
     ```bash
     curl -X POST "http://127.0.0.1:8000/chamado" -H "Content-Type: application/json" -d '{"texto": "Minha impressora está sem toner"}'
     ```

---

## ☁️ Deploy no Render

- O arquivo `render.yaml` já está pronto para deploy gratuito no Render.com.
- Basta conectar o repositório e seguir as instruções da plataforma.
- Importante: Você precisará configurar as variáveis de ambiente no dashboard do Render:
  - `GLPI_URL`
  - `GLPI_USER`
  - `GLPI_PASSWORD`
  - `GLPI_APP_TOKEN`

## 🔒 Segurança e Boas Práticas

1. **Proteção de Credenciais**
   - Nunca comite arquivos `.env` com credenciais reais no repositório.
   - Use o arquivo `.env.example` como modelo, sem incluir credenciais reais.
   - Certifique-se de que o arquivo `.env` está listado no `.gitignore`.
   - No ambiente de produção, use variáveis de ambiente em vez de arquivos `.env`.

2. **Remoção de Arquivos Sensíveis do Histórico**
   - Se acidentalmente commitou arquivos sensíveis, use os seguintes comandos para removê-los:
     ```bash
     # Remover o arquivo .env do histórico do Git
     git filter-branch --force --index-filter "git rm --cached --ignore-unmatch .env" --prune-empty --tag-name-filter cat -- --all
     
     # Forçar a atualização do repositório local
     git reflog expire --expire=now --all
     git gc --prune=now --aggressive
     
     # Forçar o push para o repositório remoto
     git push origin --force --all
     ```

3. **Boas Práticas de Código**
   - Mantenha o código modular e bem documentado.
   - Adicione comentários explicativos em funções complexas.
   - Siga as convenções de nomenclatura do Python (snake_case para variáveis e funções).
   - Utilize tipagem quando possível para melhorar a legibilidade.

## 🤝 Contribuições e Desenvolvimento Futuro

### Como Contribuir
1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

### Próximos Passos
- **Integração com IA Avançada**: Implementar modelos de machine learning para melhorar a classificação de problemas.
- **Interface Web**: Desenvolver uma interface web amigável para interação com o usuário.
- **Análise de Sentimento**: Adicionar análise de sentimento para identificar a urgência dos chamados.
- **Dashboard de Métricas**: Criar um dashboard para visualização de métricas de atendimento.
- **Suporte a Múltiplos Idiomas**: Adicionar suporte para outros idiomas além do português.