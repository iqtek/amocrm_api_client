from urllib.parse import urljoin

from ..core import ICheckAccessTokenFunction
from ...make_json_request import IMakeJsonRequestFunction, RequestMethod


__all__ = [
    "CheckAccessTokenFunction",
]


class CheckAccessTokenFunction(ICheckAccessTokenFunction):

    def __init__(
        self,
        make_json_request_function: IMakeJsonRequestFunction,
    ) -> None:
        self.__make_json_request_function = make_json_request_function

    async def __call__(
        self,
        base_url: str,
        access_token: str
    ) -> bool:
        url = urljoin(base_url, "/api/v4/account")

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        response = await self.__make_json_request_function(
            method=RequestMethod.GET,
            path=url,
            headers=headers,
        )
        if response.status_code == 200:
            return True

        return False
