from pydantic import BaseModel


class Brightness(BaseModel):
    brightness: int


class Duration(BaseModel):
    duration: int


class LightFadeOutRequest(BaseModel):
    dimming: Brightness
    dynamics: Duration
