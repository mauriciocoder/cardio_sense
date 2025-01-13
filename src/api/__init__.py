import logging
import os
from flasgger import Swagger
from flask import Flask
from .routes import bp


def create_app():
    app = Flask(__name__)
    app.config["CELERY_BROKER_URL"] = os.environ.get(
        "CELERY_BROKER_URL", "redis://redis:6379/0"
    )
    app.config["CELERY_RESULT_BACKEND"] = os.environ.get(
        "CELERY_RESULT_BACKEND", "redis://redis:6379/0"
    )
    app.register_blueprint(bp)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Flask application initialized.")
    swagger_config = {
        "title": "SQUID-IQ - Cardio Sense API",
        "version": "1.0.0",
        "description": "",
    }
    Swagger(app, config=swagger_config, merge=True)
    return app


# Since FLASK_APP=src/api is set in docker-compose.yml
# It is required to instantiate the Flask src here (src)
app = create_app()
