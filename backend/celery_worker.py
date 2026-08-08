from app import create_app
from app.extensions import celery
from app.celery_app import init_celery

app = create_app()

init_celery(app)

import app.tasks