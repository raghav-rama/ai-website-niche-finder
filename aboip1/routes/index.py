from flask import Blueprint, render_template, make_response
from aboip1.views.InputForm import InputForm
from aboip1.views.logging import getLogger

bp = Blueprint("index", __name__)

logger = getLogger()


@bp.route("/")
def index():
    form = InputForm()
    if form.validate_on_submit():
        return "CSV file uploaded successfully"
    return render_template("index.html", form=form)


@bp.route("/hello")
def hello_template():
    return render_template("hello.html", name="AI Website Niche Finder")

# test route, not a feature
@bp.route("/set_cookie")
def cookie_insertion():
    response = make_response("Cookie inserted")
    response.set_cookie("file_identifier", value="values")
    return response