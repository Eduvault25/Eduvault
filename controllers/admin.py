# controllers/admin.py
from flask import session, redirect, url_for
from app import app

def register_routes(app):
    @app.route("/admin/dash")
    def admin_dashboard():
        if session.get("role") != "admin":
            return redirect(url_for("signin_signup"))
        return "🛠️ Welcome to the Admin Dashboard"
