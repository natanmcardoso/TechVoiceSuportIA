from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from glpi_api import GLPIClient
import requests
import os
import base64
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

GLPI_URL = os.getenv('GLPI_URL')
GLPI_APP_TOKEN = os.getenv('GLPI_APP_TOKEN')
GLPI_USER_TOKEN = os.getenv('GLPI_USER_TOKEN')

app = FastAPI(title="Suporte.AI API")

class TicketRequest(BaseModel):
    title: str
    description: str
    requester_email: str

class ChamadoRequest(BaseModel):
    texto: str

# --- Mapeamento de categorias ---
CATEGORIAS = {
    "infraestrutura": {"category_id": 1, "title": "Infraestrutura"},
    "infraestrutura backup": {"category_id": 2, "title": "Infraestrutura > Backup"},
    "infraestrutura backup agendamento": {"category_id": 3, "title": "Infraestrutura > Backup > Agendamento"},
    # (restante das categorias aqui, igual ao seu código atual)
}

def classify_intent(texto: str):
    texto = texto.lower()
    for key, value in sorted(CATEGORIAS.items(), key=lambda x: x[0].count(' '), reverse=True):
        if all(word in texto for word in key.split()):
            return value
    return CATEGORIAS.get("infraestrutura", {"category_id": 1, "title": "Infraestrutura"})

# --- Novo método para iniciar sessão com user_token ---
def iniciar_sessao():
    url = f"{GLPI_URL}/apirest.php/initSession"
    headers = {
        "Content-Type": "application/json",
        "App-Token": GLPI_APP_TOKEN
    }
    payload = {"user_token": GLPI_USER_TOKEN}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get("session_token")
    else:
        raise HTTPException(status_code=400, detail=f"Erro ao iniciar sessão: {response.text}")

# --- Endpoint para criar chamado baseado em texto ---
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

        ticket_response = requests.post(ticket_url, json=payload, headers=headers)

        # Encerrar sessão
        requests.get(f"{GLPI_URL}/apirest.php/killSession", headers=headers)

        try:
            return ticket_response.json()
        except Exception:
            return {"status_code": ticket_response.status_code, "text": ticket_response.text}
    except Exception as e:
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
    """
    Testa autenticação via user_token (POST).
    """
    try:
        url = f"{GLPI_URL}/apirest.php/initSession"
        headers = {
            "Content-Type": "application/json",
            "App-Token": GLPI_APP_TOKEN
        }
        payload = {"user_token": GLPI_USER_TOKEN}
        response = requests.post(url, json=payload, headers=headers)
        return {
            "status_code": response.status_code,
            "response": response.json() if response.status_code == 200 else response.text
        }
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
    """
    Cria ticket diretamente sem GLPIClient, usando POST com user_token.
    """
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

        ticket_response = requests.post(ticket_url, json=payload, headers=headers)

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
    """
    Apenas chama iniciar_sessao() e retorna resultado.
    """
    try:
        session_token = iniciar_sessao()
        return {"success": True, "session_token": session_token[:8] + "*****" if session_token else None}
    except Exception as e:
        return {"error": str(e)}
