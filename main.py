from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from glpi_api import GLPIClient
import requests
import os
import base64
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

GLPI_URL = os.getenv('GLPI_URL')
GLPI_APP_TOKEN = os.getenv('GLPI_APP_TOKEN')

app = FastAPI(title="Suporte.AI API")

class TicketRequest(BaseModel):
    """
    Modelo de requisição para criação de ticket.
    title: Título do chamado.
    description: Descrição detalhada do chamado.
    requester_email: E-mail do solicitante.
    """
    title: str
    description: str
    requester_email: str

# Modelo para o endpoint /chamado
class ChamadoRequest(BaseModel):
    texto: str

# Mapeamento das categorias do GLPI
CATEGORIAS = {
    "infraestrutura": {"category_id": 1, "title": "Infraestrutura"},
    "infraestrutura backup": {"category_id": 2, "title": "Infraestrutura > Backup"},
    "infraestrutura backup agendamento": {"category_id": 3, "title": "Infraestrutura > Backup > Agendamento"},
    "infraestrutura backup falha de backup": {"category_id": 4, "title": "Infraestrutura > Backup > Falha de Backup"},
    "infraestrutura backup restauração": {"category_id": 5, "title": "Infraestrutura > Backup > Restauração"},
    "infraestrutura computadores": {"category_id": 6, "title": "Infraestrutura > Computadores"},
    "infraestrutura computadores desktops": {"category_id": 7, "title": "Infraestrutura > Computadores > Desktops"},
    "infraestrutura computadores formatação reinstalação": {"category_id": 8, "title": "Infraestrutura > Computadores > Formatação/Reinstalação"},
    "infraestrutura computadores notebooks": {"category_id": 9, "title": "Infraestrutura > Computadores > Notebooks"},
    "infraestrutura computadores upgrade manutenção": {"category_id": 10, "title": "Infraestrutura > Computadores > Upgrade/Manutenção"},
    "infraestrutura data center": {"category_id": 11, "title": "Infraestrutura > Data Center"},
    "infraestrutura data center climatização": {"category_id": 12, "title": "Infraestrutura > Data Center > Climatização"},
    "infraestrutura data center energia": {"category_id": 13, "title": "Infraestrutura > Data Center > Energia"},
    "infraestrutura data center racks": {"category_id": 14, "title": "Infraestrutura > Data Center > Racks"},
    "infraestrutura firewall security": {"category_id": 15, "title": "Infraestrutura > Firewall/Security"},
    "infraestrutura firewall security bloqueio de sites": {"category_id": 16, "title": "Infraestrutura > Firewall/Security > Bloqueio de Sites"},
    "infraestrutura firewall security regras de acesso": {"category_id": 17, "title": "Infraestrutura > Firewall/Security > Regras de Acesso"},
    "infraestrutura impressoras": {"category_id": 18, "title": "Infraestrutura > Impressoras"},
    "infraestrutura impressoras compartilhamento": {"category_id": 19, "title": "Infraestrutura > Impressoras > Compartilhamento"},
    "infraestrutura impressoras configuração": {"category_id": 20, "title": "Infraestrutura > Impressoras > Configuração"},
    "infraestrutura impressoras erro físico": {"category_id": 21, "title": "Infraestrutura > Impressoras > Erro Físico"},
    "infraestrutura impressoras falta de tinta toner": {"category_id": 22, "title": "Infraestrutura > Impressoras > Falta de Tinta/Toner"},
    "infraestrutura periféricos": {"category_id": 23, "title": "Infraestrutura > Periféricos"},
    "infraestrutura periféricos monitor": {"category_id": 24, "title": "Infraestrutura > Periféricos > Monitor"},
    "infraestrutura periféricos outros": {"category_id": 25, "title": "Infraestrutura > Periféricos > Outros"},
    "infraestrutura periféricos outros dúvidas gerais": {"category_id": 26, "title": "Infraestrutura > Periféricos > Outros > Dúvidas Gerais"},
    "infraestrutura periféricos outros solicitações diversas": {"category_id": 27, "title": "Infraestrutura > Periféricos > Outros > Solicitações Diversas"},
    "infraestrutura periféricos teclado mouse": {"category_id": 28, "title": "Infraestrutura > Periféricos > Teclado/Mouse"},
    "infraestrutura rede": {"category_id": 29, "title": "Infraestrutura > Rede"},
    "infraestrutura rede cabeada": {"category_id": 30, "title": "Infraestrutura > Rede > Cabeada"},
    "infraestrutura rede lentidão": {"category_id": 31, "title": "Infraestrutura > Rede > Lentidão"},
    "infraestrutura rede sem conexão": {"category_id": 32, "title": "Infraestrutura > Rede > Sem Conexão"},
    "infraestrutura rede vpn": {"category_id": 33, "title": "Infraestrutura > Rede > VPN"},
    "infraestrutura rede wi-fi": {"category_id": 34, "title": "Infraestrutura > Rede > Wi-Fi"},
    "infraestrutura servidores": {"category_id": 35, "title": "Infraestrutura > Servidores"},
    "infraestrutura servidores backup de servidor": {"category_id": 36, "title": "Infraestrutura > Servidores > Backup de Servidor"},
    "infraestrutura servidores linux": {"category_id": 37, "title": "Infraestrutura > Servidores > Linux"},
    "infraestrutura servidores virtualização": {"category_id": 38, "title": "Infraestrutura > Servidores > Virtualização"},
    "infraestrutura servidores windows": {"category_id": 39, "title": "Infraestrutura > Servidores > Windows"},
    "infraestrutura software de infraestrutura": {"category_id": 40, "title": "Infraestrutura > Software de Infraestrutura"},
    "infraestrutura software de infraestrutura antivírus": {"category_id": 41, "title": "Infraestrutura > Software de Infraestrutura > Antivírus"},
    "infraestrutura software de infraestrutura ferramentas de monitoramento": {"category_id": 42, "title": "Infraestrutura > Software de Infraestrutura > Ferramentas de Monitoramento"},
    "infraestrutura software de infraestrutura licenciamento": {"category_id": 43, "title": "Infraestrutura > Software de Infraestrutura > Licenciamento"},
    "infraestrutura telefonia": {"category_id": 44, "title": "Infraestrutura > Telefonia"},
    "infraestrutura telefonia convencional": {"category_id": 45, "title": "Infraestrutura > Telefonia > Convencional"},
    "infraestrutura telefonia ip": {"category_id": 46, "title": "Infraestrutura > Telefonia > IP"},
    "infraestrutura telefonia pabx": {"category_id": 47, "title": "Infraestrutura > Telefonia > PABX"}
}

def classify_intent(texto):
    """
    Classifica a intenção do texto recebido, buscando a categoria mais específica.
    Prioriza categorias de nível mais profundo.
    :param texto: Texto enviado pelo usuário
    :return: Dicionário com 'category_id' e 'title' da categoria encontrada
    """
    texto = texto.lower()
    for key, value in sorted(CATEGORIAS.items(), key=lambda x: x[0].count(' '), reverse=True):
        if any(word in texto for word in key.split()):
            return value
    return CATEGORIAS.get("infraestrutura", {"category_id": 1, "title": "Infraestrutura"})

@app.post("/chamado")
async def create_chamado(request: ChamadoRequest):
    """
    Endpoint para criar um chamado no GLPI a partir de um texto livre.
    O texto é classificado para identificar a categoria correta.
    :param texto: Texto enviado pelo usuário
    :return: Resposta da API do GLPI
    """
    try:
        intent = classify_intent(request.texto)
        # Configurar headers básicos
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {base64.b64encode(f'{os.getenv("GLPI_USER")}:{os.getenv("GLPI_PASSWORD")}'.encode()).decode()}",
            "App-Token": GLPI_APP_TOKEN
        }
        # Primeiro, iniciar uma sessão
        init_session_url = f"{GLPI_URL}/apirest.php/initSession"
        init_response = requests.get(init_session_url, headers=headers)
        init_response.raise_for_status()
        session_data = init_response.json()
        session_token = session_data.get('session_token')
        
        if not session_token:
            return {"error": "Falha ao obter session_token", "response": session_data}
        
        # Adicionar o token de sessão aos headers
        headers["Session-Token"] = session_token
        
        # Criar o chamado
        ticket_url = f"{GLPI_URL}/apirest.php/Ticket"
        payload = {
            "input": {
                "name": intent["title"],
                "content": f"Usuário relatou: {request.texto}",
                "itilcategories_id": intent["category_id"],
                "type": 1,  # Incidente
                "status": 1  # Novo
            }
        }
        ticket_response = requests.post(ticket_url, json=payload, headers=headers)
        
        # Encerrar a sessão
        kill_session_url = f"{GLPI_URL}/apirest.php/killSession"
        requests.get(kill_session_url, headers=headers)
        
        try:
            ticket_data = ticket_response.json()
            return ticket_data
        except Exception:
            return {
                "status_code": ticket_response.status_code,
                "text": ticket_response.text,
                "error": "Erro ao decodificar resposta do GLPI. Veja o campo 'text' para detalhes."
            }
    except Exception as e:
        return {"error": str(e)}

@app.post("/create-ticket/")
def create_ticket(request: TicketRequest):
    """
    Endpoint para criar um chamado no GLPI.
    Recebe os dados do chamado, autentica no GLPI, cria o chamado.
    """
    glpi = GLPIClient()
    glpi.authenticate()
    if not glpi.session_token:
        raise HTTPException(status_code=500, detail="Falha na autenticação com o GLPI.")
    ticket_id = glpi.create_ticket(request.title, request.description, request.requester_email)
    if not ticket_id:
        glpi.logout()
        raise HTTPException(status_code=500, detail="Falha ao criar o chamado no GLPI.")
    glpi.logout()
    return {"message": "Chamado criado com sucesso!", "ticket_id": ticket_id}

@app.get("/health")
def health_check():
    """
    Endpoint de verificação de saúde da API.
    Retorna status ok se a API estiver rodando.
    """
    return {"status": "ok"}

@app.get("/test-env")
def test_env():
    """
    Endpoint para testar as variáveis de ambiente.
    Retorna as variáveis de ambiente carregadas.
    """
    return {
        "GLPI_URL": GLPI_URL,
        "GLPI_APP_TOKEN": GLPI_APP_TOKEN[:5] + "*****" if GLPI_APP_TOKEN else None  # Mostra apenas os primeiros 5 caracteres por segurança
    }

@app.get("/test-auth")
def test_auth():
    """
    Endpoint para testar a autenticação com o GLPI.
    Tenta iniciar uma sessão e retorna o resultado.
    """
    try:
        glpi = GLPIClient()
        glpi.authenticate()
        result = {
            "authenticated": glpi.session_token is not None,
            "session_token": glpi.session_token[:5] + "*****" if glpi.session_token else None
        }
        if glpi.session_token:
            glpi.logout()
        return result
    except Exception as e:
        return {"error": str(e)}

@app.get("/test-classify")
def test_classify(texto: str):
    """
    Endpoint para testar a classificação de intenções.
    Recebe um texto e retorna a categoria identificada.
    """
    try:
        intent = classify_intent(texto)
        return {
            "texto": texto,
            "categoria": intent
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/test-direct-ticket")
def test_direct_ticket(texto: str):
    """
    Endpoint para testar a criação de chamados diretamente no GLPI.
    Recebe um texto, classifica e tenta criar um chamado usando o método direto.
    """
    try:
        intent = classify_intent(texto)
        headers = {
            "Content-Type": "application/json",
            "App-Token": GLPI_APP_TOKEN
        }
        # Primeiro, iniciar uma sessão
        init_session_url = f"{GLPI_URL}/apirest.php/initSession"
        init_response = requests.get(init_session_url, headers=headers, auth=(os.getenv('GLPI_USER'), os.getenv('GLPI_PASSWORD')))
        init_response.raise_for_status()
        session_data = init_response.json()
        session_token = session_data.get('session_token')
        
        if not session_token:
            return {"error": "Falha ao obter session_token", "response": session_data}
        
        # Adicionar o token de sessão aos headers
        headers["Session-Token"] = session_token
        
        # Criar o chamado
        ticket_url = f"{GLPI_URL}/apirest.php/Ticket"
        payload = {
            "input": {
                "name": intent["title"],
                "content": f"Usuário relatou: {texto}",
                "itilcategories_id": intent["category_id"],
                "type": 1,  # Incidente
                "status": 1  # Novo
            }
        }
        ticket_response = requests.post(ticket_url, json=payload, headers=headers)
        
        # Encerrar a sessão
        kill_session_url = f"{GLPI_URL}/apirest.php/killSession"
        requests.get(kill_session_url, headers=headers)
        
        try:
            ticket_data = ticket_response.json()
            return {
                "success": True,
                "ticket": ticket_data,
                "status_code": ticket_response.status_code
            }
        except Exception:
            return {
                "success": False,
                "status_code": ticket_response.status_code,
                "text": ticket_response.text,
                "error": "Erro ao decodificar resposta do GLPI"
            }
    except Exception as e:
        return {"error": str(e)}

@app.post("/test-chamado-request")
def test_chamado_request(request: ChamadoRequest):
    """
    Endpoint para testar a criação de chamados usando o modelo ChamadoRequest.
    Recebe um objeto ChamadoRequest e tenta criar um chamado.
    """
    try:
        # Usar o endpoint /chamado para criar o chamado
        result = create_chamado(request)
        return {
            "success": True,
            "result": result,
            "texto": request.texto
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/test-glpi-connection")
def test_glpi_connection():
    """
    Endpoint para testar a conexão com o GLPI sem autenticação.
    Verifica se o servidor GLPI está acessível.
    """
    try:
        # Tentar acessar a página inicial do GLPI
        response = requests.get(GLPI_URL, timeout=5)
        return {
            "success": response.status_code == 200,
            "status_code": response.status_code,
            "url": GLPI_URL,
            "response_size": len(response.text)
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/test-glpi-api")
def test_glpi_api():
    """
    Endpoint para testar a API do GLPI diretamente.
    Verifica se a API do GLPI está acessível e retorna informações sobre ela.
    """
    try:
        # Tentar acessar a API do GLPI
        api_url = f"{GLPI_URL}/apirest.php"
        response = requests.get(api_url, timeout=5)
        return {
            "success": response.status_code == 200,
            "status_code": response.status_code,
            "url": api_url,
            "response_size": len(response.text),
            "response_text": response.text[:500] if len(response.text) > 500 else response.text  # Limitar o tamanho da resposta
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/test-init-session")
def test_init_session(auth_method: str = "basic"):
    """
    Endpoint para testar a inicialização de sessão no GLPI com diferentes métodos de autenticação.
    :param auth_method: Método de autenticação a ser usado (basic, token, params)
    """
    try:
        headers = {
            "Content-Type": "application/json",
            "App-Token": GLPI_APP_TOKEN
        }
        init_session_url = f"{GLPI_URL}/apirest.php/initSession"
        
        if auth_method == "basic":
            # Autenticação básica (usuário e senha no cabeçalho de autenticação)
            response = requests.get(init_session_url, headers=headers, auth=(os.getenv('GLPI_USER'), os.getenv('GLPI_PASSWORD')))
        elif auth_method == "token":
            # Autenticação com token de usuário
            headers["Authorization"] = f"user_token {GLPI_APP_TOKEN}"
            response = requests.get(init_session_url, headers=headers)
        elif auth_method == "params":
            # Autenticação com parâmetros de consulta
            params = {
                "login": os.getenv('GLPI_USER'),
                "password": os.getenv('GLPI_PASSWORD')
            }
            response = requests.get(init_session_url, headers=headers, params=params)
        else:
            return {"error": f"Método de autenticação inválido: {auth_method}"}
        
        try:
            response_json = response.json()
            return {
                "success": response.status_code == 200,
                "status_code": response.status_code,
                "auth_method": auth_method,
                "response": response_json
            }
        except Exception:
            return {
                "success": False,
                "status_code": response.status_code,
                "auth_method": auth_method,
                "text": response.text,
                "error": "Erro ao decodificar resposta do GLPI"
            }
    except Exception as e:
        return {"error": str(e)}