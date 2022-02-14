from amo_crm_api_client.storage import (
    IKeyValueStorage,
)
from amo_crm_api_client.logger import (
    ILogger,
)
from ...core import (
    RequestMethod,
    IMakeJsonRequestFunction,
    IGetAccessTokenFunction,
)
from ..requests import make_url
from amo_crm_api_client.AmoCrmApiClientConfig import AmoCrmApiClientConfig


__all__ = [
    "GetAccessTokenFunctionImpl",
]


class GetAccessTokenFunctionImpl(IGetAccessTokenFunction):

    __ACCESS_TOKEN_KEY: str = "access_token"
    __ACCESS_TOKEN_TTL: int = 60 * 60 * 23
    __REFRESH_TOKEN_KEY: str = "refresh_token"
    __REFRESH_TOKEN_TTL: int = 60 * 60 * 24 * 88
    __DEFAULT_REQUEST_TIMEOUT: float = 10.0

    def __init__(
        self,
        config: AmoCrmApiClientConfig,
        make_json_request: IMakeJsonRequestFunction,
        storage: IKeyValueStorage,
        logger: ILogger,
    ) -> None:
        self.__config = config
        self.__make_json_request = make_json_request
        self.__storage = storage
        self.__logger = logger

    async def __call__(self):
        try:
            access_token = await self.__get_access_token_from_storage()
        except Exception as e:
            access_token = None

        if access_token:
            try:
                await self.__make_test_request(access_token=access_token)
            except ValueError:
                await self.__logger.info(f"Access token in storage not valid.")
                access_token = None

        if access_token is None:
            await self.__logger.info(f"Access token not found.")
            try:
                refresh_token = await self.__get_refresh_token_from_storage()
            except Exception as e:
                refresh_token = None

            if refresh_token is None:
                await self.__logger.info(f"Refresh token not found.")
                access_token = await self.__get_access_token_with_authorization_code()
                return access_token
            else:
                await self.__logger.info(f"Refresh token found.")
                access_token = await self.__get_access_token_with_refresh_token(refresh_token)
                return access_token

        return access_token

    async def __get_access_token_from_storage(self) -> str:
        return await self.__storage.get(self.__ACCESS_TOKEN_KEY)

    async def __set_access_token_to_storage(self, access_token: str) -> None:
        try:
            await self.__storage.set(self.__ACCESS_TOKEN_KEY, access_token, expire=self.__ACCESS_TOKEN_TTL)
        except Exception:
            await self.__storage.update(self.__ACCESS_TOKEN_KEY, access_token, expire=self.__ACCESS_TOKEN_TTL)

    async def __get_refresh_token_from_storage(self) -> str:
        return await self.__storage.get(self.__REFRESH_TOKEN_KEY)

    async def __set_refresh_token_to_storage(self, refresh_token: str) -> None:
        try:
            await self.__storage.set(self.__REFRESH_TOKEN_KEY, refresh_token, expire=self.__REFRESH_TOKEN_TTL)
        except Exception:
            await self.__storage.update(self.__REFRESH_TOKEN_KEY, refresh_token, expire=self.__REFRESH_TOKEN_TTL)

    async def __get_access_token_with_authorization_code(self) -> str:
        base = self.__config.base_url
        oauth2_route = "oauth2/access_token/"
        url = make_url(base, oauth2_route)

        headers = {"Content-Type": "application/json"}

        data = {
            "client_id": self.__config.integration_id,
            "client_secret": self.__config.secret_key,
            "grant_type": "authorization_code",
            "code": self.__config.auth_code,
            "redirect_uri": self.__config.redirect_uri,
        }
        try:
            response = await self.__make_json_request(
                RequestMethod.POST,
                url,
                headers=headers,
                json=data
            )
            await self.__logger.error(
                "GetAccessTokenFunctionImpl: response "
                f"{response.json}. ",
            )
            access_token = response.json["access_token"]
            refresh_token = response.json["refresh_token"]
            await self.__set_access_token_to_storage(access_token)
            await self.__set_refresh_token_to_storage(refresh_token)

        except KeyError as key_error:
            await self.__logger.error(
                "Failed get access token from response.",
            )
            raise key_error

        except Exception as set_exception:
            await self.__logger.error("Failed to get access token.")
            raise set_exception
        else:
            await self.__logger.info("Get access token by authorization code.")

        return access_token

    async def __get_access_token_with_refresh_token(self, refresh_token: str) -> str:

        base = self.__config.base_url
        oauth2_route = "oauth2/access_token/"
        url = make_url(base, oauth2_route)

        headers = {"Content-Type": "application/json"}

        data = {
            "client_id": self.__config.integration_id,
            "client_secret": self.__config.secret_key,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "redirect_uri": self.__config.redirect_uri,
        }
        try:
            response = await self.__make_json_request(RequestMethod.POST, url, headers=headers, json=data)
            access_token = response.json["access_token"]
            refresh_token = response.json["refresh_token"]

            await self.__set_access_token_to_storage(access_token)
            await self.__set_refresh_token_to_storage(refresh_token)

        except KeyError as key_error:
            await self.__logger.error(f"Failed get refresh token from response.")
            raise key_error

        except Exception as set_exception:
            await self.__logger.error(f"Failed to get refresh token.")
            raise set_exception
        else:
            await self.__logger.info(f"Get access token by refresh token.")
        return access_token

    async def __make_test_request(self, access_token: str) -> None:
        """
        Tests the access token for validity.
        :param access_token: access token to verify
        :return:
        :raise ValueError: If access token is not valid.
        """
        base = self.__config.base_url
        oauth2_route = "/api/v4/account"
        url = make_url(base, oauth2_route)
        headers = {"Authorization": f"Bearer {access_token}"}
        try:
            response = await self.__make_json_request(
                RequestMethod.GET,
                url,
                headers=headers,
            )
        except Exception:
            raise ValueError("Access token is not valid.")
        if response.status_code == 401:
            raise ValueError("Access token is not valid.")
