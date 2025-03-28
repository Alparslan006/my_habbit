class User:
    def __init__(self, username, password, is_admin=False):
        self.username = username
        self.password = password
        self.is_admin = is_admin

    def to_dict(self):
        return {
            'kullanici_adi': self.username,
            'sifre': self.password,
            'admin_mi': self.is_admin
        }
