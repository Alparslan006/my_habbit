# controllers/auth_controller.py

from flask import request, redirect, render_template, session, url_for
from services.auth_service import AuthService
from services.admin_service import AdminService

auth_service = AuthService()
admin_service = AdminService()

def login():
    if request.method == 'GET':
        return render_template('login.html')  # Giriş sayfasını getir

    username = request.form.get('username')  # Formdan gelen kullanıcı adı
    password = request.form.get('password')  # Formdan gelen şifre

    # Eğer giriş başarılıysa, admin kontrolü ile yönlendir.
    if auth_service.authenticate(username, password):
        session['username'] = username  # Session'da kullanıcı adı
        # Admin kontrolü ve role'ü session'a kaydet
        if admin_service.is_admin(username):
            session['role'] = 'admin'
            return redirect(url_for('task_bp.dashboard'))  # Görev paneline yönlendir
        else:
            session['role'] = 'user'
            return redirect(url_for('task_bp.dashboard'))  # Kullanıcıyı görevler sayfasına yönlendir
    else:
        return render_template('login.html', error='Giriş başarısız!')  # Hata mesajı ile tekrar login sayfasına dön

def logout():
    session.clear()  # Session'ı temizle
    return redirect(url_for('auth_bp.login_route'))  # Giriş sayfasına yönlendir
