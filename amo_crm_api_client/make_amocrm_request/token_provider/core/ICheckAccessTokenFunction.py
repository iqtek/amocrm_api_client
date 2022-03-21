__all__ = [
    "ICheckAccessTokenFunction",
]


class ICheckAccessTokenFunction:

    def __call__(
        self,
        base_url: str,
        access_token: str
    ) -> bool:
        """
        Check if the access token is currently valid.
        :param base_url: account base url.
        :param access_token: access_token.
        :return: bool
        """
        raise NotImplementedError()
