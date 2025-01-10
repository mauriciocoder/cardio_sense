import logging
import os
from flask import Flask
from .routes import bp


def create_app():
    app = Flask(__name__)
    app.config["CELERY_BROKER_URL"] = os.environ.get(
        "CELERY_BROKER_URL", "amqp://localhost"
    )
    app.config["CELERY_RESULT_BACKEND"] = os.environ.get(
        "CELERY_RESULT_BACKEND", "rpc://"
    )
    app.register_blueprint(bp)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Flask application initialized.")
    return app


# Since FLASK_APP=src/api is set in docker-compose.yml
# It is required to instantiate the Flask src here (src)
app = create_app()
