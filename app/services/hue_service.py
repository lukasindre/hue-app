from app.models.light_fade_out_request import LightFadeOutRequest
from app.services.config_service import ConfigService
from app.models.set_light_gradients_request import SetLightGradientsRequest
import httpx


class HueService:
    def __init__(self, config_service: ConfigService) -> None:
        self._config_service = config_service
        self.ip_address, hue_username = self._config_service.hue_config()
        self._client = httpx.Client(
            headers={
                "hue-application-key": hue_username,
                "Content-Type": "application/json",
            },
            verify=False,
        )

    def get_lights(self) -> httpx.Response:
        response = self._client.get(f"https://{self.ip_address}/clip/v2/resource/light")
        response.raise_for_status()
        return response

    def get_devices(self) -> httpx.Response:
        response = self._client.get(
            f"https://{self.ip_address}/clip/v2/resource/device"
        )
        response.raise_for_status()
        return response

    def light_fade_out(
        self, light_id: str, request: LightFadeOutRequest
    ) -> httpx.Response:
        response = self._client.put(
            f"https://{self.ip_address}/clip/v2/resource/light/{light_id}",
            json=request.model_dump(),
        )
        response.raise_for_status()
        return response

    def set_light_gradients(
        self, light_id: str, request: SetLightGradientsRequest
    ) -> httpx.Response:
        response = self._client.put(
            f"https://{self.ip_address}/clip/v2/resource/light/{light_id}",
            json=request.model_dump(),
        )
        response.raise_for_status()
        return response
