from urllib.parse import urljoin
import aiohttp

from ...core import *

from .core import TokenPair


__all__ = [
    "exchange_auth_code_by_amocrm",
    "refresh_access_token_by_amocrm",
]


async def exchange_auth_code_by_amocrm(
    base_url: str,
    integration_id: str,
    secret_key: str,
    auth_code: str,
    redirect_uri: str,
) -> TokenPair:
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
                body = await response.json()
                hint = body.get("hint", "")

                if "Check the `client_secret` parameter" in hint:
                    raise InvalidClientSecretException()

                if "Redirect URI is not associated with client" in hint:
                    raise InvalidRedirectUriException()

                if "Cannot decrypt the authorization code" in hint:
                    raise InvalidAuthorizationCodeException()

                if "Authorization code has expired" in hint:
                    raise AuthorizationCodeExpiredException()

                return TokenPair(
                    access_token=body["access_token"],
                    refresh_token=body["refresh_token"],
                    expires_in=body["expires_in"],
                )
    except aiohttp.ClientConnectorError as exc:
        raise InvalidAuthorizationCodeException("Invalid 'base_url'.") from exc


async def refresh_access_token_by_amocrm(
    base_url: str,
    integration_id: str,
    secret_key: str,
    refresh_token: str,
    redirect_uri: str,
) -> TokenPair:
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
            if response.status == 200:
                body = await response.json()

                access_token = body["access_token"]
                refresh_token = body["refresh_token"]
                expires_in = body["expires_in"]

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
