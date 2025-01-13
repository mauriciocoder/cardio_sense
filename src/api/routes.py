from flasgger import swag_from
from flask import (
    abort,
    Request,
    Response,
    Blueprint,
    current_app as app,
    request,
    jsonify,
)

from celery.result import AsyncResult
from ..worker import celery

from src.worker.tasks import create_cardio_report_task
from src.model.exams import CardioExam
from pydantic import ValidationError, TypeAdapter

bp = Blueprint("api", __name__)


def load_exams(request: Request) -> list[CardioExam]:
    return TypeAdapter(list[CardioExam]).validate_json(request.data)


@bp.route("/cardio_report_task", methods=["POST"])
@swag_from("cardio_report_task_swag.yml")
def cardio_report_task() -> Response:
    try:
        exams = load_exams(request)
        result = []
        for i, exam in enumerate(exams):
            app.logger.info(f"Creating task for Exam #{i}: {exam}")
            app.logger.info(f"Exam #{i}: {dict(exam)}")
            task = create_cardio_report_task.delay(dict(exam))
            ######################## TEST
            """
            counter = 0
            while counter < 60:
                x = AsyncResult(task.id, app=celery)
                app.logger.info(f"Task #{task.id} | Task status: {x.state}")
                counter += 1
                time.sleep(1)
            """
            ######################## END
            app.logger.info(f"Task #{task.id} created for Exam #{i}")
            result.append(
                {
                    "exam_id": exam.id,
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


@bp.route("/cardio_report_task/<task_id>", methods=["GET"])
@swag_from("cardio_report_task_get_swag.yml")
def get_cardio_report_task(task_id: str) -> Response:
    task = AsyncResult(task_id, app=celery)
    app.logger.info("###########################################")
    app.logger.info(f"Attributes of DatabaseBackend: {dir(task.backend)}")

    if task.state == "PENDING" and task.result is None:
        app.logger.warning(f"Task ID {task_id} not found.")
        abort(404)
    response = {"status": task.state, "task_id": task.id}
    if task.successful() or task.failed():
        response["result"] = task.result
    return (
        jsonify(response),
        200,
    )


@bp.route("/cardio_report_tasks", methods=["POST"])
@swag_from("cardio_report_tasks_swag.yml")
def get_cardio_report_tasks() -> Response:
    task_ids = request.json
    tasks = []
    for task_id in task_ids:
        task = AsyncResult(task_id, app=celery)
        app.logger.info(
            f"Task ID: {task.id}, Task State: {task.state}, Task Result: {task.result}"
        )
        response = {"status": task.state, "task_id": task.id}
        if task.successful() or task.failed():
            response["result"] = task.result
        tasks.append(response)
    return jsonify({"tasks": tasks}), 200
