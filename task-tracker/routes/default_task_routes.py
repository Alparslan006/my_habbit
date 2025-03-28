from flask import Blueprint
from controllers.default_task_controller import (
    list_default_tasks, add_default_task, delete_default_task
)

default_tasks_bp = Blueprint("default_tasks", __name__)

@default_tasks_bp.route("/default-tasks", methods=["GET"])
def view():
    return list_default_tasks()

@default_tasks_bp.route("/default-tasks/add", methods=["POST"])
def add():
    return add_default_task()

@default_tasks_bp.route("/default-tasks/delete", methods=["POST"])
def delete():
    return delete_default_task()
