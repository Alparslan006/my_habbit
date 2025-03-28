from flask import render_template, request, redirect, session, url_for
from datetime import datetime, timedelta
from models.task_model import Task
from services.task_service import TaskService
from services.sheet_service import GoogleSheetService
from services.default_task_service import DefaultTaskService

task_service = TaskService()
sheet_service = GoogleSheetService()
default_service = DefaultTaskService(sheet_service)

def show_new_day_form():
    username = session.get("username")
    if not username:
        return redirect(url_for("auth.login"))

    return render_template("new_day.html", username=username)

def create_new_day_tasks():
    username = session.get("username")
    if not username:
        return redirect(url_for("auth.login"))

    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    sheet_name = f"{username}_{tomorrow}"
    task_service._create_if_not_exists(sheet_name)

    # Kullanıcının formdan yazdığı görevler
    form_tasks = []
    for i in range(1, 11):
        desc = request.form.get(f"gorev{i}")
        if desc and desc.strip():
            form_tasks.append(desc.strip())

    # Sabit görevler
    default_tasks = default_service.get_default_tasks()

    # Birleştir, tekrarsız hale getir
    combined_tasks = list(set(form_tasks + default_tasks))

    for desc in combined_tasks:
        task = Task(desc)
        task_service.repo.add_task(sheet_name, task)

    return redirect(url_for("task.dashboard"))
