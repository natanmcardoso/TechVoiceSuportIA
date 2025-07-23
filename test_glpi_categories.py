import os
import requests
from dotenv import load_dotenv

# =========================
# Configuração e Constantes
# =========================

# Carrega variáveis do arquivo .env
load_dotenv()
GLPI_URL = os.getenv('GLPI_URL')
GLPI_USER = os.getenv('GLPI_USER')
GLPI_PASSWORD = os.getenv('GLPI_PASSWORD')
GLPI_APP_TOKEN = os.getenv('GLPI_APP_TOKEN')
FASTAPI_URL = "https://techvoicesuportia.onrender.com/chamado"

# Comandos de teste para cada categoria
TEST_COMMANDS = {
    "infraestrutura": "Problema geral de infraestrutura",
    "infraestrutura backup": "Problema com backup",
    "infraestrutura backup agendamento": "Agendar um backup",
    "infraestrutura backup falha de backup": "O backup falhou",
    "infraestrutura backup restauração": "Preciso restaurar um backup",
    "infraestrutura computadores": "Meu computador não funciona",
    "infraestrutura computadores desktops": "Meu desktop não liga",
    "infraestrutura computadores formatação reinstalação": "Preciso formatar meu computador",
    "infraestrutura computadores notebooks": "Meu notebook está travando",
    "infraestrutura computadores upgrade manutenção": "Preciso de um upgrade no computador",
    "infraestrutura data center": "Problema no data center",
    "infraestrutura data center climatização": "O ar-condicionado do data center parou",
    "infraestrutura data center energia": "Falta de energia no data center",
    "infraestrutura data center racks": "Problema com rack no data center",
    "infraestrutura firewall security": "O firewall está bloqueando",
    "infraestrutura firewall security bloqueio de sites": "Não consigo acessar um site",
    "infraestrutura firewall security regras de acesso": "Configurar regras de firewall",
    "infraestrutura impressoras": "Impressora não imprime",
    "infraestrutura impressoras compartilhamento": "Não consigo compartilhar a impressora",
    "infraestrutura impressoras configuração": "Configurar minha impressora",
    "infraestrutura impressoras erro físico": "Impressora com papel preso",
    "infraestrutura impressoras falta de tinta toner": "Impressora sem toner",
    "infraestrutura periféricos": "Meu teclado não funciona",
    "infraestrutura periféricos monitor": "Meu monitor está piscando",
    "infraestrutura periféricos outros": "Problema com periférico",
    "infraestrutura periféricos outros dúvidas gerais": "Dúvida sobre como usar o scanner",
    "infraestrutura periféricos outros solicitações diversas": "Preciso de um novo periférico",
    "infraestrutura periféricos teclado mouse": "Meu mouse parou de funcionar",
    "infraestrutura rede": "Não consigo acessar a internet",
    "infraestrutura rede cabeada": "A rede cabeada não funciona",
    "infraestrutura rede lentidão": "A internet está lenta",
    "infraestrutura rede sem conexão": "Sem conexão de rede",
    "infraestrutura rede vpn": "A VPN não conecta",
    "infraestrutura rede wi-fi": "O Wi-Fi está desconectando",
    "infraestrutura servidores": "O servidor está fora do ar",
    "infraestrutura servidores backup de servidor": "Backup do servidor falhou",
    "infraestrutura servidores linux": "Problema no servidor Linux",
    "infraestrutura servidores virtualização": "A máquina virtual não inicia",
    "infraestrutura servidores windows": "Problema no servidor Windows",
    "infraestrutura software de infraestrutura": "Problema com software de infraestrutura",
    "infraestrutura software de infraestrutura antivírus": "O antivírus não atualiza",
    "infraestrutura software de infraestrutura ferramentas de monitoramento": "Ferramenta de monitoramento com erro",
    "infraestrutura software de infraestrutura licenciamento": "Problema com licença de software",
    "infraestrutura telefonia": "O telefone não funciona",
    "infraestrutura telefonia convencional": "Telefone fixo sem linha",
    "infraestrutura telefonia ip": "Telefone IP não conecta",
    "infraestrutura telefonia pabx": "Problema com o PABX"
}

# =========================
# Funções de Integração GLPI
# =========================

def autenticar():
    """
    Autentica na API do GLPI e retorna o session_token.
    """
    url = f"{GLPI_URL}/apirest.php/initSession"
    headers = {'App-Token': GLPI_APP_TOKEN} if GLPI_APP_TOKEN else {}
    params = {'login': GLPI_USER, 'password': GLPI_PASSWORD}
    if GLPI_APP_TOKEN:
        params['app_token'] = GLPI_APP_TOKEN
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    return resp.json()['session_token']

def get_tickets(session_token, category_id):
    """
    Busca chamados no GLPI para uma categoria específica.
    """
    url = f"{GLPI_URL}/apirest.php/Ticket"
    headers = {
        'Session-Token': session_token,
        'Content-Type': 'application/json'
    }
    if GLPI_APP_TOKEN:
        headers['App-Token'] = GLPI_APP_TOKEN
    params = {
        'app_token': GLPI_APP_TOKEN if GLPI_APP_TOKEN else '',
        'range': '0-10',  # Últimos 10 chamados
        'expand_dropdowns': 'true'
    }
    resp = requests.get(url, headers=headers, params=params)
    if resp.status_code == 200:
        return [ticket for ticket in resp.json() if ticket.get('itilcategories_id') == category_id]
    else:
        print(f"Erro ao obter chamados: {resp.status_code} - {resp.text}")
        return []

def logout(session_token):
    """
    Encerra a sessão autenticada no GLPI.
    """
    url = f"{GLPI_URL}/apirest.php/killSession"
    headers = {
        'Session-Token': session_token
    }
    if GLPI_APP_TOKEN:
        headers['App-Token'] = GLPI_APP_TOKEN
    params = {'app_token': GLPI_APP_TOKEN} if GLPI_APP_TOKEN else {}
    requests.get(url, headers=headers, params=params)

# =========================
# Fluxo Principal
# =========================

def main():
    """
    Testa todas as categorias enviando comandos ao FastAPI e verificando os chamados no GLPI.
    """
    print("Iniciando testes das categorias...")
    session_token = None
    try:
        # Autenticar no GLPI
        session_token = autenticar()
        
        # Enviar comandos de teste ao FastAPI
        for key, comando in TEST_COMMANDS.items():
            print(f"\nTestando: {key} (Comando: '{comando}')")
            payload = {"texto": comando}
            resp = requests.post(FASTAPI_URL, json=payload)
            if resp.status_code == 200:
                print(f"Requisição enviada com sucesso: {resp.json()}")
                # Verificar o chamado criado no GLPI
                category_id = CATEGORIAS[key]["category_id"]
                tickets = get_tickets(session_token, category_id)
                if tickets:
                    for ticket in tickets:
                        if comando in ticket.get('content', ''):
                            print(f"Chamado encontrado: ID {ticket['id']}, Categoria ID {ticket['itilcategories_id']}, Título: {ticket['name']}")
                            break
                    else:
                        print(f"Chamado não encontrado para o comando '{comando}' na categoria {key}")
                else:
                    print(f"Nenhum chamado encontrado para a categoria {key} (ID {category_id})")
            else:
                print(f"Erro ao enviar requisição: {resp.status_code} - {resp.text}")
    
    except Exception as e:
        print(f"Erro durante a execução: {e}")
    finally:
        if session_token:
            logout(session_token)
            print("\nSessão finalizada.")

if __name__ == "__main__":
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
    main()