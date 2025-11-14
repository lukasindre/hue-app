from typing import Protocol, runtime_checkable
from app.models.light_fade_out_request import LightFadeOutRequest
from app.models.set_light_gradients_request import SetLightGradientsRequest
import httpx


@runtime_checkable
class LightServer(Protocol):
    def get_lights(self) -> httpx.Response: ...

    def get_devices(self) -> httpx.Response: ...

    def light_fade_out(
        self, light_id: str, request: LightFadeOutRequest
    ) -> httpx.Response: ...

    def set_light_gradients(
        self, light_id: str, request: SetLightGradientsRequest
    ) -> httpx.Response: ...
