from urllib.parse import urljoin

import aiohttp

from ...core import RefreshTokenExpiredException

from .core import GetTokensByAuthCodeFunction
from .core import GetTokensByRefreshTokenFunction
from .core import TokenPair


__all__ = [
    "DefaultGetTokensByAuthCodeFunction",
    "DefaultGetTokensByRefreshTokenFunction",
]


class DefaultGetTokensByAuthCodeFunction(GetTokensByAuthCodeFunction):

    __slots__ = ()

    async def __call__(
        self,
        base_url: str,
        integration_id: str,
        secret_key: str,
        auth_code: str,
        redirect_uri: str,
    ) -> TokensBundle:
        payload = {
          "client_id":  integration_id,
          "client_secret": secret_key,
          "grant_type": "authorization_code",
          "code": auth_code,
          "redirect_uri": redirect_uri
        }

        oauth2_route = "oauth2/access_token"
        url = urljoin(base_url, oauth2_route)

        headers = {"Content-Type": "application/json"}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url=url,
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status_code == 200:
                        access_token = response.json["access_token"]
                        refresh_token = response.json["refresh_token"]
                        expires_in = response.json["expires_in"]

                        return TokenPair(
                            access_token=access_token,
                            refresh_token=refresh_token,
                            expires_in=expires_in,
                        )

                    title = response.json["title"]
                    detail = response.json["detail"]
                    hint = response.json.get("hint", "Without a hint")

                    if "Authorization" in hint:
                        raise RefreshTokenExpiredException()

                    raise InvalidAuthorizationDataException(
                        f"Error getting tokens using authorization code. "
                        f"{title}. {detail}. {hint}."
                    )
        except aiohttp.ClientConnectorError as exc:
            raise InvalidAuthorizationDataException("Invalid 'base_url'.") from exc


class DefaultGetTokensByRefreshTokenFunction(GetTokensByRefreshTokenFunction):

    __slots__ = ()

    async def __call__(
        self,
        base_url: str,
        integration_id: str,
        secret_key: str,
        refresh_token: str,
        redirect_uri: str,
    ) -> TokensBundle:
        payload = {
            "client_id": integration_id,
            "client_secret": secret_key,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "redirect_uri": redirect_uri,
        }

        oauth2_route = "oauth2/access_token"
        url = urljoin(base_url, oauth2_route)

        headers = {"Content-Type": "application/json"}

        try:
            async with session.post(
                url=url,
                headers=headers,
                json=payload,
            ) as response:
                if response.status_code == 200:
                    access_token = response.json["access_token"]
                    refresh_token = response.json["refresh_token"]
                    expires_in = response.json["expires_in"]

                    return TokenPair(
                        access_token=access_token,
                        refresh_token=refresh_token,
                        expires_in=expires_in,
                    )

                title = response.json["title"]
                detail = response.json["detail"]
                hint = response.json.get("hint", "Without a hint")

                if "Refresh" in hint:
                    raise RefreshTokenExpiredException()

                raise InvalidAuthorizationDataException(
                    f"Error getting tokens using authorization code. "
                    f"{title}. {detail}. {hint}."
                )
        except aiohttp.ClientConnectorError as exc:
            raise InvalidAuthorizationDataException("Invalid 'base_url'.") from exc
