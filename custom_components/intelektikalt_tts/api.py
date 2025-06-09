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
