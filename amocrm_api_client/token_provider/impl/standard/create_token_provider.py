import functools as ft

from pydantic import BaseModel

from ...core import TokenProvider

from ..token_storage import FileTokenStorage
from ..authorization import exchange_auth_code_by_amocrm
from ..authorization import refresh_access_token_by_amocrm

from .DefaultTokenProvider import DefaultTokenProvider


__all__ = [
    "StandardTokenProviderConfig",
    "create_token_provider",
]


class StandardTokenProviderConfig(BaseModel):
    filepath: str = "backup.txt"
    encryption_key: str = "secret"

    integration_id: str
    secret_key: str
    auth_code: str
    base_url: str
    redirect_uri: str

def create_token_provider(config: StandardTokenProviderConfig) -> TokenProvider:
    token_storage = FileTokenStorage(
        filepath=config.filepath,
        encryption_key=config.encryption_key,
    )

    get_tokens = ft.partial(
        exchange_auth_code_by_amocrm,
        base_url=config.base_url,
        integration_id=config.integration_id,
        secret_key=config.secret_key,
        auth_code=config.auth_code,
        redirect_uri=config.redirect_uri,
    )

    refresh_tokens = ft.partial(
        refresh_access_token_by_amocrm,
        base_url=config.base_url,
        integration_id=config.integration_id,
        auth_code=config.auth_code,
        redirect_uri=config.redirect_uri,
    )

    return DefaultTokenProvider(
        get_tokens=get_tokens,
        refresh_tokens=refresh_tokens,
        token_storage=token_storage,
    )
