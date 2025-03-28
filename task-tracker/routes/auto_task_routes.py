from flask import Blueprint, redirect, url_for, flash
from services.sheet_service import GoogleSheetService

auto_task_bp = Blueprint('auto_task_bp', __name__)
sheet_service = GoogleSheetService()

@auto_task_bp.route('/newday')
def new_day():
    try:
        sheet_service.create_new_day()
        flash('Yeni gün başarıyla oluşturuldu!', 'success')
    except Exception as e:
        flash(f'Yeni gün oluşturulurken hata: {str(e)}', 'error')
    
    return redirect(url_for('task_bp.dashboard'))
