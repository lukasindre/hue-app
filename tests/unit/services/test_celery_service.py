from unittest.mock import MagicMock, patch
from app.services.celery_service import christmas_shuffle


@patch("app.services.celery_service.get_christmas_service")
def test_christmas_shuffle(mock_get_christmas_service: MagicMock) -> None:
    mock_service = MagicMock()
    mock_get_christmas_service.return_value = mock_service
    christmas_shuffle()
    mock_get_christmas_service.assert_called_once()
    mock_service.christmas_color_shuffle_job.assert_called_once_with(3000)
