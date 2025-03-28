import gspread
from config import SERVICE_ACCOUNT_FILE, SPREADSHEET_ID

class AuthRepository:
    def __init__(self):
        client = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
        sheet = client.open_by_key(SPREADSHEET_ID)
        self.user_sheet = sheet.worksheet("Users")

    def get_user(self, username):
        records = self.user_sheet.get_all_records()
        for user in records:
            if user["username"] == username:
                return user
        return None
