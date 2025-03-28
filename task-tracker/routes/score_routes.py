from flask import Blueprint
from controllers.score_controller import calculate_daily_score

score_bp = Blueprint("score_bp", __name__)

@score_bp.route("/calculate", methods=["POST"])
def calculate_score():
    return calculate_daily_score()
