from typing import Any
from typing import Mapping

from amocrm_api_client.make_json_request import MakeJsonRequestFunctionImpl

from .data_storage import DataStorageImpl
from .StandardTokenProvider import StandardTokenProvider
from .StandardTokenProviderConfig import StandardTokenProviderConfig
from ..GetTokensByAuthCodeFunction import GetTokensByAuthCodeFunction
from ..GetTokensByRefreshTokenFunction import GetTokensByRefreshTokenFunction
from ...core import ITokenProvider


__all__ = [
    "StandardTokenProviderFactory",
]


class StandardTokenProviderFactory:

    __slots__ = ()

    def get_instance(self, settings: Mapping[str, Any]) -> ITokenProvider:

        config = StandardTokenProviderConfig(**settings)

        data_storage = DataStorageImpl(
            backup_file_path=config.backup_file_path,
            encryption_key=config.encryption_key,
        )

        make_json_request_function = MakeJsonRequestFunctionImpl()

        get_tokens_by_auth_code_function = GetTokensByAuthCodeFunction(
            make_json_request_function=make_json_request_function,
        )

        get_tokens_by_refresh_token_function = GetTokensByRefreshTokenFunction(
            make_json_request_function=make_json_request_function,
        )

        token_provider = StandardTokenProvider(
            config=config,
            get_tokens_by_auth_code=get_tokens_by_auth_code_function,
            get_tokens_by_refresh_token=get_tokens_by_refresh_token_function,
            data_storage=data_storage,
        )

        return token_provider
