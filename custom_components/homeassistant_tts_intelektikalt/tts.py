import logging

import async_timeout
from homeassistant.components.tts import Provider, TextToSpeechEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.typing import ConfigType

from custom_components.homeassistant_tts_intelektikalt.const import CONF_VOICE, URL

_LOGGER = logging.getLogger(__name__)


async def async_get_engine(hass, config, discovery_info=None):
    """Return the TTS provider instance."""
    return IntelektikaLTTTSProvider(hass, config)


async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities,
) -> None:
    async_add_entities([IntelektikaLTTTSEntity(hass, config_entry.data)])


class IntelektikaLTTTSEntity(TextToSpeechEntity):
    def __init__(self, hass: HomeAssistant, config_entry: ConfigType) -> None:
        self._hass = hass
        self._language = "lt"
        self._api_key = config_entry.get("api_key")
        self._voice = config_entry.get(CONF_VOICE, "laimis")
        self._url = URL

    @property
    def default_language(self) -> str:
        """Return the default language."""
        return self._language

    @property
    def supported_languages(self) -> list[str]:
        """Return list of supported languages."""
        return [self._language]

    @property
    def supported_options(self) -> list[str]:
        """Return a list of supported options."""
        return []

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
                    return "audio/wav", data

        except Exception as e:
            _LOGGER.error("Error fetching TTS audio: %s", e)
            return None, None


class IntelektikaLTTTSProvider(Provider):
    def __init__(self, hass, config):
        self._hass = hass
        self._language = "lt"
        self._api_key = config.get("api_key")
        self._voice = config.get(CONF_VOICE, "laimis")
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
