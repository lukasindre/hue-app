from unittest.mock import patch, MagicMock

from httpx import Request, Response
from app.models.light_fade_out_request import LightFadeOutRequest
from app.models.set_light_gradients_request import SetLightGradientsRequest
from app.services.hue_service import HueService


@patch("app.services.hue_service.ConfigService")
def test_init(mock_config_service: MagicMock) -> None:
    mock_config_service.hue_config.return_value = "0.0.0.0", "sally"
    result = HueService(mock_config_service)
    assert result._config_service == mock_config_service
    assert result.ip_address == "0.0.0.0"
    assert "hue-application-key" in result._client.headers


@patch("app.services.hue_service.ConfigService")
@patch("app.services.hue_service.httpx.Client.get")
def test_get_lights(
    mock_hue_httpx_client: MagicMock, mock_config_service: MagicMock
) -> None:
    mock_config_service.hue_config.return_value = "0.0.0.0", "sally"
    mock_hue_httpx_client.return_value = Response(
        200, request=Request("GET", "https://example.com")
    )
    hue_service = HueService(mock_config_service)
    # result = hue_service.get_lights()
    hue_service.get_lights()
    mock_hue_httpx_client.assert_called_once_with(
        "https://0.0.0.0/clip/v2/resource/light"
    )


@patch("app.services.hue_service.ConfigService")
@patch("app.services.hue_service.httpx.Client.get")
def test_get_devices(
    mock_hue_httpx_client: MagicMock, mock_config_service: MagicMock
) -> None:
    mock_config_service.hue_config.return_value = "0.0.0.0", "sally"
    mock_hue_httpx_client.return_value = Response(
        200, request=Request("GET", "https://example.com")
    )
    hue_service = HueService(mock_config_service)
    hue_service.get_devices()
    mock_hue_httpx_client.assert_called_once_with(
        "https://0.0.0.0/clip/v2/resource/device"
    )


@patch("app.services.hue_service.ConfigService")
@patch("app.services.hue_service.httpx.Client.put")
def test_light_fade_out(
    mock_hue_httpx_client: MagicMock, mock_config_service: MagicMock
) -> None:
    mock_config_service.hue_config.return_value = "0.0.0.0", "sally"
    mock_hue_httpx_client.return_value = Response(
        200, request=Request("PUT", "https://example.com")
    )
    hue_service = HueService(mock_config_service)
    hue_service.light_fade_out(
        "1",
        LightFadeOutRequest.model_validate(
            {"dimming": {"brightness": 0}, "dynamics": {"duration": 1000}}
        ),
    )
    mock_hue_httpx_client.assert_called_once_with(
        "https://0.0.0.0/clip/v2/resource/light/1",
        json={"dimming": {"brightness": 0}, "dynamics": {"duration": 1000}},
    )


@patch("app.services.hue_service.ConfigService")
@patch("app.services.hue_service.httpx.Client.put")
def test_set_light_gradients(
    mock_hue_httpx_client: MagicMock, mock_config_service: MagicMock
) -> None:
    mock_config_service.hue_config.return_value = "0.0.0.0", "sally"
    mock_hue_httpx_client.return_value = Response(
        200, request=Request("PUT", "https://example.com")
    )
    hue_service = HueService(mock_config_service)
    hue_service.set_light_gradients(
        "1",
        SetLightGradientsRequest.model_validate(
            {
                "dimming": {"brightness": 100},
                "gradient": {"points": [{"color": {"xy": {"x": 0.5, "y": 0.5}}}]},
                "dynamics": {"duration": 1000},
            }
        ),
    )
    mock_hue_httpx_client.assert_called_once_with(
        "https://0.0.0.0/clip/v2/resource/light/1",
        json={
            "dimming": {"brightness": 100},
            "gradient": {"points": [{"color": {"xy": {"x": 0.5, "y": 0.5}}}]},
            "dynamics": {"duration": 1000},
        },
    )
