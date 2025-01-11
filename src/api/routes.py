from flask import Blueprint, current_app as app, request, jsonify

from src.worker.tasks import create_cardio_report_task
from src.model.exams import CardioExam
from pydantic import ValidationError, TypeAdapter

bp = Blueprint("api", __name__)


def load_exams(request) -> list[CardioExam]:
    return TypeAdapter(list[CardioExam]).validate_json(request.data)


@bp.route("/cardio_report", methods=["POST"])
def cardio_report():
    try:
        exams = load_exams(request)
        result = []
        for i, exam in enumerate(exams):
            app.logger.info(f"Creating task for Exam #{i}: {exam}")
            task = create_cardio_report_task.delay(dict(exam))
            app.logger.info(f"Task #{task.id} created for Exam #{i}")
            result.append(
                {
                    "exam_iloc": i,
                    "task_id": task.id,
                }
            )
        return (
            jsonify(result),
            201,
        )
    except ValidationError as e:
        app.logger.error(e.errors())
        return jsonify({"error": "Invalid input data", "details": e.errors()}), 400
