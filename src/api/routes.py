from flask import Blueprint, current_app as app, request, jsonify
from src.worker.tasks import generate_report_task

bp = Blueprint("api", __name__)


@bp.route("/generate_report", methods=["POST"])
def generate_report():
    app.logger.info("generate_report")
    data = request.get_json()
    if not all(k in data for k in ("age", "gender", "cholesterol_measurements")):
        return (
            jsonify(
                {
                    "error": (
                        "Missing required fields: age, gender,"
                        " cholesterol_measurements"
                    )
                }
            ),
            400,
        )
    task = generate_report_task.delay(data)
    return jsonify({"task_id": task.task_id}), 202
