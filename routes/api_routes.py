from flask import Blueprint, jsonify
from services.market_service import get_top_skills

api_bp = Blueprint("api", __name__)


@api_bp.route("/health")
def health():
    return jsonify({"status": "ok", "project": "SkillPulse AI"})


@api_bp.route("/top-skills")
def top_skills():
    data = get_top_skills(limit=10)
    return jsonify(data)
