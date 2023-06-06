from flask import send_file, Blueprint, jsonify, request
from aboip1.views.logging import getLogger
from aboip1.views.helper import getFilePath, list_files
from config import Config

logger = getLogger()

bp = Blueprint("download_csv", __name__)


@bp.route("/download_csv", methods=["GET"])
def download_csv():
    try:
        cookies = request.cookies
        logger.debug(f"cookies: {cookies}")
        file_identifier = cookies.get("file_identifier")
        logger.debug(f"session in download_csv: {Config.session}")
        # logger.debug(f"sesion['file_identifier']: {Config.session['file_identifier']}")
        file_path = getFilePath(file_identifier)
        logger.debug(f"file_path: {file_path}")
        logger.debug(f"list_files: {list_files()}")
        if file_path is None:
            return (
                jsonify(
                    {
                        "error": "No file found",
                        "file_path": file_path,
                        "files": list_files(),
                    }
                ),
                404,
            )
        else:
            return send_file(
                file_path, download_name="output.csv", as_attachment=True, max_age=600
            )
    except Exception as e:
        logger.exception("Exception: ")
        return jsonify({"error": f"{e}"}), 404
