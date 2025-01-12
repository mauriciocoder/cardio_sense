import pytest
from flask import Flask
from flask.testing import FlaskClient

VALID_EXAM_DICT = {
    "age": 25,
    "sex": "M",
    "chest_pain_type": "ATA",
    "resting_bp": 140,
    "cholesterol": 289,
    "fasting_bs": 0,
    "resting_ecg": "Normal",
    "max_hr": 172,
    "exercise_angina": "N",
    "oldpeak": 0.5,
    "st_slope": "Up",
}


INVALID_EXAM_DICT = {
    "age": 17,  # Invalid age, below 18
    "sex": "M",
    "chest_pain_type": "ATA",
    "resting_bp": 140,
    "cholesterol": 289,
    "fasting_bs": 0,
    "resting_ecg": "Normal",
    "max_hr": 172,
    "exercise_angina": "N",
    "oldpeak": 0,
    "st_slope": "Up",
}


@pytest.fixture
def app() -> Flask:
    from src.api import app

    yield app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


def test_create_valid_cardio_report(client: FlaskClient, mocker):
    # Mock Celery task creation (create_cardio_report_task.delay)
    mock_task = mocker.Mock()
    mock_task.id = "1"
    mock_task.result = None
    mocker.patch(
        "src.api.routes.create_cardio_report_task.delay", return_value=mock_task
    )
    # Send a POST request to /cardio_report
    response = client.post(
        "/cardio_report",
        json=[VALID_EXAM_DICT, VALID_EXAM_DICT],
    )
    assert response.status_code == 201
    assert len(response.json) == 2
    assert response.json[0]["task_id"] == "1"
    assert response.json[1]["task_id"] == "1"


def test_create_invalid_cardio_report(client: FlaskClient, mocker):
    # Mock Celery task creation (create_cardio_report_task.delay)
    mock_task = mocker.Mock()
    mock_task.id = "1"
    mock_task.result = None
    mocker.patch(
        "src.api.routes.create_cardio_report_task.delay", return_value=mock_task
    )
    # Send a POST request to /cardio_report
    response = client.post(
        "/cardio_report",
        json=[INVALID_EXAM_DICT, INVALID_EXAM_DICT],
    )
    assert response.status_code == 400
    assert len(response.json) == 2
    detail = {
        "ctx": {"gt": 18},
        "input": 17,
        "loc": [0, "age"],
        "msg": "Input should be greater than 18",
        "type": "greater_than",
        "url": "https://errors.pydantic.dev/2.10/v/greater_than",
    }
    assert response.json["details"][0] == detail
    detail["loc"] = [1, "age"]
    assert response.json["details"][1] == detail
