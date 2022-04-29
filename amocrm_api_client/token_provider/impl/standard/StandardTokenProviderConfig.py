from pydantic import BaseModel


__all__ = [
    "StandardTokenProviderConfig",
]


class StandardTokenProviderConfig(BaseModel):
    backup_file_path: str = "backup.txt"
    encryption_key: str = "secret"

    integration_id: str
    secret_key: str
    auth_code: str
    base_url: str
    redirect_uri: str
