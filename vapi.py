from fastapi import FastAPI, HTTPException, Header
import requests
import os

app = FastAPI()

# Configurações GLPI
GLPI_URL = os.getenv("GLPI_URL", "http://18.228.89.89/apirest.php")
GLPI_APP_TOKEN = os.getenv("GLPI_APP_TOKEN")
GLPI_USER_TOKEN = os.getenv("GLPI_USER_TOKEN")

# Configurações VAPI
VAPI_API_KEY = os.getenv("VAPI_API_KEY")

# Validação inicial
if not GLPI_APP_TOKEN or not GLPI_USER_TOKEN:
    raise RuntimeError("GLPI_APP_TOKEN e GLPI_USER_TOKEN são obrigatórios.")

# Função para autenticar no GLPI
def get_glpi_session_token():
    headers = {"Content-Type": "application/json", "App-Token": GLPI_APP_TOKEN}
    payload = {"user_token": GLPI_USER_TOKEN}
    response = requests.post(f"{GLPI_URL}/initSession", json=payload, headers=headers)

    if response.status_code == 200:
        return response.json().get("session_token")
    raise HTTPException(status_code=401, detail=f"Falha na autenticação GLPI: {response.text}")

def close_glpi_session(session_token: str):
    headers = {"App-Token": GLPI_APP_TOKEN, "Session-Token": session_token}
    requests.get(f"{GLPI_URL}/killSession", headers=headers)

@app.post("/armazenar-infos")
async def armazenar_infos(data: dict, authorization: str = Header(None)):
    # Valida requisição da VAPI
    if authorization != f"Bearer {VAPI_API_KEY}":
        raise HTTPException(status_code=403, detail="Unauthorized")

    name = data.get("name")
    issue_description = data.get("issue_description")
    contact_email = data.get("contact_email", None)

    if not name or not issue_description:
        raise HTTPException(status_code=400, detail="Name e issue_description são obrigatórios.")

    ticket_description = f"Problema relatado por {name}\n"
    ticket_description += f"Problema: {issue_description}\n"
    if contact_email:
        ticket_description += f"E-mail de contato: {contact_email}"

    # Autentica no GLPI
    session_token = get_glpi_session_token()

    try:
        # Cria ticket
        ticket_payload = {
            "input": {
                "name": f"Problema Técnico - {name}",
                "content": ticket_description,
                "priority": 3,
                "entities_id": 0
            }
        }
        headers = {
            "Content-Type": "application/json",
            "Session-Token": session_token,
            "App-Token": GLPI_APP_TOKEN
        }
        response = requests.post(f"{GLPI_URL}/Ticket", json=ticket_payload, headers=headers)

        if response.status_code in [200, 201]:
            return {"status": "success", "ticket_id": response.json().get("id"), "collected_data": data}
        else:
            raise HTTPException(status_code=response.status_code, detail="Falha ao criar GLPI ticket")
    finally:
        close_glpi_session(session_token)

@app.post("/criar-chamado-glpi")
async def criar_chamado_glpi(data: dict):
    issue_title = data.get("title", "Problema Técnico")
    issue_description = data.get("description", "Problema relatado via assistente de voz")
    priority = data.get("priority", 3)

    session_token = get_glpi_session_token()

    try:
        ticket_payload = {
            "input": {
                "name": issue_title,
                "content": issue_description,
                "priority": priority,
                "entities_id": 0
            }
        }
        headers = {
            "Content-Type": "application/json",
            "Session-Token": session_token,
            "App-Token": GLPI_APP_TOKEN
        }
        response = requests.post(f"{GLPI_URL}/Ticket", json=ticket_payload, headers=headers)

        if response.status_code in [200, 201]:
            return {"status": "success", "ticket_id": response.json().get("id")}
        else:
            raise HTTPException(status_code=response.status_code, detail="Falha ao criar GLPI ticket")
    finally:
        close_glpi_session(session_token)
