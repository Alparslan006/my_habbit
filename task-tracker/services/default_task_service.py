class DefaultTaskService:
    def __init__(self, sheet_service):
        self.sheet_service = sheet_service
        self.sheet_name = "VarsayilanGorevler"

    def get_default_tasks(self):
        try:
            worksheet = self.sheet_service.sheet.worksheet(self.sheet_name)
            rows = worksheet.col_values(1)
            return [r.strip() for r in rows if r.strip().lower() != "gorev" and r.strip() != ""]
        except Exception as e:
            print("Varsayılan görevler alınamadı:", e)
            return []

    def add_task(self, description):
        worksheet = self.sheet_service.sheet.worksheet(self.sheet_name)
        worksheet.append_row([description])

    def delete_task(self, description):
        worksheet = self.sheet_service.sheet.worksheet(self.sheet_name)
        rows = worksheet.col_values(1)
        for i, row in enumerate(rows):
            if row.strip().lower() == description.strip().lower():
                worksheet.delete_rows(i + 1)
                break
