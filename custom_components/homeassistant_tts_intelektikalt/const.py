"""Constants for homeassistant_tts_intelektikalt."""
from enum import Enum
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

CONF_VOICE = "voice"
API_DOMAIN = "homeassistant_tts_intelektikalt"
API_TITLE = "IntelektikaLT TTS"
API_FORMAT = "mp3"
API_URL = "https://sinteze.intelektika.lt/synthesis.service/prod/synthesize"
API_LANGUAGE = "lt"


class Voice(Enum):
    LAIMIS = "laimis"
    LINA = "lina"
    ASTRA = "astra"
    VYTAUTAS = "vytautas"

    @classmethod
    def default(cls) -> "Voice":
        return cls.LAIMIS
