from flask import Blueprint, jsonify, request
from aboip1.views.helper import list_files, cleanup
from aboip1.views.logging import getLogger
from aboip1.views.inputs import Inputs

bp = Blueprint("can_continue", __name__)
logger = getLogger()


@bp.route("/can_continue", methods=["GET"])
def continue_():
    file_list = list_files()
    if len(file_list):
        return jsonify({"status": "can continue"}), 200
    else:
        return jsonify({"status": "can't continue"}), 200


@bp.route("/cleanup", methods=["POST"])
def cleanup_():
    data = request.get_json()
    print(data["choice"])
    try:
        if data["choice"] == "yes":
            cleanup()
            logger.debug(f"Cleanup done")
            Inputs.flag = 1
            return jsonify({"status": "cleaned up"}), 200
        if data["choice"] == "no":
            Inputs.flag = 0
            return jsonify({"status": "not cleaned up"}), 200
    except Exception as e:
        Inputs.flag = 0
        return jsonify({"error": f"{e}"}), 404
