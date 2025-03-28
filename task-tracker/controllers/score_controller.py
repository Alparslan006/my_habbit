from flask import session, redirect
from services.score_service import ScoreService
from datetime import datetime

score_service = ScoreService()

def calculate_daily_score():
    if 'username' not in session:
        return redirect('/auth/login')

    today = datetime.now().strftime('%Y-%m-%d')
    score_service.calculate_and_store_score(session['username'], today)
    return redirect('/tasks/dashboard')
