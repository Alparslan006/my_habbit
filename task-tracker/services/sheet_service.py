import gspread
from google.oauth2.service_account import Credentials
from config import SPREADSHEET_ID, SERVICE_ACCOUNT_FILE
from datetime import datetime, timedelta

class GoogleSheetService:
    def __init__(self):
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open_by_key(SPREADSHEET_ID)
        
        # Görevler worksheet'ini kontrol et ve yoksa oluştur
        try:
            self.sheet.worksheet("Görevler")
        except gspread.WorksheetNotFound:
            worksheet = self.sheet.add_worksheet(title="Görevler", rows=100, cols=2)
            worksheet.append_row(["Görev", "Durum"])

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

    def _get_user_sheet(self, username):
        """Kullanıcının worksheet'ini getirir veya oluşturur"""
        sheet_name = f"Görevler_{username}"
        try:
            return self.sheet.worksheet(sheet_name)
        except gspread.WorksheetNotFound:
            worksheet = self.sheet.add_worksheet(title=sheet_name, rows=1000, cols=6)
            # Başlıkları ekle: Tarih | Görev | Durum | Tamamlanma Zamanı | Hatırlatma Saati | Hatırlatma Durumu
            worksheet.append_row(["Tarih", "Görev", "Durum", "Tamamlanma Zamanı", "Hatırlatma Saati", "Hatırlatma Durumu"])
            return worksheet

    def get_tasks(self, username, date=None):
        """Kullanıcının görevlerini getirir. 
        date parametresi verilirse o güne ait görevleri getirir."""
        try:
            worksheet = self._get_user_sheet(username)
            all_tasks = worksheet.get_all_records()
            
            if date:
                # Belirli güne ait görevleri filtrele
                tasks = [task for task in all_tasks if task["Tarih"] == date]
            else:
                # Bugünün görevlerini getir
                today = datetime.now().strftime("%Y-%m-%d")
                tasks = [task for task in all_tasks if task["Tarih"] == today]

            # Hatırlatma zamanını kontrol et
            now = datetime.now()
            for task in tasks:
                if task["Hatırlatma Saati"]:
                    task_time = datetime.strptime(f"{task['Tarih']} {task['Hatırlatma Saati']}", "%Y-%m-%d %H:%M")
                    task["hatirlatma_yakinda"] = now <= task_time <= (now + timedelta(minutes=30))
                else:
                    task["hatirlatma_yakinda"] = False
                
            return tasks
                
        except Exception as e:
            print(f"Görevler getirilirken hata: {str(e)}")
            return []

    def add_task(self, username, task, reminder_time=None):
        """Yeni görev ekler."""
        try:
            worksheet = self._get_user_sheet(username)
            today = datetime.now().strftime("%Y-%m-%d")
            reminder_status = "bekliyor" if reminder_time else "hatırlatma yok"
            worksheet.append_row([today, task, "beklemede", "", reminder_time or "", reminder_status])
        except Exception as e:
            raise Exception(f"Görev eklenirken hata: {str(e)}")

    def complete_task(self, username, index):
        """Görevi tamamlandı olarak işaretler."""
        try:
            worksheet = self._get_user_sheet(username)
            completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # İndeks 0'dan başladığı için satır numarasına 2 ekliyoruz (1 başlık satırı + 1 indeks düzeltmesi)
            row = index + 2
            worksheet.update_cell(row, 3, "tamamlandı")  # Durum sütunu
            worksheet.update_cell(row, 4, completion_time)  # Tamamlanma zamanı sütunu
        except Exception as e:
            raise Exception(f"Görev tamamlanırken hata: {str(e)}")

    def create_new_day(self, username):
        """Kullanıcı için yeni bir gün başlatır."""
        try:
            worksheet = self._get_user_sheet(username)
            today = datetime.now().strftime("%Y-%m-%d")
            
            # Bugün için zaten görev var mı kontrol et
            tasks = self.get_tasks(username, today)
            if tasks:
                return False  # Bugün için görevler zaten mevcut
            
            # Varsayılan görevleri ekle
            default_tasks = [
                "Günlük toplantıya katıl",
                "E-postaları kontrol et",
                "Günlük raporu hazırla",
                "Takım arkadaşlarıyla iletişim kur"
            ]
            
            for task in default_tasks:
                worksheet.append_row([today, task, "beklemede", "", "", ""])
                
            return True
        except Exception as e:
            raise Exception(f"Yeni gün oluşturulurken hata: {str(e)}")

    def get_task_history(self, username, start_date=None, end_date=None):
        """Kullanıcının görev geçmişini getirir."""
        try:
            worksheet = self._get_user_sheet(username)
            all_tasks = worksheet.get_all_records()
            
            # Tarihe göre filtreleme
            if start_date and end_date:
                filtered_tasks = [task for task in all_tasks 
                                if start_date <= task["Tarih"] <= end_date]
            else:
                filtered_tasks = all_tasks

            # Tarihe göre grupla
            grouped_tasks = {}
            for task in filtered_tasks:
                date = task["Tarih"]
                if date not in grouped_tasks:
                    grouped_tasks[date] = []
                task["completed"] = task["Durum"] == "tamamlandı"
                grouped_tasks[date].append(task)

            # Tarihe göre sırala
            return dict(sorted(grouped_tasks.items(), reverse=True))
        except Exception as e:
            print(f"Görev geçmişi getirilirken hata: {str(e)}")
            return {}

    def update_reminder_status(self, username, index, status):
        """Hatırlatma durumunu günceller."""
        try:
            worksheet = self._get_user_sheet(username)
            row = index + 2  # Başlık satırı ve 0-tabanlı indeks düzeltmesi
            worksheet.update_cell(row, 6, status)  # 6. sütun: Hatırlatma Durumu
        except Exception as e:
            raise Exception(f"Hatırlatma durumu güncellenirken hata: {str(e)}")

    def get_upcoming_reminders(self, username):
        """Yaklaşan hatırlatmaları getirir (30 dakika içinde)"""
        try:
            worksheet = self._get_user_sheet(username)
            all_tasks = worksheet.get_all_records()
            now = datetime.now()
            today = now.strftime("%Y-%m-%d")
            
            upcoming_tasks = []
            for task in all_tasks:
                # Sadece bugünün görevlerini kontrol et
                if task["Tarih"] != today:
                    continue
                    
                # Tamamlanmış görevleri atla
                if task["Durum"] == "tamamlandı":
                    continue
                    
                if task["Hatırlatma Saati"]:
                    try:
                        task_time = datetime.strptime(f"{today} {task['Hatırlatma Saati']}", "%Y-%m-%d %H:%M")
                        time_diff = (task_time - now).total_seconds() / 60  # Dakika cinsinden fark
                        
                        # Eğer hatırlatma zamanı geçmediyse ve 30 dakika içindeyse
                        if -1 <= time_diff <= 30:
                            upcoming_tasks.append(task)
                    except ValueError:
                        continue  # Geçersiz saat formatı
            
            return upcoming_tasks
        except Exception as e:
            print(f"Yaklaşan hatırlatmalar getirilirken hata: {str(e)}")
            return []