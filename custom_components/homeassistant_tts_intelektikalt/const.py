"""Constants for homeassistant_tts_intelektikalt."""
from enum import Enum
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

CONF_VOICE = "voice"

DOMAIN = "homeassistant_tts_intelektikalt"

TITLE = "IntelektikaLT TTS"

URL = "https://sinteze.intelektika.lt/synthesis.service/prod/synthesize"

class Voice(Enum):
    LAIMIS = "laimis"
    LINA = "lina"
    ASTRA = "astra"
    VYTAUTAS = "vytautas"
