"""TTS Wrapper for intelektikalt TTS integration."""

import base64
import logging

import async_timeout
from homeassistant.components.tts import (
    Provider,
    TextToSpeechEntity,
    TtsAudioType,
    Voice,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from custom_components.intelektikalt_tts.const import (
    API_FORMAT,
    API_LANGUAGE,
    API_TITLE,
    API_URL,
    CONF_VOICE,
    VoiceEnum,
)
from custom_components.intelektikalt_tts.errors import ApiClientError, check_response

_LOGGER = logging.getLogger(__name__)


class AddEntitiesCallback:
    """Fake Callback for adding entities."""
    pass


async def async_get_engine(
        hass: HomeAssistant, config: dict, _discovery_info: dict | None = None
) -> Provider:
    """Return the TTS provider instance."""
    return IntelektikaLTTTSProvider(hass, config)


async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the intelektikalt TTS platform from a config entry."""
    async_add_entities(
        [
            IntelektikaLTTTSEntity(
                provider=IntelektikaLTTTSProvider(hass, config_entry.data)
            )
        ]
    )


class IntelektikaLTTTSProvider(Provider):
    """TTS provider for intelektikalt TTS service."""

    def __init__(self, hass: HomeAssistant, config: dict) -> None:
        """Initialize the TTS provider."""
        self._hass = hass
        self._language = API_LANGUAGE
        self._api_key = config.get("api_key")
        self._voice = VoiceEnum.default().value
        self._url = API_URL

    @property
    def default_language(self) -> str:
        """Return the default language of the TTS provider."""
        return self._language

    @property
    def language(self) -> str:
        """Return the language of the TTS provider."""
        return self._language

    @property
    def name(self) -> str:
        """Return the name of the TTS provider."""
        return API_TITLE

    @property
    def supported_languages(self) -> list[str]:
        """Return a list of supported languages."""
        return [self._language]

    async def async_get_tts_audio(
            self, message: str, _language: str, options: dict | None = None
    ) -> TtsAudioType:
        """Load TTS from intelektikalt."""
        try:
            selected_voice = options.get(CONF_VOICE) if options else None
            if not selected_voice:
                selected_voice = self._voice

            payload = {
                "text": message,
                "outputFormat": API_FORMAT,
                "outputTextFormat": "none",
                "saveRequest": False,
                "speed": 1,
                "voice": selected_voice,
            }
            headers = {"Authorization": f"Key {self._api_key}"} if self._api_key else {}

            _LOGGER.info("TTS request: %s", payload)

            async with async_timeout.timeout(10):
                session = async_get_clientsession(self._hass)
                async with session.post(
                        self._url, json=payload, headers=headers
                ) as resp:
                    check_response(resp)
                    data = await resp.json()
                    audio_bytes = base64.b64decode(data.get("audioAsString"))
                    return API_FORMAT, audio_bytes

        except HomeAssistantError:
            raise
        except Exception as e:
            raise ApiClientError(value=f"{e}") from e

    @property
    def supports_streaming(self) -> bool:
        """Return True if the provider supports streaming."""
        return False


class IntelektikaLTTTSEntity(TextToSpeechEntity):
    """Text to Speech entity for intelektikalt TTS provider."""

    def __init__(self, provider: IntelektikaLTTTSProvider) -> None:
        """Initialize the TTS entity."""
        self._provider = provider

    @property
    def default_language(self) -> str:
        """Return the default language."""
        return self._provider.default_language

    @property
    def supported_languages(self) -> list[str]:
        """Return list of supported languages."""
        return self._provider.supported_languages

    @property
    def name(self) -> str:
        """Return the name of the TTS provider."""
        return self._provider.name

    @property
    def supported_options(self) -> list[str]:
        """Return a list of supported options."""
        return [CONF_VOICE]

    @callback
    def async_get_supported_voices(self, language: str) -> list[Voice] | None:
        """Return a list of supported voices for a language."""
        if language == self._provider.language:
            return [
                Voice(voice_id=VoiceEnum.LAIMIS.value, name="Laimis"),
                Voice(voice_id=VoiceEnum.LINA.value, name="Lina"),
                Voice(voice_id=VoiceEnum.ASTRA.value, name="Astra"),
                Voice(voice_id=VoiceEnum.VYTAUTAS.value, name="Vytautas"),
            ]
        return None

    async def async_get_tts_audio(
            self, message: str, language: str, options: dict | None = None
    ) -> TtsAudioType:
        """Load TTS from intelektikalt."""
        return await self._provider.async_get_tts_audio(
            message=message, language=language, options=options
        )
