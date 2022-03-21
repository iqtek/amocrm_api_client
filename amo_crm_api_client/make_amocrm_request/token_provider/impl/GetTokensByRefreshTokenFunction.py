from urllib.parse import urljoin
from ...make_json_request import (
    IMakeJsonRequestFunction,
    RequestMethod,
)
from ..core import (
    RefreshTokenExpiredException,
    InvalidAuthorizationDataException,
    IGetTokensByRefreshTokenFunction,
    TokensBundle,
)


__all__ = [
    "GetTokensByRefreshTokenFunction",
]


class GetTokensByRefreshTokenFunction(IGetTokensByRefreshTokenFunction):

    def __init__(
        self,
        make_json_request_function: IMakeJsonRequestFunction,
    ) -> None:
        self.__make_json_request_function = make_json_request_function

    async def __call__(
        self,
        base_url: str,
        integration_id: str,
        secret_key: str,
        refresh_token: str,
        redirect_uri: str,
    ) -> TokensBundle:

        data = {
            "client_id": integration_id,
            "client_secret": secret_key,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "redirect_uri": redirect_uri,
        }

        oauth2_route = "oauth2/access_token/"
        url = urljoin(base_url, oauth2_route)

        headers = {"Content-Type": "application/json"}

        try:
            response = await self.__make_json_request_function(
                method=RequestMethod.POST,
                path=url,
                headers=headers,
                json=data
            )
        except Exception:
            raise InvalidAuthorizationDataException(
                "Error getting tokens using authorization code. "
                "Invalid 'base_url'. "
            )

        if response.status_code == 200:
            access_token = response.json["access_token"]
            refresh_token = response.json["refresh_token"]
            expires_in = response.json["expires_in"]

            return TokensBundle(
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
