# controllers/auth_controller.py

from flask import request, redirect, render_template, session
from services.auth_service import AuthService

auth_service = AuthService()

def login():
    if request.method == 'GET':
        return render_template('login.html')  # Giriş sayfasını getir

    username = request.form.get('username')  # Formdan gelen kullanıcı adı
    password = request.form.get('password')  # Formdan gelen şifre

    # Eğer giriş başarılıysa, admin kontrolü ile yönlendir.
    if auth_service.authenticate(username, password):
        session['username'] = username  # Session'da kullanıcı adı
        if auth_service.is_admin(username):
            return redirect('/admin/panel')  # Admin paneline yönlendir
        return redirect('/tasks/dashboard')  # Kullanıcıyı görevler sayfasına yönlendir
    else:
        return render_template('login.html', error='Giriş başarısız!')  # Hata mesajı ile tekrar login sayfasına dön

def logout():
    session.clear()  # Session'ı temizle
    return redirect('/')  # Giriş sayfasına yönlendir
