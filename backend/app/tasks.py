from datetime import date

from .extensions import celery, db
from .models import Trek


@celery.task
def update_trek_statuses():

    today = date.today()

    treks = Trek.query.filter(
        Trek.status == "UPCOMING",
        Trek.end_date < today
    ).all()

    updated_count = 0

    for trek in treks:

        trek.status = "COMPLETED"

        updated_count += 1

    if updated_count > 0:
        db.session.commit()

    return {
        "updated_treks": updated_count
    }