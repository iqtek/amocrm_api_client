# Amocrm Api Client

Library for working with the main entities of amoCRM. With automatic authorization via OAuth 2.0.

***
+ Work with AmoCRM entities as Pydantic models.
+ Inbuilt Rate Limiter.
+ Inbuilt Request Repeater.
+ Inbuilt key-value storage for  Access and  Refresh tokens.
***

# Installation
```bash
pip install git+https://github.com/iqtek/amocrm_api_client.git@v2.0.5
```
***
# Getting started

##  Create token provider
Token Provider - a callable object that returns an **access token** as a string. Thanks to this, you can store tokens anywhere. The Provider token is passed to the AmoCrmApiClient constructor.

The standard implementation stores tokens in a file containing a dictionary encrypted with JWT.

```python
settings = {
    "backup_file_path": "./backup_file",
    "encryption_key": "my_key_for_encrypting_tokens",
    "integration_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "secret_key": "secret_key",
    "auth_code": "auth_code",
    "base_url": "https://mycompany.amocrm.ru/",
    "redirect_uri": "https://mycompany.ru/",
}
token_provider_factory = StandardTokenProviderFactory()
token_provider = token_provider_factory.get_instance(settings=settings)
```

##  Create client 
Create a client using the pydantic config model.
If desired, you can configure a request repeater and a rate limiter.

```python
from asyncio import get_event_loop

from amocrm_api_client import AmoCrmApiClient
from amocrm_api_client import AmoCrmApiClientConfig
from amocrm_api_client import create_amocrm_api_client
from amocrm_api_client.token_provider import StandardTokenProviderFactory

settings = {
    "backup_file_path": "./backup_file",
    "encryption_key": "my_key_for_encrypting_tokens",
    "integration_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "secret_key": "secret_key",
    "auth_code": "auth_code",
    "base_url": "https://mycompany.amocrm.ru/",
    "redirect_uri": "https://mycompany.ru/",
}
# Create a standard token provider
token_provider_factory = StandardTokenProviderFactory()
token_provider = token_provider_factory.get_instance(settings=settings)

amo_client: AmoCrmApiClient = create_amocrm_api_client(
	token_provider=token_provider,
	config=AmoCrmApiClientConfig(base_url=base_url),
)

```

## Using
Get account information!

```python
await amo_client.initialize()
info = await amo_client.account.get_info()
print(info)
await amo_client.deinitialize()

```

# License

__Amocrm Api Client__  is offered under the MIT license.
