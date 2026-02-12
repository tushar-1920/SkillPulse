# upload_routes.py
from flask import Blueprint, render_template, request

upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/upload", methods=["GET", "POST"])
def upload_resume():
    if request.method == "POST":
        # we will implement later
        return "Uploaded (processing will be added later)"
    return render_template("upload.html")
