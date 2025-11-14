from unittest.mock import patch, MagicMock
from app.services.factories import (
    get_christmas_service,
    get_config_service,
    get_hue_service,
)
from app.services.config_service import ConfigService


def test_get_config_service() -> None:
    result = get_config_service()
    assert isinstance(result, ConfigService)


@patch("app.services.factories.HueService")
@patch("app.services.factories.get_config_service")
def test_get_hue_service(
    mock_config_service_factory: MagicMock, mock_hue_service: MagicMock
) -> None:
    mock_config = MagicMock
    mock_config_service_factory.return_value = mock_config
    get_hue_service()
    mock_config_service_factory.assert_called_once()
    mock_hue_service.assert_called_once_with(mock_config)


@patch("app.services.factories.ChristmasService")
@patch("app.services.factories.get_hue_service")
@patch("app.services.factories.get_config_service")
def test_get_christmas_service(
    mock_config_service_factory: MagicMock,
    mock_hue_service_factory: MagicMock,
    mock_christmas_service: MagicMock,
) -> None:
    mock_config = MagicMock()
    mock_config_service_factory.return_value = mock_config
    mock_hue_service = MagicMock()
    mock_hue_service_factory.return_value = mock_hue_service
    get_christmas_service()
    mock_config_service_factory.assert_called_once()
    mock_hue_service_factory.assert_called_once()
    mock_christmas_service.assert_called_once_with(mock_hue_service, mock_config)
