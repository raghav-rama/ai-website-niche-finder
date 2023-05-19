from flask import Blueprint, render_template, request
import pandas as pd
import time
from aboip1.views.inputs import Inputs
from aboip1.views.InputForm import InputForm
from aboip1.views.logging import getLogger
from aboip1.views.send_req import get_gpt_response

logger = getLogger()

bp = Blueprint("upload_csv", __name__)


@bp.route("/upload_csv", methods=["POST"])
def upload_csv():
    form = InputForm()
    setInputs(form)
    logger.debug(f"Input.from_row = {Inputs.from_row}")
    logger.debug(f"Input.to_row = {Inputs.to_row}")
    logger.debug(f"Input.batch_length = {Inputs.batch_length}")
    logger.debug(f"Input.prompt_context = {Inputs.prompt_context}")
    logger.debug(f"Input.prompt_question = {Inputs.prompt_question}")
    get_gpt_response()
    return "CSV file uploaded successfully"


def setInputs(form):
    Inputs.from_row = int(form.from_row.data)
    Inputs.to_row = int(form.to_row.data)
    Inputs.batch_length = int(form.batch_length.data)
    Inputs.prompt_context = form.prompt_context.data
    Inputs.prompt_question = form.prompt_question.data
    Inputs.input_csv = request.files["csv_file"]
    Inputs.df = pd.read_csv(Inputs.input_csv, header=None)
    Inputs.FROM = 0
    Inputs.TO = len(Inputs.df.index)
    # Process the CSV data based on the form inputs
    # ...
    time.sleep(5)
    logger.debug(f"Dataframe: {Inputs.df}")
