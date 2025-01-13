import pytest
from src.model.exams import CardioExam
from src.worker.llm import LLM
from src.worker.tasks import create_cardio_report_content


@pytest.fixture
def exam():
    return CardioExam(
        id="ID",
        age=25,
        sex="M",
        chest_pain_type="ATA",
        resting_bp=140,
        cholesterol=289,
        fasting_bs=0,
        resting_ecg="Normal",
        max_hr=172,
        exercise_angina="N",
        oldpeak=0.5,
        st_slope="Up",
    )


def test_create_cardio_report(mocker, exam: CardioExam):
    llm_mock = mocker.patch.object(
        LLM, "create_cardio_report_summary", return_value="Mocked summary"
    )
    report = create_cardio_report_content(exam)
    llm_mock.assert_called_once_with(exam)
    assert "Exam Id:</span> ID" in report
    assert "Age:</span> 25" in report
    assert "Sex:</span> Male" in report
    assert "Chest Pain Type:</span> Atypical Angina" in report
    assert "Resting Blood Pressure:</span> 140" in report
    assert "Cholesterol:</span> 289" in report
    assert "Fasting Blood Sugar:</span> <= 120" in report
    assert "Resting ECG:</span> Normal" in report
    assert "Max Heart Rate:</span> 172" in report
    assert "Exercise Angina:</span> No" in report
    assert "Oldpeak (ST):</span> 0.5" in report
    assert "ST Slope:</span> Up" in report
    assert "Mocked summary" in report
