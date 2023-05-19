from flask import Flask
from aboip1.views.hello import bp as hello_bp

app = Flask(__name__)
app.register_blueprint(hello_bp)

if __name__ == '__main__':
    app.run(debug=True)
