from flask import session
from services.sheets_service import UserPermissionService

class AdminService:
    def __init__(self):
        self.sheets_service = UserPermissionService()
        self.module_definitions = {
            "module_1": "Görev Yönetimi",
            "module_2": "Puan Sistemi",
            "module_3": "Otomatik Görevler",
            "module_4": "Excel Raporları",
            "module_5": "Analiz Paneli"
            # Yeni modüller buraya eklenebilir
        }

    def get_all_modules(self):
        """Tüm modülleri ve kullanıcının erişim durumlarını getirir"""
        if 'username' not in session:
            return []

        username = session['username']
        user_permissions = self.sheets_service.get_user_module_permissions(username)
        
        modules = []
        for module_id, module_name in self.module_definitions.items():
            modules.append({
                "id": module_id,
                "name": module_name,
                "active": user_permissions.get(module_id, False)
            })
        return modules

    def update_module_statuses(self, selected_modules):
        """Kullanıcının modül erişimlerini günceller"""
        if 'username' not in session:
            return False

        username = session['username']
        permissions = {module_id: module_id in selected_modules 
                     for module_id in self.module_definitions.keys()}
        
        return self.sheets_service.update_user_module_permissions(username, permissions)

    def is_admin(self, username):
        """Kullanıcının admin olup olmadığını kontrol eder"""
        user_role = self.sheets_service.get_user_role(username)
        return user_role == "admin"

    def get_module_name(self, module_id):
        """Modül ID'sine göre modül adını döndürür"""
        return self.module_definitions.get(module_id, "Bilinmeyen Modül")
