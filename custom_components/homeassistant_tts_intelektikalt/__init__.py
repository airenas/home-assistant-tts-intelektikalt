"""
Custom integration to integrate IntelektikaLT TTS Service with Home Assistant.

For more details about this integration, please refer to
https://github.com/airenas/homeassistant_tts_intelektikalt
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN, LOGGER

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant


# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(
        _hass: HomeAssistant,
        _entry: ConfigEntry,
) -> bool:
    """Set up this integration using UI."""
    return True


async def async_unload_entry(
        _hass: HomeAssistant,
        _entry: ConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    return True
