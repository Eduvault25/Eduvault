from flask import session, redirect, url_for
from app import app  # ← directly import the app instance

@app.route("/student/dashboard")
def student_dashboard():
    if session.get("role") != "student":
        return redirect(url_for("signin_signup"))
    return "🎓 Welcome to the Student Dashboard"
