import pytest
from unittest.mock import MagicMock, patch
from app.models.light_fade_out_request import LightFadeOutRequest
from app.models.set_light_gradients_request import SetLightGradientsRequest
from app.services.christmas_service import ChristmasService
from app.services.config_service import GradientLightConfig
from typing import Generator


@patch("app.services.christmas_service.LightServer")
@patch("app.services.christmas_service.ConfigService")
def test_init(mock_light_server: MagicMock, mock_config_service: MagicMock) -> None:
    christmas_service = ChristmasService(mock_light_server, mock_config_service)
    assert christmas_service.christmas_colors == [
        {
            "color": {  # mint
                "xy": {"x": 0.300, "y": 0.400}
            }
        },
        {
            "color": {  # amber
                "xy": {"x": 0.525, "y": 0.410}
            }
        },
        {
            "color": {  # red
                "xy": {"x": 0.700, "y": 0.298}
            }
        },
        {
            "color": {  # green
                "xy": {"x": 0.210, "y": 0.710}
            }
        },
        {
            "color": {  # blue
                "xy": {"x": 0.160, "y": 0.150}
            }
        },
    ]


@patch("app.services.christmas_service.sleep")
@patch("app.services.christmas_service.random.shuffle")
@patch("app.services.christmas_service.ConfigService")
@patch("app.services.christmas_service.LightServer")
def test_christmas_color_shuffle(
    mock_light_server: MagicMock,
    mock_config_service: MagicMock,
    mock_random_shuffle: MagicMock,
    mock_time_sleep: MagicMock,
    outdoor_gradient_light_config: Generator[list[GradientLightConfig], None, None],
) -> None:
    christmas_service = ChristmasService(mock_light_server, mock_config_service)
    mock_config_service.outdoor_config.return_value = outdoor_gradient_light_config

    christmas_service.christmas_color_shuffle(3000)
    mock_random_shuffle.assert_called_once_with(christmas_service.christmas_colors)
    mock_config_service.outdoor_config.assert_called_once()
    mock_light_server.set_light_gradients.assert_any_call(
        "light_one",
        SetLightGradientsRequest.model_validate(
            {
                "dimming": {"brightness": 100},
                "gradient": {"points": [{"color": {"xy": {"x": 0.300, "y": 0.400}}}]},
                "dynamics": {"duration": 3000},
            }
        ),
    )
    mock_light_server.set_light_gradients.assert_any_call(
        "light_two",
        SetLightGradientsRequest.model_validate(
            {
                "dimming": {"brightness": 100},
                "gradient": {
                    "points": [
                        {"color": {"xy": {"x": 0.300, "y": 0.400}}},
                        {"color": {"xy": {"x": 0.525, "y": 0.410}}},
                    ]
                },
                "dynamics": {"duration": 3000},
            }
        ),
    )
    assert mock_time_sleep.call_count == 2
    mock_time_sleep.assert_called_with(3.0)
    mock_light_server.light_fade_out.assert_any_call(
        "light_one",
        LightFadeOutRequest.model_validate(
            {"dimming": {"brightness": 0}, "dynamics": {"duration": 3000}}
        ),
    )
    mock_light_server.light_fade_out.assert_any_call(
        "light_two",
        LightFadeOutRequest.model_validate(
            {"dimming": {"brightness": 0}, "dynamics": {"duration": 3000}}
        ),
    )


@pytest.fixture
def outdoor_gradient_light_config() -> Generator[list[GradientLightConfig], None, None]:
    yield [
        GradientLightConfig.model_validate(
            {"id": "light_one", "name": "light_one", "gradient-points": 1}
        ),
        GradientLightConfig.model_validate(
            {"id": "light_two", "name": "light_two", "gradient-points": 2}
        ),
    ]
