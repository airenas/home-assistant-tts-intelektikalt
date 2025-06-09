import base64
import logging

import async_timeout
from homeassistant.components.tts import Provider, TextToSpeechEntity, Voice
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.typing import ConfigType

from custom_components.homeassistant_tts_intelektikalt.const import CONF_VOICE, API_URL, API_TITLE, API_LANGUAGE, \
    API_FORMAT, VoiceEnum

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
        _LOGGER.info(f"Init {__name__}")
        self._hass = hass
        self._language = API_LANGUAGE
        self._api_key = config_entry.get("api_key")
        self._voice = config_entry.get(CONF_VOICE, VoiceEnum.default().value)
        _LOGGER.info(f"Using voice: {self._voice}")
        self._url = API_URL

    @property
    def default_language(self) -> str:
        """Return the default language."""
        return self._language

    @property
    def supported_languages(self) -> list[str]:
        """Return list of supported languages."""
        return [self._language]

    @property
    def name(self):
        return API_TITLE

    @property
    def supported_options(self) -> list[str]:
        """Return a list of supported options."""
        return [CONF_VOICE]

    @callback
    def async_get_supported_voices(self, language: str) -> list[Voice] | None:
        """Return a list of supported voices for a language."""
        if language == self._language:  # Assuming `self._language` is the default language
            return [
                Voice(voice_id="laimis", name="Laimis"),
                Voice(voice_id="lina", name="Lina"),
                Voice(voice_id="astra", name="Astra"),
                Voice(voice_id="vytautas", name="Vytautas"),
            ]
        return None

    async def async_get_tts_audio(self, message, language, options=None):
        try:
            selected_voice = options.get(CONF_VOICE) if options
            if selected_voice:
                selected_voice = selected_voice.voice_id
            else:
                selected_voice = self._voice

            payload = {"text": message,
                       "outputFormat": API_FORMAT,
                       "outputTextFormat": "none",
                       "saveRequest": False,
                       "speed": 1,
                       "voice": selected_voice
                       }
            headers = {"Authorization": f"Key {self._api_key}"} if self._api_key else {}

            _LOGGER.info("TTS request: %s", payload)

            async with async_timeout.timeout(10):
                session = async_get_clientsession(self._hass)
                async with session.post(self._url, json=payload, headers=headers) as resp:
                    resp.raise_for_status()
                    data = await resp.json()
                    audio_bytes = base64.b64decode(data.get("audioAsString"))
                    return API_FORMAT, audio_bytes

        except Exception as e:
            _LOGGER.error("Error fetching TTS audio: %s", e)
            return None, None


class IntelektikaLTTTSProvider(Provider):
    def __init__(self, hass, config):
        _LOGGER.info(f"Init {__name__}")
        self._hass = hass
        self._language = API_LANGUAGE
        self._api_key = config.get("api_key")
        self._voice = config.get(CONF_VOICE, VoiceEnum.default().value)
        self._url = API_URL

    @property
    def default_language(self):
        return self._language

    @property
    def name(self):
        return API_TITLE

    @property
    def supported_languages(self):
        return [self._language]

    async def async_get_tts_audio(self, message, language, options=None):
        try:
            selected_voice = options.get(CONF_VOICE) if options
            if selected_voice:
                selected_voice = selected_voice.voice_id
            else:
                selected_voice = self._voice

            payload = {"text": message,
                       "outputFormat": API_FORMAT,
                       "outputTextFormat": "none",
                       "saveRequest": False,
                       "speed": 1,
                       "voice": selected_voice
                       }
            headers = {"Authorization": f"Key {self._api_key}"} if self._api_key else {}

            _LOGGER.info("TTS request: %s", payload)

            async with async_timeout.timeout(10):
                session = async_get_clientsession(self._hass)
                async with session.post(self._url, json=payload, headers=headers) as resp:
                    resp.raise_for_status()
                    data = await resp.json()
                    audio_bytes = base64.b64decode(data.get("audioAsString"))
                    return API_FORMAT, audio_bytes

        except Exception as e:
            _LOGGER.error("Error fetching TTS audio: %s", e)
            return None, None

    @property
    def supports_streaming(self) -> bool:
        return False
