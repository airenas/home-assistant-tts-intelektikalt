"""Constants for home-assistant-tts-intelektikalt."""
from enum import Enum
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

CONF_VOICE = "voice"
API_DOMAIN = "intelektikalt_tts"
API_TITLE = "Intelektika.lt TTS"
API_FORMAT = "mp3"
API_URL = "https://sinteze.intelektika.lt/synthesis.service/prod/synthesize"
API_LANGUAGE = "lt"


class VoiceEnum(Enum):
    LAIMIS = "laimis"
    LINA = "lina"
    ASTRA = "astra"
    VYTAUTAS = "vytautas"

    @classmethod
    def default(cls) -> "VoiceEnum":
        return cls.LAIMIS
