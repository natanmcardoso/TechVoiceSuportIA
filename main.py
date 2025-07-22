from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from glpi_api import GLPIClient
import requests
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

GLPI_URL = os.getenv('GLPI_URL')
API_TOKEN = os.getenv('API_TOKEN')

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

# Mapeamento das categorias do GLPI (pode ser importado de um módulo, se preferir)
CATEGORIAS = {
    # ... (cole aqui o dicionário de categorias do chamado_api.py) ...
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
    intent = classify_intent(request.texto)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"user_token {API_TOKEN}"
    }
    payload = {
        "input": {
            "name": intent["title"],
            "content": f"Usuário relatou: {request.texto}",
            "itilcategories_id": intent["category_id"],
            "type": 1,  # Incidente
            "status": 1  # Novo
        }
    }
    response = requests.post(f"{GLPI_URL}/Ticket", json=payload, headers=headers)
    return response.json()

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