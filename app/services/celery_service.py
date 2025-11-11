from celery import Celery
from app.services.christmas_service import ChristmasService
from app.services.hue_service import HueService
from app.services.config_service import ConfigService


app = Celery(
    "celery_service", broker="redis://redis:6379/0", backend="redis://redis:6379/0"
)
config_service = ConfigService()
hue_service = HueService(config_service)
christmas_service = ChristmasService(hue_service, config_service)


@app.task
def christmas_shuffle():
    christmas_service.christmas_color_shuffle_job(3000)
