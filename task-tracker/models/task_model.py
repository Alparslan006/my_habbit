class Task:
    def __init__(self, description, status='bekliyor'):
        self.description = description
        self.status = status  # 'bekliyor' veya 'tamamlandı'

    def to_dict(self):
        return {
            'gorev': self.description,
            'durum': self.status
        }
