import os
from flask import Flask
from flask_cors import CORS
from flask_session import Session
from aboip1.routes.upload_csv import bp as upload_csv_bp
from aboip1.routes.index import bp as index_bp
from aboip1.routes.can_continue import bp as can_continue_bp
from aboip1.routes.download_csv import bp as download_csv_bp


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ["APP_SECRET_KEY"]
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["SESSION_COOKIE_SECURE"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_DOMAIN"] = "localhost" if app.debug else ".vercel.app"
    Session(app)

    app.register_blueprint(index_bp)
    app.register_blueprint(upload_csv_bp)
    app.register_blueprint(can_continue_bp)
    app.register_blueprint(download_csv_bp)

    CORS(app, supports_credentials=True)

    return app
