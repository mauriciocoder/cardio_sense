from flask import Blueprint, current_app as app, request, jsonify

# from src.worker.tasks import generate_report_task
from src.model.exams import CardioExam
from pydantic import ValidationError, TypeAdapter

bp = Blueprint("api", __name__)


@bp.route("/cardio_report", methods=["POST"])
def cardio_report():
    try:
        exams = TypeAdapter(list[CardioExam]).validate_json(request.data)
        app.logger.info(f"exams: {exams}")
    except ValidationError as e:
        app.logger.error(e.errors())
        return jsonify({"error": "Invalid input data", "details": e.errors()}), 400
    return (
        jsonify(
            {
                "message": "Report generated successfully",
                "items_processed": len(exams),
            }
        ),
        200,
    )
    """
    for index, exam in enumerate(payload):
        app.logger.info(f"Processing exam {index}: {exam}")
        if isinstance(exam, dict):
            age = exam.get("Age", "N/A")
            sex = exam.get("Sex", "N/A")
            app.logger.info(f"Age: {age}, Sex: {sex}")
        else:
            app.logger.warning(f"Item at index {index} is not a valid object: {exam}")
    return (
        jsonify(
            {
                "message": "Report generated successfully",
                "items_processed": len(payload),
            }
        ),
        200,
    )
    """
