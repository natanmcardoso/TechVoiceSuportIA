from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from glpi_api import GLPIClient  # Mantém o cliente GLPI
from urllib.parse import urljoin
import requests
import json
from fastapi import Request
from dotenv import load_dotenv
import os
import logging


# Configuração inicial
load_dotenv()
app = FastAPI(title="TechVoiceSuportIA API")

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variáveis de ambiente
GLPI_URL = os.getenv("GLPI_URL")
GLPI_APP_TOKEN = os.getenv("GLPI_APP_TOKEN")
GLPI_USER_TOKEN = os.getenv("GLPI_USER_TOKEN")
VAPI_API_KEY = os.getenv("VAPI_API_KEY")

if not all([GLPI_APP_TOKEN, GLPI_USER_TOKEN, VAPI_API_KEY]):
    raise RuntimeError("GLPI_APP_TOKEN, GLPI_USER_TOKEN e VAPI_API_KEY são obrigatórios no .env")

# Validação inicial
if not all([GLPI_APP_TOKEN, GLPI_USER_TOKEN, VAPI_API_KEY]):
    raise RuntimeError("GLPI_APP_TOKEN, GLPI_USER_TOKEN e VAPI_API_KEY são obrigatórios no .env")

# Mapeamento de categorias do GLPI
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

# Modelos Pydantic
class Consulta(BaseModel):
    problema: str

class Ticket(BaseModel):
    nome: str
    email: str
    problema: str

class Feedback(BaseModel):
    nota: int
    comentario: str = None
    ticket_id: str = None

class ChamadoRequest(BaseModel):
    texto: str

class TicketRequest(BaseModel):
    title: str
    description: str
    requester_email: str

# Funções auxiliares
def iniciar_sessao():
    url = f"{GLPI_URL}/initSession"
    headers = {
        "Content-Type": "application/json",
        "App-Token": GLPI_APP_TOKEN
    }
    payload = {"user_token": GLPI_USER_TOKEN}
    logger.info(f"Tentando iniciar sessão com URL: {url}, Headers: {headers}, Payload: {payload}")
    response = requests.post(url, json=payload, headers=headers, timeout=10)
    logger.info(f"Resposta do GLPI: Status {response.status_code}, Texto: {response.text}")
    if response.status_code == 200:
        session_data = response.json()
        session_token = session_data.get("session_token")
        if session_token:
            logger.info(f"Sessão iniciada com sucesso. Token: {session_token[:8]}****")
            return session_token
        else:
            raise HTTPException(status_code=400, detail="Session_token não encontrado na resposta do GLPI.")
    raise HTTPException(status_code=response.status_code, detail=f"Erro ao iniciar sessão: {response.text}")

def close_glpi_session(session_token: str):
    headers = {"App-Token": GLPI_APP_TOKEN, "Session-Token": session_token}
    requests.get(f"{GLPI_URL}/killSession", headers=headers, timeout=10)

def classify_intent(texto: str):
    texto = texto.lower()
    for key, value in sorted(CATEGORIAS.items(), key=lambda x: x[0].count(' '), reverse=True):
        if all(word in texto for word in key.split()):
            return value
    return CATEGORIAS.get("infraestrutura", {"category_id": 1, "title": "Infraestrutura"})

# Endpoints para Tools do VAPI (sem workflow)
from fastapi import Request
import json

@app.post("/consultar_solucao")
async def consultar_solucao(request: Request):
    body = await request.body()
    raw_payload = body.decode('utf-8')
    logger.info(f"Raw payload recebido em /consultar_solucao: {raw_payload}")
    try:
        data = json.loads(raw_payload)
        # Extrai os argumentos do toolCall
        arguments = data.get('message', {}).get('toolCalls', [{}])[0].get('function', {}).get('arguments', {})
        consulta = Consulta(**arguments)  # Valida os argumentos com o modelo Consulta
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao decodificar JSON: {str(e)}")
        raise HTTPException(status_code=422, detail="Payload JSON inválido")
    except Exception as e:
        logger.error(f"Erro de validação em /consultar_solucao: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))

    session_token = iniciar_sessao()
    try:
        search_url = f"{GLPI_URL}/KnowbaseItem"
        headers = {"Content-Type": "application/json", "Session-Token": session_token, "App-Token": GLPI_APP_TOKEN}
        search_data = {
            "criteria": [{"field": "12", "searchtype": "contains", "value": consulta.problema}],
            "range": "0-10"
        }
        response = requests.get(search_url, params=search_data, headers=headers, timeout=10)
        response.raise_for_status()
        results = response.json()
        return {"solucao": results[0]["answer"] if results and len(results) > 0 else None}
    except Exception as e:
        logger.error(f"Erro ao consultar solução: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_glpi_session(session_token)

@app.post("/criar_ticket")
async def criar_ticket(request: Request):
    body = await request.body()
    raw_payload = body.decode('utf-8')
    logger.info(f"Raw payload recebido em /criar_ticket: {raw_payload}")
    try:
        data = json.loads(raw_payload)
        # Extrai os argumentos do toolCall
        arguments = data.get('message', {}).get('toolCalls', [{}])[0].get('function', {}).get('arguments', {})
        ticket = Ticket(**arguments)  # Valida os argumentos com o modelo Ticket
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao decodificar JSON: {str(e)}")
        raise HTTPException(status_code=422, detail="Payload JSON inválido")
    except Exception as e:
        logger.error(f"Erro de validação em /criar_ticket: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))

    session_token = iniciar_sessao()
    try:
        ticket_url = f"{GLPI_URL}/Ticket"
        logger.info(f"Tentando criar ticket em: {ticket_url} com session_token: {session_token[:8]}****")
        headers = {"Content-Type": "application/json", "Session-Token": session_token, "App-Token": GLPI_APP_TOKEN}
        intent = classify_intent(ticket.problema)
        ticket_data = {
            "input": {
                "name": intent["title"],
                "content": f"Usuário: {ticket.nome}\nEmail: {ticket.email}\nProblema: {ticket.problema}",
                "itilcategories_id": intent["category_id"],
                "type": 1,
                "status": 1,
                "entities_id": 1
            }
        }
        response = requests.post(ticket_url, json=ticket_data, headers=headers, timeout=10)
        logger.info(f"Resposta do GLPI para criar ticket: Status {response.status_code}, Texto: {response.text}")
        if response.status_code == 403:
            logger.error(f"Erro 403: Permissão negada para {ticket_url} - Resposta: {response.text}")
            raise HTTPException(status_code=403, detail=f"Permissão negada no GLPI. Resposta: {response.text}")
        response.raise_for_status()
        ticket_id = response.json().get("id")
        return f"Ticket criado com sucesso com ID {ticket_id}"  # Retorno simples como string
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao criar ticket: {str(e)} - Resposta: {getattr(e.response, 'text', 'Sem resposta')}")
        raise HTTPException(status_code=500, detail=f"Erro ao conectar ao GLPI: {str(e)}")
    except Exception as e:
        logger.error(f"Erro inesperado ao criar ticket: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_glpi_session(session_token)

@app.post("/coletar_feedback")
async def coletar_feedback(feedback: Feedback):
    session_token = iniciar_sessao()
    try:
        headers = {"Content-Type": "application/json", "Session-Token": session_token, "App-Token": GLPI_APP_TOKEN}
        if feedback.ticket_id:
            followup_data = {
                "input": {
                    "tickets_id": feedback.ticket_id,
                    "content": f"Feedback: Nota {feedback.nota}/5. Comentário: {feedback.comentario or 'Nenhum'}"
                }
            }
            response = requests.post(f"{GLPI_URL}/TicketFollowup", json=followup_data, headers=headers, timeout=10)
            response.raise_for_status()
        return {"message": "Feedback coletado!"}
    except Exception as e:
        logger.error(f"Erro ao coletar feedback: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_glpi_session(session_token)

# Endpoints existentes do seu código
@app.post("/chamado")
async def create_chamado(request: ChamadoRequest):
    try:
        intent = classify_intent(request.texto)
        session_token = iniciar_sessao()
        
        headers = {
            "Content-Type": "application/json",
            "App-Token": GLPI_APP_TOKEN,
            "Session-Token": session_token
        }

        ticket_url = f"{GLPI_URL}/apirest.php/Ticket"
        payload = {
            "input": {
                "name": intent["title"],
                "content": f"Usuário relatou: {request.texto}",
                "itilcategories_id": intent["category_id"],
                "type": 1,
                "status": 1
            }
        }

        ticket_response = requests.post(ticket_url, json=payload, headers=headers, timeout=10)

        # Encerrar sessão
        requests.get(f"{GLPI_URL}/apirest.php/killSession", headers=headers)

        try:
            return ticket_response.json()
        except Exception:
            return {"status_code": ticket_response.status_code, "text": ticket_response.text}
    except Exception as e:
        logger.error(f"Erro ao criar chamado: {str(e)}")
        return {"error": str(e)}

@app.post("/create-ticket/")
def create_ticket(request: TicketRequest):
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

# Endpoints de teste
@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/test-env")
def test_env():
    return {
        "GLPI_URL": GLPI_URL,
        "GLPI_APP_TOKEN": GLPI_APP_TOKEN[:5] + "*****" if GLPI_APP_TOKEN else None
    }

@app.get("/test-auth")
def test_auth():
    try:
        session_token = iniciar_sessao()
        return {"success": True, "session_token": session_token[:8] + "*****"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/test-classify")
def test_classify(texto: str):
    try:
        intent = classify_intent(texto)
        return {"texto": texto, "categoria": intent}
    except Exception as e:
        return {"error": str(e)}

@app.get("/test-direct-ticket")
def test_direct_ticket(texto: str):
    try:
        intent = classify_intent(texto)
        session_token = iniciar_sessao()

        headers = {
            "Content-Type": "application/json",
            "App-Token": GLPI_APP_TOKEN,
            "Session-Token": session_token
        }

        ticket_url = f"{GLPI_URL}/apirest.php/Ticket"
        payload = {
            "input": {
                "name": intent["title"],
                "content": f"Usuário relatou: {texto}",
                "itilcategories_id": intent["category_id"],
                "type": 1,
                "status": 1
            }
        }

        ticket_response = requests.post(ticket_url, json=payload, headers=headers, timeout=10)

        # Encerra sessão
        requests.get(f"{GLPI_URL}/apirest.php/killSession", headers=headers)

        try:
            return ticket_response.json()
        except Exception:
            return {"status_code": ticket_response.status_code, "text": ticket_response.text}
    except Exception as e:
        return {"error": str(e)}

@app.get("/test-glpi-connection")
def test_glpi_connection():
    try:
        response = requests.get(GLPI_URL, timeout=5)
        return {"success": response.status_code == 200, "status_code": response.status_code}
    except Exception as e:
        return {"error": str(e)}

@app.get("/test-glpi-api")
def test_glpi_api():
    try:
        api_url = f"{GLPI_URL}/apirest.php"
        response = requests.get(api_url, timeout=5)
        return {"success": response.status_code == 200, "status_code": response.status_code}
    except Exception as e:
        return {"error": str(e)}

@app.get("/test-init-session")
def test_init_session():
    try:
        session_token = iniciar_sessao()
        return {"success": True, "session_token": session_token[:8] + "*****" if session_token else None}
    except Exception as e:
        return {"error": str(e)}