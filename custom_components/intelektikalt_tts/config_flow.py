"""Adds config flow for IntelektikaLT TTS."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY
from homeassistant.helpers import selector

from .const import API_DOMAIN, API_TITLE


class IntelektikaLTTTSFlowHandler(config_entries.ConfigFlow, domain=API_DOMAIN):
    """Config flow for Intelektika.lt TTS."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            await self.async_set_unique_id(API_DOMAIN)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=API_TITLE, data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_API_KEY): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.PASSWORD
                        )
                    )
                }
            ),
            errors=_errors,
        )
