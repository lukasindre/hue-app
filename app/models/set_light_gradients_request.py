from pydantic import BaseModel


class LightDimming(BaseModel):
    brightness: int


class GradientPointColorXY(BaseModel):
    x: float
    y: float


class GradientPointColor(BaseModel):
    xy: GradientPointColorXY


class GradientPoint(BaseModel):
    color: GradientPointColor


class Gradient(BaseModel):
    points: list[GradientPoint]


class Dynamics(BaseModel):
    duration: int


class SetLightGradientsRequest(BaseModel):
    # TODO: set light state to `on`
    dimming: LightDimming
    gradient: Gradient
    dynamics: Dynamics
