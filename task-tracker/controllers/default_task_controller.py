from flask import render_template, request, redirect, session, url_for
from services.sheet_service import GoogleSheetService
from services.default_task_service import DefaultTaskService

sheet_service = GoogleSheetService()
default_service = DefaultTaskService(sheet_service)

def list_default_tasks():
    username = session.get("username")
    if not username or session.get("role") != "admin":
        return redirect(url_for("auth.login_route"))
    
    tasks = default_service.get_default_tasks()
    print(tasks)  # Burada task'leri yazdırın
    return render_template("default_tasks.html", tasks=tasks)


def add_default_task():
    new_task = request.form.get("new_task")
    if new_task and new_task.strip():  # Eğer görevde boşluk yoksa
        default_service.add_task(new_task.strip())  # Boşlukları temizle
    return redirect(url_for("default_tasks.view"))  # Sayfayı yeniden yükleyerek güncellenmiş görevleri göster

def delete_default_task():
    task_to_delete = request.form.get("delete_task")
    if task_to_delete:
        default_service.delete_task(task_to_delete.strip())  # Boşlukları temizle
    return redirect(url_for("default_tasks.view"))  # Yine aynı sayfaya yönlendirme yaparak görevleri güncelle
