"""Adds config flow for IntelektikaLT TTS."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_USERNAME, CONF_API_KEY
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from slugify import slugify

from .api import IntelektikaLTTTSApiClientError, IntelektikaLTTTSApiClientCommunicationError, \
    IntelektikaLTTTSApiClientAuthenticationError, IntelektikaLTTTSApiClient
from .const import DOMAIN, LOGGER, CONF_VOICE, Voice


class IntelektikaLTTTSFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for IntelektikaLT TTS."""

    VERSION = 1

    async def async_step_user(
            self,
            user_input: dict | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                await self._test_credentials(
                    username=user_input[CONF_API_KEY],
                    password=user_input[CONF_VOICE],
                )
            except IntelektikaLTTTSApiClientAuthenticationError as exception:
                LOGGER.warning(exception)
                _errors["base"] = "auth"
            except IntelektikaLTTTSApiClientCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except IntelektikaLTTTSApiClientError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(
                    ## Do NOT use this in production code
                    ## The unique_id should never be something that can change
                    ## https://developers.home-assistant.io/docs/config_entries_config_flow_handler#unique-ids
                    unique_id=slugify(user_input[CONF_USERNAME])
                )
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=user_input[CONF_USERNAME],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_API_KEY): selector.TextSelector(
                        selector.TextSelectorConfig(type=selector.TextSelectorType.PASSWORD)
                    ),
                    vol.Required(CONF_VOICE, default= Voice.LAIMIS.value): selector.SelectSelector(
                        selector.SelectSelectorConfig(
                            options=[ Voice.LAIMIS.value,  Voice.ASTRA.value,  Voice.LINA.value,  Voice.VYTAUTAS.value],
                            mode=selector.SelectSelectorMode.DROPDOWN,
                        )
                    )
                },
            ),
            errors=_errors,
        )

    async def _test_credentials(self, key: str, voice: str) -> None:
        """Validate key."""
        client = IntelektikaLTTTSApiClient(
            key=key,
            voice=voice,
            session=async_create_clientsession(self.hass),
        )
        await client.async_test()
