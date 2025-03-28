from flask import Blueprint, render_template, redirect, session, url_for
from controllers.admin_controller import show_admin_panel, toggle_modules

admin_bp = Blueprint("admin_bp", __name__)

@admin_bp.route("/panel")
def admin_panel():
    # Admin kullanıcı adı ve rol kontrolü
    if not session.get("username") or session.get("role") != "admin":
        return redirect(url_for("auth_bp.login_route"))
    
    # Admin panelini göster
    return show_admin_panel()

@admin_bp.route("/toggle-module", methods=["POST"])
def toggle_module():
    # Admin kullanıcı adı ve rol kontrolü
    if not session.get("username") or session.get("role") != "admin":
        return redirect(url_for("auth_bp.login_route"))
    
    return toggle_modules()
