from repositories.auth_repository import AuthRepository

class AuthService:
    def __init__(self):
        from services.sheet_service import GoogleSheetService
        self.sheet_service = GoogleSheetService()
        self.sheet = self.sheet_service.sheet
        self.user_sheet = self.sheet.worksheet("Users")

    def authenticate(self, username, password):
        users = self.user_sheet.get_all_records()
        for user in users:
            if user["username"] == username and user["password"] == password:
                return True
        return False

    def is_admin(self, username):
        users = self.user_sheet.get_all_records()
        for user in users:
            if user["username"] == username:
                return user["role"].lower() == "admin"
        return False

    def get_user(self, username):  # 💥 BUNU EKLEDİK
        users = self.user_sheet.get_all_records()
        for user in users:
            if user["username"] == username:
                return user
        return None

