from typing import (
    Mapping,
    Any,
)
from amo_crm_api_client.logger import (
    ILogger,
)
from amo_crm_api_client.storage import (
    IKeyValueStorage,
)
from ..core import (
    IMakeAmocrmRequestFunction,
)
from .requests import (
    MakeAmocrmRequestFunctionImpl,
    MakeJsonRequestFunctionImpl,
)
from .tokens import (
    GetAccessTokenFunctionImpl,
)
from amo_crm_api_client.AmoCrmApiClientConfig import AmoCrmApiClientConfig


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
        make_json_request=make_json_request_function,
        storage=storage,
        logger=logger,
    )

    make_amocrm_request_function = MakeAmocrmRequestFunctionImpl(
        base_url=config.base_url,
        get_access_token_function=get_access_token_function,
        make_json_request_function=make_json_request_function,
    )

    return make_amocrm_request_function
