from flask import Blueprint
from controllers.task_controller import show_dashboard, add_task, complete_task

task_bp = Blueprint("task", __name__)

@task_bp.route("/dashboard")
def dashboard():
    return show_dashboard()

@task_bp.route("/add", methods=["POST"])
def add():
    return add_task()

@task_bp.route("/complete/<int:index>", methods=["POST"])
def complete(index):
    return complete_task(index)
