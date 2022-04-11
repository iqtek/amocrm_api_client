from amo_crm_api_client.AmoCrmApiClientConfig import AmoCrmApiClientConfig
from amo_crm_api_client.logger import ILogger
from amo_crm_api_client.storage import IKeyValueStorage
from .make_amocrm_request import IMakeAmocrmRequestFunction
from .make_amocrm_request import MakeAmocrmRequestFunctionImpl
from .make_json_request import MakeJsonRequestFunctionImpl
from .token_provider import GetAccessTokenFunctionImpl
from .token_provider.impl import (
    CheckAccessTokenFunction,
    GetTokensByAuthCodeFunction,
    GetTokensByRefreshTokenFunction,
)


__all__ = [
    "handle_startup",
]


def handle_startup(
    config: AmoCrmApiClientConfig,
    storage: IKeyValueStorage,
    logger: ILogger,
) -> IMakeAmocrmRequestFunction:

    make_json_request_function = MakeJsonRequestFunctionImpl(
        logger=logger,
    )

    get_access_token_function = GetAccessTokenFunctionImpl(
        config=config,
        get_tokens_by_auth_code=GetTokensByAuthCodeFunction(make_json_request_function),
        get_tokens_by_refresh_token=GetTokensByRefreshTokenFunction(make_json_request_function),
        check_access_token_function=CheckAccessTokenFunction(make_json_request_function),
        storage=storage,
        logger=logger,
    )

    make_amocrm_request_function = MakeAmocrmRequestFunctionImpl(
        base_url=config.base_url,
        get_access_token_function=get_access_token_function,
        make_json_request_function=make_json_request_function,
    )

    return make_amocrm_request_function