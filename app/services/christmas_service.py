from app.services.config_service import ConfigService
from app.services.hue_service import HueService
import random
from app.models.set_light_gradients_request import SetLightGradientsRequest
from app.models.light_fade_out_request import LightFadeOutRequest
from time import sleep


class ChristmasService:
    def __init__(self, hue_service: HueService, config_service: ConfigService):
        self._hue_service = hue_service
        self._config_service = config_service
        self.christmas_colors = [
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

    def christmas_color_shuffle(self, effect_duration: int):
        random.shuffle(self.christmas_colors)
        outdoor_config = self._config_service.outdoor_config()
        sleep_time = effect_duration / 1000
        print("lighting up")
        # TODO: set light state to `on`
        for light in outdoor_config:
            request = SetLightGradientsRequest.model_validate(
                {
                    "dimming": {"brightness": 100},
                    "gradient": {
                        "points": self.christmas_colors[: light.gradient_points]
                    },
                    "dynamics": {"duration": effect_duration},
                }
            )
            self._hue_service.set_light_gradients(light.id, request)
        sleep(sleep_time)
        print("lighting down")
        for light in outdoor_config:
            request = LightFadeOutRequest.model_validate(
                {
                    "dimming": {"brightness": 0},
                    "dynamics": {"duration": effect_duration},
                }
            )
            self._hue_service.light_fade_out(light.id, request)
        sleep(sleep_time)

    def christmas_color_shuffle_job(self, effect_duration: int):
        while True:
            self.christmas_color_shuffle(effect_duration)
