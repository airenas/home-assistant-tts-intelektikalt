import logging

import async_timeout
from homeassistant.components.tts import Provider
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)


async def async_get_engine(hass, config, discovery_info=None):
    """Return the TTS provider instance."""
    return IntelektikaLTTTSProvider(hass, config)


class IntelektikaLTTTSProvider(Provider):
    def __init__(self, hass, config):
        self._hass = hass
        self._language = "lt"
        self._api_key = config.get("api_key")
        self._voice = config.get("voice", "laimis")
        self._url = "https://sinteze.intelektika.lt/synthesis.service/prod/synthesize"

    @property
    def default_language(self):
        return self._language

    @property
    def supported_languages(self):
        return [self._language]

    async def async_get_tts_audio(self, message, language, options=None):
        try:
            payload = {"text": message,
                       "outputFormat": "wav",
                       "outputTextFormat": "none",
                       "saveRequest": False,
                       "speed": 1,
                       "voice": self._voice
                       }
            headers = {"Authorization": f"Key {self._api_key}"} if self._api_key else {}

            _LOGGER.info("TTS request: %s", payload)

            async with async_timeout.timeout(10):
                session = async_get_clientsession(self._hass)
                async with session.post(self._url, json=payload, headers=headers) as resp:
                    resp.raise_for_status()
                    data = await resp.read()
                    return ("audio/wav", data)

        except Exception as e:
            _LOGGER.error("Error fetching TTS audio: %s", e)
            return (None, None)

    @property
    def supports_streaming(self) -> bool:
        return False
