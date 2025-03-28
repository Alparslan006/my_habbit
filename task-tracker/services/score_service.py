from repositories.score_repository import ScoreRepository
from services.task_service import TaskService
from models.score_model import Score

class ScoreService:
    def __init__(self):
        self.repo = ScoreRepository()
        self.task_service = TaskService()

    def calculate_and_store_score(self, username, date):
        tasks = self.task_service.get_tasks_for_user(username, date)
        total = len(tasks)
        completed = len([t for t in tasks if t.status == "tamamlandı"])
        missing = total - completed

        if missing == 0:
            point = 5
        elif missing == 1:
            point = 3
        elif missing == 2:
            point = 0
        elif missing == 3:
            point = -2
        else:
            point = -5

        score = Score(username, date, point)
        self.repo.save_score(score)
