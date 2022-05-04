from urllib.parse import urljoin

from amocrm_api_client.make_json_request import IMakeJsonRequestFunction
from amocrm_api_client.make_json_request import RequestMethod

from ..core import ICheckAccessTokenFunction


__all__ = [
    "CheckAccessTokenFunction",
]


class CheckAccessTokenFunction(ICheckAccessTokenFunction):

    __slots__ = (
        "__make_json_request_function",
    )

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
