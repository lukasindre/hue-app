from typing import Tuple
from pydantic import Field, BaseModel
import yaml
from dotenv import load_dotenv
import os

load_dotenv()


class HueConfig(BaseModel):
    username_key: str = Field(alias="username-key")
    token_key: str = Field(alias="token-key")
    bridge_ip_address: str = Field(alias="bridge-ip-address")


class GradientLightConfig(BaseModel):
    name: str
    id: str
    gradient_points: int = Field(alias="gradient-points")


class LightsConfig(BaseModel):
    outdoor: list[GradientLightConfig]


class Config(BaseModel):
    hue: HueConfig
    lights: LightsConfig


class ConfigService:
    def __init__(self):
        try:
            with open(f"app/config/{os.environ['ENV']}.yaml", "r") as f:
                self._config = Config.model_validate(yaml.safe_load(f))
        except Exception as e:
            print(f"Failed to parse config, {e}")
            raise

    def hue_config(self) -> Tuple[str, str]:
        return (
            self._config.hue.bridge_ip_address,
            os.environ[self._config.hue.username_key],
        )

    def outdoor_config(self) -> list[GradientLightConfig]:
        return self._config.lights.outdoor
