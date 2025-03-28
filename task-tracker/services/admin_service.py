class AdminService:
    def __init__(self):
        self.modules = {
            "task_module": True,
            "score_module": True,
            "excel_creator": True
        }

    def get_all_modules(self):
        return [{"name": k, "active": v} for k, v in self.modules.items()]

    def update_module_statuses(self, selected_names):
        for name in self.modules:
            self.modules[name] = name in selected_names

    def is_admin(self, username):
        return username == "admin"  # daha gelişmiş kontrol auth_service’te var
