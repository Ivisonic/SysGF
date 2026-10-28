import json
import os
from flask import Flask, jsonify, render_template, request
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
]

# Nome exato da sua planilha no Google Drive
SPREADSHEET_NAME = 'DB_FROTA'

SHEETS = [
    'veiculos',
    'setor',
    'hcarros',
    'revprevent',
    'proprietarios',
    'condutores',
    'oficinas',
]


def get_gspread_client():
  # Tenta ler das Variáveis de Ambiente (Render/Produção)
  creds_json_str = os.getenv('GOOGLE_CREDENTIALS_JSON')

  if creds_json_str:
    creds_info = json.loads(creds_json_str)
    creds = Credentials.from_service_account_info(
        creds_info, scopes=SCOPES
    )
  elif os.path.exists('credentials.json'):
    # Fallback para desenvolvimento local
    creds = Credentials.from_service_account_file(
        'credentials.json', scopes=SCOPES
    )
  else:
    raise Exception('Nenhuma credencial do Google encontrada!')

  return gspread.authorize(creds)