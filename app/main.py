from fastapi import Depends, FastAPI
from typing import Any

from app.services.hue_service import HueService
from app.services.celery_service import app as celery_app, christmas_shuffle
from app.services.factories import get_hue_service


app = FastAPI()


@app.get("/status")
def get_status() -> dict[str, str]:
    return {"msg": "I am alive."}


@app.get("/lights")
def get_lights(hue_service: HueService = Depends(get_hue_service)) -> Any:
    return hue_service.get_lights().json()


@app.post("/christmas_shuffle")
def get_christmas_shuffle() -> dict[str, str]:
    christmas_shuffle.delay()
    return {"msg": "christmas color shuffle enqueued"}


# TODO: consider turning this into a decorator for
#       indefinite lighting jobs.
@app.post("/cancel")
def post_cancel() -> dict[str, str]:
    revoked = []
    inspect = celery_app.control.inspect()
    active = inspect.active()
    task_ids = []

    if active is None:
        return {"msg": "no active tasks"}

    for worker_tasks in active.values():
        for t in worker_tasks:
            task_ids.append(t["id"])
    for task_id in task_ids:
        celery_app.control.revoke(task_id, terminate=True, signal="SIGTERM")
        revoked.append(task_id)
    return {
        "msg": f"revoked {len(revoked)} tasks.",
        "revoked_task_ids": ",".join(revoked),
    }
