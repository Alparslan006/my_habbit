from flask import Flask, redirect
from routes.task_routes import task_bp
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.score_routes import score_bp
from routes.auto_task_routes import auto_task_bp
from routes.default_task_routes import default_tasks_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = "gizli_anahtar_123"  # Gerçek ortamda .env ile sakla

    # Route kayıtları
    app.register_blueprint(task_bp, url_prefix="/tasks")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(score_bp, url_prefix="/score")
    app.register_blueprint(auto_task_bp, url_prefix="/auto")
    app.register_blueprint(default_tasks_bp)

    @app.route("/")
    def index():
        return redirect("/auth/login")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='127.0.0.1', port=5000, debug=True)
