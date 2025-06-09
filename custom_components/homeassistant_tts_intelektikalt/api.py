"""Sample API Client."""

from __future__ import annotations

import socket
from typing import Any

import aiohttp
import async_timeout

from custom_components.homeassistant_tts_intelektikalt.const import URL


class IntelektikaLTTTSApiClientError(Exception):
    """Exception to indicate a general API error."""


class IntelektikaLTTTSApiClientCommunicationError(
    IntelektikaLTTTSApiClientError,
):
    """Exception to indicate a communication error."""


class IntelektikaLTTTSApiClientAuthenticationError(
    IntelektikaLTTTSApiClientError,
):
    """Exception to indicate an authentication error."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Verify that the response is valid."""
    if response.status in (401, 403):
        msg = "Invalid credentials"
        raise IntelektikaLTTTSApiClientAuthenticationError(
            msg,
        )
    response.raise_for_status()


class IntelektikaLTTTSApiClient:
    """IntelektikaLT TTS API Client."""

    def __init__(
            self,
            key: str,
            voice: str,
            session: aiohttp.ClientSession,
    ) -> None:
        self._key = key
        self._voice = voice
        self._session = session

    async def async_test(self) -> Any:
        return await self._api_wrapper(
            text="Testas",
        )

    async def _api_wrapper(
            self,
            text: str,
    ) -> Any:
        """Call API."""
        try:
            headers = {
                "Content-Type": "application/json",
            }
            if self._key:
                headers["Authorization"] = f"Key {self._key}"
            data = {"text": text,
                    "outputFormat": "wav",
                    "outputTextFormat": "none",
                    "saveRequest": False,
                    "speed": 1,
                    "voice": self._voice
                    }

            async with async_timeout.timeout(10):

                response = await self._session.request(
                    method="post",
                    url=URL,
                    headers=headers,
                    json=data,
                )
                _verify_response_or_raise(response)
                return await response.json()

        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise IntelektikaLTTTSApiClientCommunicationError(
                msg,
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise IntelektikaLTTTSApiClientCommunicationError(
                msg,
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Something really wrong happened! - {exception}"
            raise IntelektikaLTTTSApiClientError(
                msg,
            ) from exception
