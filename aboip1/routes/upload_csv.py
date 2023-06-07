from flask import Blueprint, request, jsonify, make_response
import pandas as pd
import time
from aboip1.views.inputs import Inputs
from aboip1.views.InputForm import InputForm
from aboip1.views.logging import getLogger
from aboip1.views.send_req import get_gpt_response, save_file_id_to_session
from config import Config

logger = getLogger()

bp = Blueprint("upload_csv", __name__)


# test route, not a feature
@bp.route("/get_cookie")
def get_cookie():
    cookies = request.cookies
    logger.debug(f"cookies: {cookies}")
    file_identifier = cookies.get("file_identifier")
    logger.debug(f"file_identifier: {file_identifier}")
    return jsonify({"file_identifier": file_identifier})


@bp.after_request
def after_request(response):
    timestamp = time.strftime("[%Y-%b-%d %H:%M]")
    logger.debug(f"{timestamp} {request.method} {request.url} {response.status}")
    return response


@bp.route("/upload_csv", methods=["POST"])
def upload_csv():
    try:
        # form = InputForm()
        # setInputs(form)
        save_file_id_to_session()
        domain = (
            None
            if request.host == "localhost:5000"
            else "ai-website-niche-finder-client.vercel.app"
        )
        logger.debug(f"Config.session in upload_csv: {Config.session}")
        response = make_response(jsonify({"status": "success"}), 200)
        response.set_cookie(
            "file_identifier", Config.session["file_identifier"], domain=domain
        )

        Inputs.from_row = int(request.form["fromRow"])
        Inputs.to_row = int(request.form["toRow"])
        Inputs.batch_length = int(request.form["batchLength"])
        Inputs.prompt_context = request.form["promptContext"]
        Inputs.prompt_question = request.form["promptQuestion"]
        Inputs.input_csv = request.files["csvFile"]
        Inputs.df = pd.read_csv(Inputs.input_csv, header=None)
        Inputs.FROM = Inputs.from_row
        Inputs.TO = Inputs.to_row
        logger.debug(f"Input.from_row = {Inputs.from_row}")
        logger.debug(f"Input.to_row = {Inputs.to_row}")
        logger.debug(f"Input.batch_length = {Inputs.batch_length}")
        logger.debug(f"Input.prompt_context = {Inputs.prompt_context}")
        logger.debug(f"Input.prompt_question = {Inputs.prompt_question}")
        logger.debug(f"Input.input_csv = {Inputs.input_csv}")
        logger.debug(f"Input.df = {Inputs.df}")

        get_gpt_response()
        return response
    except Exception as e:
        logger.exception("Exception: ")
        return jsonify({"error": f"{e}"}), 404


def setInputs(form):
    try:
        Inputs.from_row = int(form.from_row.data)
        Inputs.to_row = int(form.to_row.data)
        Inputs.batch_length = int(form.batch_length.data)
        Inputs.prompt_context = form.prompt_context.data
        Inputs.prompt_question = form.prompt_question.data
        Inputs.input_csv = request.files["csv_file"]
        Inputs.df = pd.read_csv(Inputs.input_csv, header=None)
        Inputs.FROM = 0
        Inputs.TO = len(Inputs.df.index)
        logger.debug(f"Dataframe: {Inputs.df}")
    except Exception as e:
        logger.exception("Exception: ")
