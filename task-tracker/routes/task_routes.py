from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from services.sheet_service import GoogleSheetService
from services.sheets_service import UserPermissionService

task_bp = Blueprint('task_bp', __name__)
sheet_service = GoogleSheetService()
permission_service = UserPermissionService()

@task_bp.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('auth_bp.login'))
    
    username = session['username']
    role = session.get('role', 'user')  # Session'dan role'ü al, yoksa 'user' varsayılanını kullan
    tasks = sheet_service.get_tasks()
    
    return render_template('dashboard.html', 
                         user=username,
                         role=role,
                         tasks=tasks)

@task_bp.route('/complete/<int:index>', methods=['POST'])
def complete(index):
    try:
        sheet_service.complete_task(index)
        flash('Görev başarıyla tamamlandı!', 'success')
    except Exception as e:
        flash(f'Görev tamamlanırken hata: {str(e)}', 'error')
    return redirect(url_for('task_bp.dashboard'))

@task_bp.route('/add', methods=['POST'])
def add():
    new_task = request.form.get('new_task')
    if new_task:
        try:
            sheet_service.add_task(new_task)
            flash('Yeni görev başarıyla eklendi!', 'success')
        except Exception as e:
            flash(f'Görev eklenirken hata: {str(e)}', 'error')
    return redirect(url_for('task_bp.dashboard'))
