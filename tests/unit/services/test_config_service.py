from unittest.mock import patch, MagicMock

import pytest

from app.services.config_service import Config, ConfigService, GradientLightConfig


@patch("app.services.config_service.open", side_effect=Exception("bam"))
def test_init_sad_path(mock_open: MagicMock) -> None:
    with pytest.raises(Exception, match="bam"):
        ConfigService()


def test_init_happy_path() -> None:
    config_service = ConfigService()
    assert isinstance(config_service._config, Config)


def test_hue_config() -> None:
    config_service = ConfigService()
    ip_address, _ = config_service.hue_config()
    assert ip_address == "192.168.163.2"


def test_outdoor_config() -> None:
    config_service = ConfigService()
    result = config_service.outdoor_config()
    assert result == [
        GradientLightConfig.model_validate(
            {
                "name": "upper-light",
                "id": "b86e1048-7aed-4b4f-b596-6a0e818d19e5",
                "gradient-points": 5,
            },
        ),
        GradientLightConfig.model_validate(
            {
                "name": "porch-light",
                "id": "80d7d9d2-448c-4897-a4ff-6a163d6dd244",
                "gradient-points": 2,
            }
        ),
    ]
