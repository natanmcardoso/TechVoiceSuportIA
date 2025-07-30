from fastapi import FastAPI
import requests
import os
import base64
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

app = FastAPI()
GLPI_URL = os.getenv("GLPI_URL")
GLPI_APP_TOKEN = os.getenv("GLPI_APP_TOKEN")

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
    texto = texto.lower()
    for key, value in sorted(CATEGORIAS.items(), key=lambda x: x[0].count(' '), reverse=True):
        if any(word in texto for word in key.split()):
            return value
    return CATEGORIAS.get("infraestrutura", {"category_id": 1, "title": "Infraestrutura"})

@app.post("/chamado")
async def create_chamado(texto: str):
    try:
        intent = classify_intent(texto)
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
        payload = {
            "input": {
                "name": intent["title"],
                "content": f"Usuário relatou: {texto}",
                "itilcategories_id": intent["category_id"],
                "type": 1,  # Incidente
                "status": 1  # Novo
            }
        }
        response = requests.post(f"{GLPI_URL}/apirest.php/Ticket", json=payload, headers=headers)
        
        # Encerrar a sessão
        kill_session_url = f"{GLPI_URL}/apirest.php/killSession"
        requests.get(kill_session_url, headers=headers)
        
        try:
            response_json = response.json()
            return response_json
        except ValueError:
            return {
                "error": "Erro ao decodificar resposta do GLPI. Veja o campo 'text' para detalhes.",
                "status_code": response.status_code,
                "text": response.text
            }
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "status_code": response.status_code if 'response' in locals() else None, "text": response.text if 'response' in locals() else ""}
    except Exception as e:
        return {"error": str(e), "status_code": None, "text": ""}
