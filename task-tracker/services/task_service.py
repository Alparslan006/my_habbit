from repositories.task_repository import TaskRepository
from models.task_model import Task
from datetime import datetime

class TaskService:
    def __init__(self):
        self.repo = TaskRepository()

    def get_tasks_for_user(self, username, date):
        sheet_name = f"{username}_{date}"
        return self.repo.get_tasks(sheet_name)

    def add_task(self, username, date, description):
        sheet_name = f"{username}_{date}"
        self._create_if_not_exists(sheet_name)
        task = Task(description)
        self.repo.add_task(sheet_name, task)

    def mark_task_complete(self, username, date, index):
        sheet_name = f"{username}_{date}"
        self.repo.update_task_status(sheet_name, index, "tamamlandı")

    def _create_if_not_exists(self, sheet_name):
        headers = ["gorev", "durum"]
        self.repo.sheet_service.create_daily_sheet(sheet_name, headers)
