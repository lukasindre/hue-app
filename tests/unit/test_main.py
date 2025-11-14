from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.services.factories import get_hue_service


client = TestClient(app)


def test_get_status() -> None:
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"msg": "I am alive."}


@patch("app.main.HueService")
def test_get_lights(mock_hue_service: MagicMock) -> None:
    app.dependency_overrides[get_hue_service] = lambda: mock_hue_service
    mock_response = MagicMock()
    mock_response.json.return_value = {"valid": "json"}
    mock_hue_service.get_lights.return_value = mock_response

    response = client.get("/lights")

    assert response.status_code == 200
    assert response.json() == {"valid": "json"}
    app.dependency_overrides.clear()


@patch("app.main.christmas_shuffle.delay")
def test_get_christmas_shuffle(christmas_shuffle_delay_mock: MagicMock) -> None:
    response = client.post("/christmas_shuffle")
    christmas_shuffle_delay_mock.assert_called_once()
    assert response.json() == {"msg": "christmas color shuffle enqueued"}


@patch("app.main.celery_app.control.inspect")
def test_post_cancel_no_active_tasks(mock_inspect: MagicMock) -> None:
    mock_inspect.return_value.active.return_value = None
    client = TestClient(app)
    response = client.post("/cancel")
    assert response.status_code == 200
    assert response.json() == {"msg": "no active tasks"}


@patch("app.main.celery_app.control.inspect")
@patch("app.main.celery_app.control.revoke")
def test_post_cancel_with_active_tasks(
    mock_revoke: MagicMock, mock_inspect: MagicMock
) -> None:
    active_tasks = {
        "worker1": [{"id": "task1"}, {"id": "task2"}],
        "worker2": [{"id": "task3"}],
    }

    mock_inspect.return_value.active.return_value = active_tasks

    client = TestClient(app)
    response = client.post("/cancel")

    mock_revoke.assert_any_call("task1", terminate=True, signal="SIGTERM")
    mock_revoke.assert_any_call("task2", terminate=True, signal="SIGTERM")
    mock_revoke.assert_any_call("task3", terminate=True, signal="SIGTERM")
    assert mock_revoke.call_count == 3

    assert response.status_code == 200
    resp_json = response.json()
    assert resp_json["msg"] == "revoked 3 tasks."
    assert resp_json["revoked_task_ids"] == "task1,task2,task3"
