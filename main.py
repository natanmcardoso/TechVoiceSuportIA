from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from glpi_api import GLPIClient
from google_sheets import log_ticket_to_sheets

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

@app.post("/create-ticket/")
def create_ticket(request: TicketRequest):
    """
    Endpoint para criar um chamado no GLPI e registrar no Google Sheets.
    Recebe os dados do chamado, autentica no GLPI, cria o chamado e registra na planilha.
    """
    glpi = GLPIClient()
    glpi.authenticate()
    if not glpi.session_token:
        raise HTTPException(status_code=500, detail="Falha na autenticação com o GLPI.")
    ticket_id = glpi.create_ticket(request.title, request.description, request.requester_email)
    if not ticket_id:
        glpi.logout()
        raise HTTPException(status_code=500, detail="Falha ao criar o chamado no GLPI.")
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Registra o chamado na planilha Google Sheets
        log_ticket_to_sheets(ticket_id, request.title, request.description, timestamp)
    except Exception as e:
        glpi.logout()
        raise HTTPException(status_code=500, detail=f"Chamado criado, mas falha ao registrar no Google Sheets: {e}")
    glpi.logout()
    return {"message": "Chamado criado com sucesso!", "ticket_id": ticket_id}

@app.get("/health")
def health_check():
    """
    Endpoint de verificação de saúde da API.
    Retorna status ok se a API estiver rodando.
    """
    return {"status": "ok"} 