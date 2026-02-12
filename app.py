# app.py
from flask import Flask
from routes.dashboard_routes import dashboard_bp
from routes.api_routes import api_bp
from routes.upload_routes import upload_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # register blueprints
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(upload_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
