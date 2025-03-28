from services.sheet_service import GoogleSheetService
from models.score_model import Score
import json

class ScoreRepository:
    def __init__(self):
        self.sheet_service = GoogleSheetService()
        self.score_sheet = "Puan"
        self.score_file = "score.json"

    def save_score(self, score: Score):
        self.sheet_service.append_row(self.score_sheet, list(score.to_dict().values()))
        self._save_to_file(score)

    def _save_to_file(self, score: Score):
        try:
            with open(self.score_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        data.append(score.to_dict())

        with open(self.score_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
