import pytest
from flask import Flask
from flask.testing import FlaskClient


@pytest.fixture
def app() -> Flask:
    from src.api import app

    yield app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture
def exam_dict():
    return {
        "id": "EXAM-1011",
        "age": 25,
        "chest_pain_type": "ATA",
        "cholesterol": 289,
        "exercise_angina": "N",
        "fasting_bs": 0,
        "max_hr": 172,
        "oldpeak": 0.5,
        "resting_bp": 140,
        "resting_ecg": "Normal",
        "sex": "M",
        "st_slope": "Up",
    }


def mock_create_cardio_report_task(mocker):
    # Mock Celery task creation (create_cardio_report_task.delay)
    mock_task = mocker.Mock()
    mock_task.id = "1"
    mock_task.result = None
    mocker.patch(
        "src.api.routes.create_cardio_report_task.delay", return_value=mock_task
    )


def test_create_valid_cardio_report_task(client: FlaskClient, mocker, exam_dict):
    mock_create_cardio_report_task(mocker)
    response = client.post(
        "/cardio_report_task",
        json=[exam_dict, exam_dict],
    )
    assert response.status_code == 201
    assert len(response.json) == 2
    assert response.json[0]["task_id"] == "1"
    assert response.json[1]["task_id"] == "1"


def test_create_invalid_cardio_report_task(client: FlaskClient, mocker, exam_dict):
    mock_create_cardio_report_task(mocker)
    exam_dict["age"] = 17  # Invalid age
    response = client.post(
        "/cardio_report_task",
        json=[exam_dict, exam_dict],
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
