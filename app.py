from flask import Flask

app = Flask(__name__)

if __name__ == "__main__":
    print("Execute these commands to run the flask app: ")
    print("For windows: ")
    print("set FLASK_APP=aboip1")
    print("set FLASK_ENV=development")
    print("flask run")
    print("For linux/mac: ")
    print("export FLASK_APP=aboip1")
    print("export FLASK_ENV=development")
    print("flask run")
    app.run(debug=True)
