import os
from flask import Flask
from aboip1.routes.upload_csv import bp as upload_csv_bp
from aboip1.routes.index import bp as index_bp

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ["APP_SECRET_KEY"]
    
    app.register_blueprint(index_bp)
    app.register_blueprint(upload_csv_bp)

    return app
