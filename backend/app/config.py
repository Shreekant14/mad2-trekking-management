import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "mad2-secret-key")

    SQLALCHEMY_DATABASE_URI = "sqlite:///trekking.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "jwt-secret-key"
    )

    # Redis
    REDIS_URL = os.getenv(
        "REDIS_URL",
        "redis://localhost:6379/0"
    )

    # Celery
    CELERY_BROKER_URL = os.getenv(
        "CELERY_BROKER_URL",
        "redis://localhost:6379/1"
    )

    CELERY_RESULT_BACKEND = os.getenv(
        "CELERY_RESULT_BACKEND",
        "redis://localhost:6379/1"
    )

    CELERY_TIMEZONE = "Asia/Kolkata"

    CELERY_BEAT_SCHEDULE = {
        "update-trek-statuses-daily": {
            "task": "app.tasks.update_trek_statuses",
            "schedule": 3600.0,
        }
    }