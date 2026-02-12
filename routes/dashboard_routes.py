from flask import Blueprint, render_template
from services.market_service import get_top_skills

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def home():
    return render_template("home.html")


@dashboard_bp.route("/dashboard")
def dashboard():
    top_skills = get_top_skills(limit=10)
    return render_template("dashboard.html", top_skills=top_skills)
