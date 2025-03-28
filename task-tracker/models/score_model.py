class Score:
    def __init__(self, username, date, point):
        self.username = username
        self.date = date
        self.point = point

    def to_dict(self):
        return {
            'kullanici': self.username,
            'tarih': self.date,
            'puan': self.point
        }
