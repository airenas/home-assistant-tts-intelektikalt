from typing import TYPE_CHECKING

from aiohttp import ClientResponseError
from homeassistant.exceptions import (
    HomeAssistantError

)


class ApiClientError(HomeAssistantError):
    """Exception to indicate a general API error."""

    def __init__(
            self, value: str
    ) -> None:
        """Initialize error."""
        if TYPE_CHECKING:
            value = str(value)
        super().__init__(
            translation_domain="homeassistant",
            translation_key="intelektikalt_api_error",
            translation_placeholders={
                "value": value,
            },
        )
        self.value = value
        self.generate_message = True


class WrongKeyError(HomeAssistantError):
    """Exception to indicate a bad key error."""

    def __init__(
            self
    ) -> None:
        """Initialize error."""
        super().__init__(
            translation_domain="homeassistant",
            translation_key="intelektikalt_wrong_key",
        )
        self.generate_message = True


class QuotaExceeded(HomeAssistantError):
    """Exception to indicate out of quota error."""

    def __init__(
            self, quota: int, remaining: int
    ) -> None:
        """Initialize error."""
        if TYPE_CHECKING:
            quota = str(quota)
            remaining = str(remaining)
        super().__init__(
            translation_domain="homeassistant",
            translation_key="intelektikalt_quota_exceeded",
            translation_placeholders={
                "quota": quota,
                "remaining": remaining,
            },
        )
        self.quota = quota
        self.remaining = remaining
        self.generate_message = True


def check_response(resp):
    try:
        resp.raise_for_status()
    except ClientResponseError as e:
        if e.status == 429:
            raise QuotaExceeded(remaining=e.headers.get('X-Rate-Limit-Short-Remaining', 0), quota=e.headers.get('X-Rate-Limit-Limit', 0))
        elif e.status == 403:
            raise QuotaExceeded(remaining=e.headers.get('X-Rate-Limit-Remaining', 0), quota=e.headers.get('X-Rate-Limit-Limit', 0))
        elif e.status == 401:
            raise WrongKeyError()
        else:
            raise ApiClientError(value=f"failed with status {e.status}: {e.message}")
    except Exception as e:
        raise ApiClientError(value=f"{e}")
