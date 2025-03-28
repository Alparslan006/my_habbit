from datetime import datetime, timedelta
from models.task_model import Task

class AutoTaskService:
    def __init__(self, auth_repo, task_service, default_task_service):
        self.auth_repo = auth_repo
        self.task_service = task_service
        self.default_task_service = default_task_service

    def create_tasks_for_tomorrow(self):
        users = self.auth_repo.get_all_users()
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        default_tasks = self.default_task_service.get_default_tasks()

        for user in users:
            username = user["username"]
            sheet_name = f"{username}_{tomorrow}"
            print(f"[AUTO] {sheet_name} oluşturuluyor...")

            self.task_service._create_if_not_exists(sheet_name)

            for desc in default_tasks:
                task = Task(desc)
                self.task_service.repo.add_task(sheet_name, task)
