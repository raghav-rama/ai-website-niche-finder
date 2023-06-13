from flask import Blueprint, request, jsonify, make_response
import pandas as pd
import time
import os
from aboip1.views.inputs import Inputs
from aboip1.views.helper import getFilePath
from aboip1.views.logging import getLogger
from aboip1.views.send_req import get_gpt_response, save_file_id_to_session
from config import Config
import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

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
    logger.debug(f"after request: {response}")
    send_mail()
    return response


@bp.route("/upload_csv", methods=["POST"])
def upload_csv():
    try:
        # form = InputForm()
        # setInputs(form)
        save_file_id_to_session()
        # domain = (
        #     None
        #     if request.host == "localhost:5000"
        #     else ".vercel.app"
        # )
        logger.debug(f"Config.session in upload_csv: {Config.session}")
        response = make_response(jsonify({"status": "success"}), 200)
        response.headers.add(
            "Set-Cookie",
            f"file_identifier={Config.session['file_identifier']}; Secure; SameSite=None",
        )
        # response.set_cookie(
        #     "file_identifier",
        #     Config.session["file_identifier"],
        #     domain=None,
        #     samesite=None,
        # )

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
        logger.debug(f"Input.FROM = {Inputs.FROM}")
        logger.debug(f"Input.TO = {Inputs.TO}")

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


def send_mail():
    msg = MIMEMultipart()
    msg["Subject"] = "CSV Result"
    msg["From"] = Config.FROM_EMAIL
    msg["To"] = ", ".join(Config.TO_EMAILS)
    part = MIMEText("PFA", "plain")
    msg.attach(part)
    ses_client = boto3.client(
        "ses",
        region_name=Config.AWS_REGION,
        aws_access_key_id=Config.AWS_ACCESS_KEY,
        aws_secret_access_key=Config.AWS_SECRET_KEY,
    )

    csv_file_path = getFilePath(Config.session["file_identifier"])

    try:
        with open(csv_file_path, "rb") as file:
            filename = os.path.basename(csv_file_path)
            filename.replace(f"-{Config.session['file_identifier']}", "")
            part = MIMEApplication(file.read())
            part.add_header(
                "Content-Disposition",
                "attachment",
                filename=filename,
            )
            msg.attach(part)
            response = ses_client.send_raw_email(
                Destinations=Config.TO_EMAILS,
                # Destination={
                #     "ToAddresses": Config.TO_EMAILS,
                # },
                # Message={
                #     "Body": {
                #         "Html": {
                #             "Charset": "UTF-8",
                #             "Data": f"Your file is ready for download. <br><br> <a href=#>Download</a>",
                #         },
                #         "Text": {
                #             "Data": f"Your file is ready for download. Download from attachment",
                #         },
                #     },
                #     "Subject": {
                #         "Charset": "UTF-8",
                #         "Data": "Your file is ready for download",
                #     },
                # },
                RawMessage={"Data": msg.as_string()},
                Source=Config.FROM_EMAIL,
            )
    except ClientError as e:
        print(e.response["Error"]["Message"])
        logger.exception("Client Error: ")
    except Exception as e:
        print("Some error occurerd", e)
        logger.exception("Error: ")
    else:
        print(f"Email sent! Message ID: {response['MessageId']}")
        logger.info("Email Sent!")
