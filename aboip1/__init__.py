from flask import Flask
from aboip1.views.index import bp as index_bp
from aboip1.views.upload_csv import bp as upload_csv_bp

app = Flask(__name__)

app.register_blueprint(index_bp)
app.register_blueprint(upload_csv_bp)

if __name__ == '__main__':
    app.run(debug=True)
