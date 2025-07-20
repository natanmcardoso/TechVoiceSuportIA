import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
from datetime import datetime

def init_google_sheets():
    """
    Inicializa a conexão com o Google Sheets usando as credenciais da conta de serviço.
    Retorna o objeto da planilha (sheet) pronta para uso.
    """
    try:
        load_dotenv()
        creds_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH')
        sheet_id = os.getenv('GOOGLE_SHEET_ID')
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(sheet_id).sheet1
        print('Conexão com Google Sheets realizada com sucesso!')
        return sheet
    except Exception as e:
        print(f'Erro ao conectar ao Google Sheets: {e}')
        return None

def log_ticket_to_sheets(ticket_id, title, description, timestamp=None):
    """
    Adiciona uma nova linha na planilha do Google Sheets com os dados do chamado.
    ticket_id: ID do chamado criado no GLPI.
    title: Título do chamado.
    description: Descrição do chamado.
    timestamp: Data e hora do registro (opcional, usa o horário atual se não informado).
    """
    try:
        sheet = init_google_sheets()
        if not sheet:
            print('Planilha não disponível.')
            return
        if not timestamp:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        row = [str(ticket_id), title, description, timestamp]
        sheet.append_row(row)
        print('Ticket registrado na planilha com sucesso!')
    except Exception as e:
        print(f'Erro ao registrar ticket na planilha: {e}') 