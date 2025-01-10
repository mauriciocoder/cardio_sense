from . import celery, logger
from jinja2 import Template


@celery.task
def generate_report_task(data):
    logger.info("generate_report_task called")
    age = data["age"]
    gender = data["gender"]
    cholesterol_measurements = data["cholesterol_measurements"]

    template = Template(
        """
    <html>
        <body>
            <h1>Cholesterol Report</h1>
            <p><strong>Age:</strong> {{ age }}</p>
            <p><strong>Gender:</strong> {{ gender }}</p>
            <p><strong>Cholesterol Measurements:</strong></p>
            <ul>
                {% for measurement in cholesterol_measurements %}
                <li>{{ measurement }} mm/dl</li>
                {% endfor %}
            </ul>
        </body>
    </html>
    """
    )
    report = template.render(
        age=age,
        gender=gender,
        cholesterol_measurements=cholesterol_measurements,
    )
    return report
