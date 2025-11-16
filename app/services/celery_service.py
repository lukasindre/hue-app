from celery import Celery
from app.services.factories import get_christmas_service


app = Celery(
    "celery_service", broker="redis://redis:6379/0", backend="redis://redis:6379/0"
)


@app.task
def christmas_shuffle() -> None:
    christmas_service = get_christmas_service()
    christmas_service.christmas_color_shuffle_job(3000)


@app.task
def christmas_glow() -> None:
    christmas_service = get_christmas_service()
    christmas_service.christmas_glow_job(3000)
