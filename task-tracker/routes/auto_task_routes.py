from flask import Blueprint
from controllers.auto_task_controller import show_new_day_form, create_new_day_tasks

auto_task_bp = Blueprint("auto_task", __name__)

@auto_task_bp.route("/newday")
def new_day_form():
    return show_new_day_form()

@auto_task_bp.route("/newday/create", methods=["POST"])
def create_tasks():
    return create_new_day_tasks()
