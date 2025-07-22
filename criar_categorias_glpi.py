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

# =========================
# Árvore de Categorias para Suporte de Infraestrutura
# =========================
# Edite esta lista para adicionar/remover categorias e subcategorias.
# O campo 'itilcategories_id' deve ser o 'name' da categoria pai.
CATEGORIAS = [
    # Raiz
    {"name": "Infraestrutura", "completename": "Infraestrutura", "code": "INFRA", "comment": "Categoria raiz para suporte de infraestrutura", "level": 1},
    # Rede
    {"name": "Rede", "completename": "Rede", "code": "NET", "comment": "Problemas de rede", "level": 2, "itilcategories_id": "Infraestrutura"},
    {"name": "Wi-Fi", "completename": "Wi-Fi", "code": "NET-WIFI", "comment": "Problemas com Wi-Fi", "level": 3, "itilcategories_id": "Rede"},
    {"name": "Cabeada", "completename": "Cabeada", "code": "NET-CAB", "comment": "Rede cabeada", "level": 3, "itilcategories_id": "Rede"},
    {"name": "VPN", "completename": "VPN", "code": "NET-VPN", "comment": "Problemas com VPN", "level": 3, "itilcategories_id": "Rede"},
    {"name": "Lentidão", "completename": "Lentidão", "code": "NET-LENT", "comment": "Rede lenta", "level": 3, "itilcategories_id": "Rede"},
    {"name": "Sem Conexão", "completename": "Sem Conexão", "code": "NET-NOCON", "comment": "Sem conexão de rede", "level": 3, "itilcategories_id": "Rede"},
    # Servidores
    {"name": "Servidores", "completename": "Servidores", "code": "SRV", "comment": "Problemas com servidores", "level": 2, "itilcategories_id": "Infraestrutura"},
    {"name": "Windows", "completename": "Windows", "code": "SRV-WIN", "comment": "Servidor Windows", "level": 3, "itilcategories_id": "Servidores"},
    {"name": "Linux", "completename": "Linux", "code": "SRV-LIN", "comment": "Servidor Linux", "level": 3, "itilcategories_id": "Servidores"},
    {"name": "Virtualização", "completename": "Virtualização", "code": "SRV-VIRT", "comment": "Virtualização de servidores", "level": 3, "itilcategories_id": "Servidores"},
    {"name": "Backup de Servidor", "completename": "Backup de Servidor", "code": "SRV-BACKUP", "comment": "Backup de servidores", "level": 3, "itilcategories_id": "Servidores"},
    # Impressoras
    {"name": "Impressoras", "completename": "Impressoras", "code": "IMP", "comment": "Problemas com impressoras", "level": 2, "itilcategories_id": "Infraestrutura"},
    {"name": "Configuração", "completename": "Configuração de Impressora", "code": "IMP-CONF", "comment": "Configuração de impressoras", "level": 3, "itilcategories_id": "Impressoras"},
    {"name": "Erro Físico", "completename": "Erro Físico de Impressora", "code": "IMP-ERR", "comment": "Erro físico em impressora", "level": 3, "itilcategories_id": "Impressoras"},
    {"name": "Falta de Tinta/Toner", "completename": "Falta de Tinta/Toner", "code": "IMP-TINTA", "comment": "Falta de tinta ou toner", "level": 3, "itilcategories_id": "Impressoras"},
    {"name": "Compartilhamento", "completename": "Compartilhamento de Impressora", "code": "IMP-COMP", "comment": "Compartilhamento de impressora", "level": 3, "itilcategories_id": "Impressoras"},
    # Computadores
    {"name": "Computadores", "completename": "Computadores", "code": "PC", "comment": "Problemas com computadores", "level": 2, "itilcategories_id": "Infraestrutura"},
    {"name": "Desktops", "completename": "Desktops", "code": "PC-DESK", "comment": "Problemas com desktops", "level": 3, "itilcategories_id": "Computadores"},
    {"name": "Notebooks", "completename": "Notebooks", "code": "PC-NOTE", "comment": "Problemas com notebooks", "level": 3, "itilcategories_id": "Computadores"},
    {"name": "Formatação/Reinstalação", "completename": "Formatação/Reinstalação", "code": "PC-FORM", "comment": "Formatação ou reinstalação de sistema", "level": 3, "itilcategories_id": "Computadores"},
    {"name": "Upgrade/Manutenção", "completename": "Upgrade/Manutenção", "code": "PC-UPG", "comment": "Upgrade ou manutenção de hardware", "level": 3, "itilcategories_id": "Computadores"},
    # Periféricos
    {"name": "Periféricos", "completename": "Periféricos", "code": "PER", "comment": "Problemas com periféricos", "level": 2, "itilcategories_id": "Infraestrutura"},
    {"name": "Teclado/Mouse", "completename": "Teclado/Mouse", "code": "PER-TM", "comment": "Problemas com teclado ou mouse", "level": 3, "itilcategories_id": "Periféricos"},
    {"name": "Monitor", "completename": "Monitor", "code": "PER-MON", "comment": "Problemas com monitor", "level": 3, "itilcategories_id": "Periféricos"},
    {"name": "Outros", "completename": "Outros Periféricos", "code": "PER-OUT", "comment": "Outros periféricos", "level": 3, "itilcategories_id": "Periféricos"},
    # Telefonia
    {"name": "Telefonia", "completename": "Telefonia", "code": "TEL", "comment": "Problemas com telefonia", "level": 2, "itilcategories_id": "Infraestrutura"},
    {"name": "IP", "completename": "Telefonia IP", "code": "TEL-IP", "comment": "Telefonia IP", "level": 3, "itilcategories_id": "Telefonia"},
    {"name": "Convencional", "completename": "Telefonia Convencional", "code": "TEL-CONV", "comment": "Telefonia convencional", "level": 3, "itilcategories_id": "Telefonia"},
    {"name": "PABX", "completename": "PABX", "code": "TEL-PABX", "comment": "Problemas com PABX", "level": 3, "itilcategories_id": "Telefonia"},
    # Firewall/Security
    {"name": "Firewall/Security", "completename": "Firewall/Security", "code": "FW", "comment": "Problemas de firewall e segurança", "level": 2, "itilcategories_id": "Infraestrutura"},
    {"name": "Regras de Acesso", "completename": "Regras de Acesso", "code": "FW-REG", "comment": "Regras de acesso", "level": 3, "itilcategories_id": "Firewall/Security"},
    {"name": "Bloqueio de Sites", "completename": "Bloqueio de Sites", "code": "FW-BLOQ", "comment": "Bloqueio de sites", "level": 3, "itilcategories_id": "Firewall/Security"},
    {"name": "VPN", "completename": "VPN (Firewall)", "code": "FW-VPN", "comment": "VPN via firewall", "level": 3, "itilcategories_id": "Firewall/Security"},
    # Backup
    {"name": "Backup", "completename": "Backup", "code": "BKP", "comment": "Problemas com backup", "level": 2, "itilcategories_id": "Infraestrutura"},
    {"name": "Falha de Backup", "completename": "Falha de Backup", "code": "BKP-FAIL", "comment": "Falha ao realizar backup", "level": 3, "itilcategories_id": "Backup"},
    {"name": "Restauração", "completename": "Restauração de Backup", "code": "BKP-REST", "comment": "Restauração de backup", "level": 3, "itilcategories_id": "Backup"},
    {"name": "Agendamento", "completename": "Agendamento de Backup", "code": "BKP-AGEN", "comment": "Agendamento de backup", "level": 3, "itilcategories_id": "Backup"},
    # Data Center
    {"name": "Data Center", "completename": "Data Center", "code": "DC", "comment": "Problemas no data center", "level": 2, "itilcategories_id": "Infraestrutura"},
    {"name": "Energia", "completename": "Energia", "code": "DC-ENERG", "comment": "Problemas de energia", "level": 3, "itilcategories_id": "Data Center"},
    {"name": "Climatização", "completename": "Climatização", "code": "DC-CLIMA", "comment": "Problemas de climatização", "level": 3, "itilcategories_id": "Data Center"},
    {"name": "Racks", "completename": "Racks", "code": "DC-RACK", "comment": "Problemas com racks", "level": 3, "itilcategories_id": "Data Center"},
    # Software de Infraestrutura
    {"name": "Software de Infraestrutura", "completename": "Software de Infraestrutura", "code": "SOFT-INFRA", "comment": "Softwares essenciais de infraestrutura", "level": 2, "itilcategories_id": "Infraestrutura"},
    {"name": "Antivírus", "completename": "Antivírus", "code": "SOFT-AV", "comment": "Problemas com antivírus", "level": 3, "itilcategories_id": "Software de Infraestrutura"},
    {"name": "Ferramentas de Monitoramento", "completename": "Ferramentas de Monitoramento", "code": "SOFT-MON", "comment": "Ferramentas de monitoramento", "level": 3, "itilcategories_id": "Software de Infraestrutura"},
    {"name": "Licenciamento", "completename": "Licenciamento", "code": "SOFT-LIC", "comment": "Licenciamento de software", "level": 3, "itilcategories_id": "Software de Infraestrutura"},
    # Outros
    {"name": "Outros", "completename": "Outros", "code": "OUT", "comment": "Outros problemas de infraestrutura", "level": 2, "itilcategories_id": "Infraestrutura"},
    {"name": "Dúvidas Gerais", "completename": "Dúvidas Gerais", "code": "OUT-DUV", "comment": "Dúvidas gerais sobre infraestrutura", "level": 3, "itilcategories_id": "Outros"},
    {"name": "Solicitações Diversas", "completename": "Solicitações Diversas", "code": "OUT-SOL", "comment": "Solicitações diversas", "level": 3, "itilcategories_id": "Outros"},
]

# =========================
# Funções de Integração GLPI
# =========================

def autenticar():
    """
    Autentica na API do GLPI e retorna o session_token.
    """
    url = f"{GLPI_URL}/apirest.php/initSession"
    headers = {'App-Token': GLPI_APP_TOKEN}
    params = {'login': GLPI_USER, 'password': GLPI_PASSWORD, 'app_token': GLPI_APP_TOKEN}
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    data = resp.json()
    return data['session_token']

def get_existing_categories(session_token):
    """
    Busca todas as categorias existentes no GLPI.
    Retorna um dicionário: nome -> id
    """
    url = f"{GLPI_URL}/apirest.php/ITILCategory"
    headers = {
        'App-Token': GLPI_APP_TOKEN,
        'Session-Token': session_token
    }
    params = {'app_token': GLPI_APP_TOKEN}
    resp = requests.get(url, headers=headers, params=params)
    if resp.status_code == 200:
        # Retorna dict nome -> id
        return {cat['name']: cat['id'] for cat in resp.json() if 'name' in cat and 'id' in cat}
    else:
        print(f"Erro ao obter categorias: {resp.status_code} - {resp.text}")
        return {}

def criar_categoria(session_token, categoria, categorias_existentes):
    """
    Cria uma categoria no GLPI.
    Se a categoria for subcategoria, busca o id do pai pelo nome.
    """
    url = f"{GLPI_URL}/apirest.php/ITILCategory"
    headers = {
        'App-Token': GLPI_APP_TOKEN,
        'Session-Token': session_token,
        'Content-Type': 'application/json'
    }
    params = {'app_token': GLPI_APP_TOKEN}
    payload = {
        "input": {
            "name": categoria["name"],
            "completename": categoria["completename"],
            "comment": categoria["comment"],
            "level": categoria["level"],
            "is_active": 1
        }
    }
    # Adiciona categoria pai se existir
    if "itilcategories_id" in categoria:
        parent_name = categoria["itilcategories_id"]
        if parent_name in categorias_existentes:
            payload["input"]["itilcategories_id"] = categorias_existentes[parent_name]
        else:
            print(f"Categoria pai '{parent_name}' não encontrada. Criando categoria sem pai.")
    resp = requests.post(url, headers=headers, params=params, json=payload)
    if resp.status_code in [200, 201]:
        print(f"Categoria '{categoria['name']}' criada com sucesso. ID: {resp.json().get('id')}")
        return resp.json().get('id')
    elif resp.status_code == 400 and "already exists" in resp.text.lower():
        print(f"Categoria '{categoria['name']}' já existe. Pulando...")
    else:
        print(f"Erro ao criar categoria '{categoria['name']}': {resp.status_code} - {resp.text}")

def logout(session_token):
    """
    Encerra a sessão autenticada no GLPI.
    """
    url = f"{GLPI_URL}/apirest.php/killSession"
    headers = {
        'App-Token': GLPI_APP_TOKEN,
        'Session-Token': session_token
    }
    params = {'app_token': GLPI_APP_TOKEN}
    requests.get(url, headers=headers, params=params)

# =========================
# Fluxo Principal
# =========================

def main():
    """
    Fluxo principal do script:
    - Autentica no GLPI
    - Cria categorias e subcategorias conforme a lista
    - Garante que subcategorias referenciem o pai recém-criado
    - Encerra a sessão ao final
    """
    print("Iniciando sessão no GLPI...")
    session_token = None
    try:
        session_token = autenticar()
        categorias_existentes = get_existing_categories(session_token)
        for categoria in CATEGORIAS:
            if categoria["name"] not in categorias_existentes:
                nova_id = criar_categoria(session_token, categoria, categorias_existentes)
                # Atualiza o dicionário para que subcategorias criadas depois encontrem o pai recém-criado
                if nova_id:
                    categorias_existentes[categoria["name"]] = nova_id
            else:
                print(f"Categoria '{categoria['name']}' já existe. ID: {categorias_existentes[categoria['name']]}")
    except Exception as e:
        print(f"Erro durante a execução: {e}")
    finally:
        if session_token:
            logout(session_token)
            print("Sessão finalizada.")

if __name__ == "__main__":
    main() 