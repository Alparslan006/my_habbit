from flask import session, redirect, render_template, request
from services.admin_service import AdminService

admin_service = AdminService()

def show_admin_panel():
    if 'username' not in session or not admin_service.is_admin(session['username']):
        return redirect('/auth/login')

    modules = admin_service.get_all_modules()
    return render_template('admin.html', user=session['username'], modules=modules)

def toggle_modules():
    if 'username' not in session or not admin_service.is_admin(session['username']):
        return redirect('/auth/login')

    selected_modules = request.form.getlist('moduller')
    admin_service.update_module_statuses(selected_modules)
    return redirect('/admin/panel')
