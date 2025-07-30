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
        
        # Configura os headers básicos
        self.headers = {
            'Content-Type': 'application/json',
            'App-Token': self.glpi_app_token
        }
        
        # Valida se tem credenciais suficientes para autenticação
        if not (self.glpi_user and self.glpi_password and self.glpi_app_token):
            raise Exception("ERROR_LOGIN_PARAMETERS_MISSING: É necessário fornecer usuário, senha e app_token")


    def authenticate(self):
        """
        Autentica na API do GLPI e armazena o session_token.
        A autenticação pode ser feita via user_token ou basic auth (usuário e senha).
        """
        try:
            import base64
            url = f"{self.glpi_url}/apirest.php/initSession"
            auth_headers = self.headers.copy()
            
            # Configura a autenticação
            # Autenticação básica (usuário e senha)
            credentials = f"{self.glpi_user}:{self.glpi_password}"
            auth_string = base64.b64encode(credentials.encode()).decode()
            auth_headers['Authorization'] = f"Basic {auth_string}"
            print("Usando autenticação básica")
            
            response = requests.get(url, headers=auth_headers)
            print("Resposta do GLPI:", response.text)  # Ajuda na depuração
            
            if response.status_code == 200:
                data = response.json()
                self.session_token = data.get('session_token')
                if self.session_token:
                    self.headers['Session-Token'] = self.session_token
                    print('Autenticação GLPI realizada com sucesso!')
                    return True
                else:
                    print('Erro: session_token não encontrado na resposta')
            else:
                print(f'Erro na autenticação. Status code: {response.status_code}')
                print(f'Resposta: {response.text}')
            
            return False
        except Exception as e:
            print(f'Erro na autenticação GLPI: {e}')
            return False

    def create_ticket(self, title, description, requester_email):
        """
        Cria um chamado no GLPI com os dados fornecidos.
        Retorna o ID do ticket criado ou None em caso de erro.
        """
        if not self.session_token:
            print('Erro: Sessão não autenticada. Execute authenticate() primeiro.')
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
            
            print(f"Criando ticket com payload: {payload}")
            print(f"Headers utilizados: {self.headers}")
            
            response = requests.post(url, json=payload, headers=self.headers)
            print(f"Status code: {response.status_code}")
            print(f"Resposta do GLPI: {response.text}")
            
            if response.status_code == 201:
                data = response.json()
                ticket_id = data.get('id')
                if ticket_id:
                    print(f'Ticket criado com sucesso! ID: {ticket_id}')
                    return ticket_id
                else:
                    print('Erro: ID do ticket não encontrado na resposta')
            else:
                print(f'Erro ao criar ticket. Status code: {response.status_code}')
                print(f'Resposta de erro: {response.text}')
            
            return None
        except Exception as e:
            print(f'Erro ao criar ticket: {str(e)}')
            return None

    def logout(self):
        """
        Encerra a sessão autenticada no GLPI.
        Retorna True se a sessão foi encerrada com sucesso, False caso contrário.
        """
        if not self.session_token:
            print('Aviso: Nenhuma sessão ativa para encerrar.')
            return False

        try:
            url = f"{self.glpi_url}/apirest.php/killSession"
            print(f"Encerrando sessão com token: {self.session_token}")
            print(f"Headers utilizados: {self.headers}")
            
            response = requests.get(url, headers=self.headers)
            print(f"Status code: {response.status_code}")
            print(f"Resposta do GLPI: {response.text}")
            
            if response.status_code == 200:
                self.session_token = None
                self.headers.pop('Session-Token', None)
                print('Sessão encerrada com sucesso!')
                return True
            else:
                print(f'Erro ao encerrar sessão. Status code: {response.status_code}')
                print(f'Resposta de erro: {response.text}')
                return False
    except Exception as e:
        print(f'Erro ao encerrar sessão: {str(e)}')
        return False