from flask import Blueprint
from controllers.auth_controller import login, logout

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login_route():
    return login()

@auth_bp.route("/logout", methods=["POST"])
def logout_route():
    return logout()
