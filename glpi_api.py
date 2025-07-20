import os
import requests
from dotenv import load_dotenv

class GLPIClient:
    """
    Cliente para integração com a API REST do GLPI.
    Responsável por autenticar, criar chamados e encerrar sessões.
    """
    def __init__(self):
        """
        Inicializa o cliente GLPI carregando variáveis de ambiente e configurando headers.
        """
        load_dotenv()
        self.glpi_url = os.getenv('GLPI_URL')
        self.glpi_user = os.getenv('GLPI_USER')
        self.glpi_password = os.getenv('GLPI_PASSWORD')
        self.glpi_app_token = os.getenv('GLPI_APP_TOKEN')  # App Token da aplicação GLPI
        self.session_token = None
        self.headers = {
            'Content-Type': 'application/json',
            'App-Token': self.glpi_app_token  # Inclui o App Token no header
        }

    def authenticate(self):
        """
        Autentica na API do GLPI e armazena o session_token.
        """
        try:
            url = f"{self.glpi_url}/apirest.php/initSession"
            params = {
                'login': self.glpi_user,
                'password': self.glpi_password
            }
            response = requests.get(url, params=params, headers=self.headers)
            print("Resposta do GLPI:", response.text)  # Ajuda na depuração
            response.raise_for_status()
            data = response.json()
            self.session_token = data.get('session_token')
            if self.session_token:
                self.headers['Session-Token'] = self.session_token
                print('Autenticação GLPI realizada com sucesso!')
            else:
                print('Erro ao obter session_token do GLPI.')
        except Exception as e:
            print(f'Erro na autenticação GLPI: {e}')

    def create_ticket(self, title, description, requester_email):
        """
        Cria um chamado no GLPI com os dados fornecidos.
        Retorna o ID do ticket criado ou None em caso de erro.
        """
        if not self.session_token:
            print('Sessão não autenticada. Execute authenticate() primeiro.')
            return None
        try:
            url = f"{self.glpi_url}/apirest.php/Ticket"
            payload = {
                'input': {
                    'name': title,
                    'content': description,
                    'requester': [{
                        'name': requester_email
                    }]
                }
            }
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            ticket_id = data.get('id')
            if ticket_id:
                print(f'Ticket criado com sucesso! ID: {ticket_id}')
                return ticket_id
            else:
                print('Erro ao criar ticket no GLPI.')
                return None
        except Exception as e:
            print(f'Erro ao criar ticket: {e}')
            return None

    def logout(self):
        """
        Encerra a sessão autenticada no GLPI.
        """
        if not self.session_token:
            print('Nenhuma sessão ativa para encerrar.')
            return
        try:
            url = f"{self.glpi_url}/apirest.php/killSession"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            print('Logout realizado com sucesso!')
            self.session_token = None
            self.headers.pop('Session-Token', None)
        except Exception as e:
            print(f'Erro ao encerrar sessão: {e}') 