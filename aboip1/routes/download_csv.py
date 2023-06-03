from flask import send_file, Blueprint, jsonify
from aboip1.views.logging import getLogger
from aboip1.views.inputs import Inputs
from aboip1.views.helper import getFilePath, list_files

logger = getLogger()

bp = Blueprint("download_csv", __name__)


@bp.route("/download_csv", methods=["GET"])
def download_csv():
    try:
        file_path = getFilePath()
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
            return send_file(file_path, download_name="output.csv", as_attachment=True, max_age=600)
    except Exception as e:
        logger.exception("Exception: ")
        return jsonify({"error": f"{e}"}), 404
