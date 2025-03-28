from google.oauth2 import service_account
from googleapiclient.discovery import build
import json

class UserPermissionService:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self.SPREADSHEET_ID = '14A2ELiC3KY8TrRe7vnKOX-iGWkQT4cL6slkoasiW2Zw'  # .env'den alınabilir
        self.credentials = service_account.Credentials.from_service_account_file(
            'credentials.json', scopes=self.SCOPES)
        self.service = build('sheets', 'v4', credentials=self.credentials)
        self.sheet = self.service.spreadsheets()

    def get_user_module_permissions(self, username):
        """
        Kullanıcının modül izinlerini Google Sheets'ten alır
        Örnek sheet yapısı:
        | username | module_1 | module_2 | module_3 | module_4 | module_5 |
        |----------|----------|----------|----------|----------|----------|
        | alparslan| true     | true     | false    | true     | false    |
        """
        try:
            # Kullanıcı izinleri sayfasını oku
            result = self.sheet.values().get(
                spreadsheetId=self.SPREADSHEET_ID,
                range='ModulePermissions!A:Z'  # Tüm sütunları al
            ).execute()
            
            values = result.get('values', [])
            if not values:
                return {}

            # Başlık satırını al
            headers = values[0]
            module_indices = {header: idx for idx, header in enumerate(headers)}

            # Kullanıcıyı bul
            for row in values[1:]:  # İlk satır başlık olduğu için atla
                if row[0] == username:  # İlk sütun username
                    permissions = {}
                    for module_id in [col for col in headers if col.startswith('module_')]:
                        idx = module_indices[module_id]
                        if idx < len(row):
                            permissions[module_id] = row[idx].lower() == 'true'
                        else:
                            permissions[module_id] = False
                    return permissions

            return {}  # Kullanıcı bulunamadıysa boş dict döndür

        except Exception as e:
            print(f"Sheets API Error: {e}")
            return {}

    def update_user_module_permissions(self, username, permissions):
        """
        Kullanıcının modül izinlerini Google Sheets'e kaydeder
        permissions = {
            'module_1': True,
            'module_2': False,
            ...
        }
        """
        try:
            # Önce mevcut verileri al
            result = self.sheet.values().get(
                spreadsheetId=self.SPREADSHEET_ID,
                range='ModulePermissions!A:Z'
            ).execute()
            
            values = result.get('values', [])
            if not values:
                return False

            headers = values[0]
            module_indices = {header: idx for idx, header in enumerate(headers)}
            
            # Kullanıcının satırını bul veya yeni satır oluştur
            user_row_idx = None
            for idx, row in enumerate(values[1:], 1):
                if row[0] == username:
                    user_row_idx = idx
                    break

            # Yeni değerleri hazırla
            new_row = [''] * len(headers)
            new_row[0] = username
            for module_id, is_active in permissions.items():
                if module_id in module_indices:
                    new_row[module_indices[module_id]] = str(is_active).lower()

            if user_row_idx is not None:
                # Mevcut kullanıcıyı güncelle
                range_name = f'ModulePermissions!A{user_row_idx+1}'
                self.sheet.values().update(
                    spreadsheetId=self.SPREADSHEET_ID,
                    range=range_name,
                    valueInputOption='RAW',
                    body={'values': [new_row]}
                ).execute()
            else:
                # Yeni kullanıcı ekle
                self.sheet.values().append(
                    spreadsheetId=self.SPREADSHEET_ID,
                    range='ModulePermissions!A:A',
                    valueInputOption='RAW',
                    insertDataOption='INSERT_ROWS',
                    body={'values': [new_row]}
                ).execute()

            return True

        except Exception as e:
            print(f"Sheets API Error: {e}")
            return False

    def get_user_role(self, username):
        """
        Kullanıcının rolünü Google Sheets'ten alır
        """
        try:
            result = self.sheet.values().get(
                spreadsheetId=self.SPREADSHEET_ID,
                range='Users!A:B'  # A: username, B: role
            ).execute()
            
            values = result.get('values', [])
            if not values:
                return 'user'

            for row in values[1:]:  # İlk satır başlık
                if row[0] == username:
                    return row[1] if len(row) > 1 else 'user'

            return 'user'  # Kullanıcı bulunamadıysa varsayılan rol

        except Exception as e:
            print(f"Sheets API Error: {e}")
            return 'user' 