from flask import Blueprint, render_template, redirect, url_for, request, session, flash, jsonify
from services.sheet_service import GoogleSheetService
from services.sheets_service import UserPermissionService
from datetime import datetime, timedelta

task_bp = Blueprint('task_bp', __name__)
sheet_service = GoogleSheetService()
permission_service = UserPermissionService()

@task_bp.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('auth_bp.login'))
    
    username = session['username']
    role = session.get('role', 'user')
    
    # Bugünün tarihi
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Bugünün görevlerini getir
    tasks = sheet_service.get_tasks(username, today)
    
    return render_template('dashboard.html', 
                         user=username,
                         role=role,
                         tasks=tasks,
                         current_date=today)

@task_bp.route('/check_reminders')
def check_reminders():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
    username = session['username']
    reminders = sheet_service.get_upcoming_reminders(username)
    return jsonify({'reminders': reminders})

@task_bp.route('/weekly')
def weekly_view():
    if 'username' not in session:
        return redirect(url_for('auth_bp.login'))
    
    username = session['username']
    start_date = request.args.get('start_date')
    
    if not start_date:
        # Varsayılan olarak bu haftanın başlangıcını al
        today = datetime.now()
        start_date = (today - timedelta(days=today.weekday())).strftime("%Y-%m-%d")
    
    # Başlangıç tarihinden itibaren 7 günlük görevleri al
    start = datetime.strptime(start_date, "%Y-%m-%d")
    weekly_tasks = {}
    
    for i in range(7):
        current_date = (start + timedelta(days=i)).strftime("%Y-%m-%d")
        tasks = sheet_service.get_tasks(username, current_date)
        if tasks:  # Sadece görev olan günleri göster
            weekly_tasks[current_date] = tasks
    
    return render_template('weekly_view.html',
                         user=username,
                         weekly_tasks=weekly_tasks,
                         start_date=start_date)

@task_bp.route('/complete/<int:index>', methods=['POST'])
def complete(index):
    if 'username' not in session:
        return redirect(url_for('auth_bp.login'))
    
    username = session['username']
    try:
        sheet_service.complete_task(username, index)
        flash('Görev başarıyla tamamlandı!', 'success')
    except Exception as e:
        flash(f'Görev tamamlanırken hata: {str(e)}', 'error')
    return redirect(url_for('task_bp.dashboard'))

@task_bp.route('/add', methods=['POST'])
def add():
    if 'username' not in session:
        return redirect(url_for('auth_bp.login'))
    
    username = session['username']
    new_task = request.form.get('new_task')
    reminder_time = request.form.get('reminder_time')
    
    if new_task:
        try:
            sheet_service.add_task(username, new_task, reminder_time)
            flash('Yeni görev başarıyla eklendi!', 'success')
        except Exception as e:
            flash(f'Görev eklenirken hata: {str(e)}', 'error')
    return redirect(url_for('task_bp.dashboard'))

@task_bp.route('/history')
def history():
    if 'username' not in session:
        return redirect(url_for('auth_bp.login'))
    
    username = session['username']
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    tasks = sheet_service.get_task_history(username, start_date, end_date)
    
    return render_template('task_history.html',
                         user=username,
                         tasks=tasks,
                         start_date=start_date,
                         end_date=end_date)
