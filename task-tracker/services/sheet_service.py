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

    def create_new_day(self):
        """Yeni bir gün için görev listesi oluşturur."""
        try:
            # Mevcut görevleri temizle
            worksheet = self.sheet.worksheet("Görevler")
            worksheet.clear()
            
            # Başlıkları ekle
            worksheet.append_row(["Görev", "Durum"])
            
            # Varsayılan görevleri ekle
            default_tasks = [
                "Günlük toplantıya katıl",
                "E-postaları kontrol et",
                "Günlük raporu hazırla",
                "Takım arkadaşlarıyla iletişim kur"
            ]
            
            for task in default_tasks:
                worksheet.append_row([task, "beklemede"])
                
            return True
        except Exception as e:
            raise Exception(f"Yeni gün oluşturulurken hata: {str(e)}")

    def get_tasks(self):
        """Günlük görevleri getirir."""
        try:
            worksheet = self.sheet.worksheet("Görevler")
            tasks = worksheet.get_all_records()
            return tasks
        except Exception as e:
            print(f"Görevler getirilirken hata: {str(e)}")
            return []

    def complete_task(self, index):
        """Görevi tamamlandı olarak işaretler."""
        try:
            worksheet = self.sheet.worksheet("Görevler")
            # İndeks 0'dan başladığı için satır numarasına 2 ekliyoruz (1 başlık satırı + 1 indeks düzeltmesi)
            worksheet.update_cell(index + 2, 2, "tamamlandı")
        except Exception as e:
            raise Exception(f"Görev tamamlanırken hata: {str(e)}")

    def add_task(self, task):
        """Yeni görev ekler."""
        try:
            worksheet = self.sheet.worksheet("Görevler")
            worksheet.append_row([task, "beklemede"])
        except Exception as e:
            raise Exception(f"Görev eklenirken hata: {str(e)}")