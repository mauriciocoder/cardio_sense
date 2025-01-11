from src.model.exams import CardioExam
from src.worker.llm import LLM
from src.worker.tasks import create_cardio_report_task


def test_create_cardio_report_task(mocker):
    # Mocking LLM().create_cardio_report_summary
    llm_mock = mocker.patch.object(
        LLM, "create_cardio_report_summary", return_value="Mocked summary"
    )
    mocker.patch("src.worker.tasks.save_report", return_value="mocked_file_path.html")

    # Mocking create_cardio_report_task
    exam = CardioExam(
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
    file_path, report = create_cardio_report_task(dict(exam))
    llm_mock.assert_called_once_with(exam)
    assert file_path == "mocked_file_path.html"
    assert "<span>Age:</span> 25" in report
    assert "<span>Sex:</span> Male" in report
    assert "<span>Chest Pain Type:</span> Atypical Angina" in report
    assert "<span>Resting Blood Pressure:</span> 140" in report
    assert "<span>Cholesterol:</span> 289" in report
    assert "<span>Fasting Blood Sugar:</span> <= 120" in report
    assert "<span>Resting ECG:</span> Normal" in report
    assert "<span>Max Heart Rate:</span> 172" in report
    assert "<span>Exercise Angina:</span> No" in report
    assert "<span>Oldpeak (ST):</span> 0.5" in report
    assert "<span>ST Slope:</span> Up" in report
    assert "<p>Mocked summary</p>" in report
