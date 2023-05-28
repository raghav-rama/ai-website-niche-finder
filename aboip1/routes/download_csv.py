from flask import send_file, Blueprint, jsonify
from aboip1.views.logging import getLogger
from aboip1.views.inputs import Inputs
from aboip1.views.helper import getFilePath

logger = getLogger()

bp = Blueprint("download_csv", __name__)

@bp.route("/download_csv", methods=["GET"])
def download_csv():
    try:
        file_path = getFilePath()
        if file_path is None:
            return jsonify({"error": "No file found"}), 404
        else:
            return send_file(file_path, download_name="output.csv", as_attachment=True)
    except Exception as e:
        logger.exception("Exception: ")
        return jsonify({"error": f"{e}"}), 404
