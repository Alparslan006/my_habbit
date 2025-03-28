import gspread
from google.oauth2.service_account import Credentials
from config import SPREADSHEET_ID, SERVICE_ACCOUNT_FILE

class GoogleSheetService:
    def __init__(self):
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open_by_key(SPREADSHEET_ID)

    def get_sheet(self, name):
        try:
            return self.sheet.worksheet(name)
        except gspread.WorksheetNotFound:
            return None

    def create_daily_sheet(self, name, headers):
        if not self.get_sheet(name):
            self.sheet.add_worksheet(title=name, rows=100, cols=str(len(headers)))
            self.sheet.worksheet(name).append_row(headers)

    def read_all_rows(self, name):
        worksheet = self.get_sheet(name)
        if worksheet:
            return worksheet.get_all_records()
        return []

    def append_row(self, name, row_data):
        worksheet = self.get_sheet(name)
        if worksheet:
            worksheet.append_row(row_data)

    def update_cell(self, name, row, col, value):
        worksheet = self.get_sheet(name)
        if worksheet:
            worksheet.update_cell(row, col, value)

    def delete_sheet(self, name):
        worksheet = self.get_sheet(name)
        if worksheet:
            self.sheet.del_worksheet(worksheet)