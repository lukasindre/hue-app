from app.services.config_service import ConfigService
from app.services.hue_service import HueService
from app.services.christmas_service import ChristmasService


def get_config_service() -> ConfigService:
    return ConfigService()


def get_hue_service() -> HueService:
    config = get_config_service()
    return HueService(config)


def get_christmas_service() -> ChristmasService:
    config = get_config_service()
    hue = get_hue_service()
    return ChristmasService(hue, config)
