from flask import Blueprint, render_template
from config import Config
from aboip1.views.InputForm import InputForm

OPENAI_API_KEY = Config.OPENAI_API_KEY

bp = Blueprint("index", __name__)


@bp.route("/")
def index():
    form = InputForm()
    if form.validate_on_submit():
        return "CSV file uploaded successfully"
    return render_template("index.html", form=form)


@bp.route("/hello")
def hello_template():
    return render_template("hello.html", name=OPENAI_API_KEY)
