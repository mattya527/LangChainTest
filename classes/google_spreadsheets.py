import os.path
import gspread
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

class GoogleSpreadsheets:
  def __init__(self,spreadsheet_id):
    self.creds = None
    self.credentials_path = "/workspace/LangChain/classes/credentials.json"
    self.client = None
    self.spreadsheet_id = spreadsheet_id

  def authorize(self):
    # 認証情報の読み込み
    self.creds = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_path, SCOPES)
    self.client = gspread.authorize(self.creds)
    # スプレッドシートのアクセス
    self.sheet = self.client.open_by_key(self.spreadsheet_id).sheet1 

  def write_data(self, row, col, data):
    # データの書き込み
    self.sheet.update_cell(row, col, data)  # 1行1列に書き込み

  def read_data(self):
    # データの読み込み
    result = self.sheet.get_all_records()
    return result

  def update_data(self, row, col, data):
    # データの更新
    self.sheet.update_cell(row, col, data)

  def delete_data(self, row, col):
    # データの削除
    self.sheet.update_cell(row, col, "")

  def append_data(self, data):
    # データの追加
    self.sheet.append_row(data)

  def clear_data(self):
    # データのクリア
    self.sheet.clear()

  def get_sheet(self):
    return self.sheet

  def get_client(self):
    return self.client

  def get_creds(self):
    return self.creds

  def get_credentials_path(self):
    return self.credentials_path

  def set_sheet(self, sheet):
    self.sheet = sheet

  def set_client(self, client):
    self.client = client

  def set_creds(self, creds):
    self.creds = creds

  def set_credentials_path(self, credentials_path):
    self.credentials_path = credentials_path
      
if __name__ == "__main__":
  SPREADSHEET_ID = "1gbYwErukpa7aCTs3kTMPDaloQ3Cd-KOrf4nTNiXh1Q8"
  spreadsheet1 = GoogleSpreadsheets(SPREADSHEET_ID)
  spreadsheet1.authorize()
  spreadsheet1.write_data(3, 1, "Hello, World!")
  