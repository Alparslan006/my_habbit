from services.sheet_service import GoogleSheetService

class TaskRepository:
    def __init__(self):
        self.sheet_service = GoogleSheetService()

    def get_tasks(self, sheet_name):
        try:
            worksheet = self.sheet_service.sheet.worksheet(sheet_name)
            rows = worksheet.get_all_records()
        except Exception as e:
            print(f"Sayfa bulunamadı: {sheet_name} → {e}")
            return []

        tasks = []
        for row in rows:
            gorev = row.get("gorev")
            durum = row.get("durum", "bekliyor")

            if gorev is not None and gorev.strip() != "":
                tasks.append({
                    "gorev": gorev.strip(),
                    "durum": durum.strip() if durum else "bekliyor"
                })

        return tasks

    def add_task(self, sheet_name, task):
        worksheet = self.sheet_service.sheet.worksheet(sheet_name)
        worksheet.append_row([task.description, "bekliyor"])

    def update_task_status(self, sheet_name, index, status):
        worksheet = self.sheet_service.sheet.worksheet(sheet_name)
        cell_row = index + 2  # başlıklar 1. satırda olduğu için +2
        worksheet.update_cell(cell_row, 2, status)
