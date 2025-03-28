from flask import render_template, request, redirect, session, url_for
from datetime import datetime
from services.task_service import TaskService

task_service = TaskService()

def show_dashboard():
    username = session.get("username")
    if not username:
        return redirect(url_for("login"))

    today = datetime.now().strftime("%Y-%m-%d")
    tasks = task_service.get_tasks_for_user(username, today)
    return render_template("dashboard.html", username=username, tasks=tasks)

def add_task():
    username = session.get("username")
    if not username:
        return redirect(url_for("login"))

    description = request.form.get("description")
    today = datetime.now().strftime("%Y-%m-%d")
    task_service.add_task(username, today, description)
    return redirect(url_for("task.dashboard"))

def complete_task(index):
    username = session.get("username")
    if not username:
        return redirect(url_for("login"))

    today = datetime.now().strftime("%Y-%m-%d")
    task_service.mark_task_complete(username, today, index)
    return redirect(url_for("task.dashboard"))
