# Amocrm Api Client

Library for working with the main entities of amoCRM. With automatic authorization via OAuth 2.0.

***
+ Work with AmoCRM entities as Pydantic models
+ Inbuilt Rate Limiter
+ Inbuilt Request Repeater
+ Inbuilt key-value storage for  Access and  Refresh tokens
***

# Installation
```bash
pip install 
```
***
# Getting started

##  Create client 
Create a client using the pydantic model.
```python
import yaml

from amo_crm_api_client import (
    create_amo_crm_api_client,
    AmoCrmApiClient,
    AmoCrmApiClientConfig,
)

if __name__ == "__main__":

    with open('config.yml') as config_file:
        config = yaml.safe_load(config_file)

    amocrm_config = AmoCrmApiClientConfig(**config)

    amocrm_client = create_amo_crm_api_client(
        config=amocrm_config,
    )

```

## Using
If you are using MemoryStorage, then a call deinitialize() is required so that the storage data is saved to disk.

```python
import asyncio
import yaml

from amo_crm_api_client import (
    create_amo_crm_api_client,
    AmoCrmApiClient,
    AmoCrmApiClientConfig,
)


async def test(amocrm_client: AmoCrmApiClient) -> None:
    await amocrm_client.initialize()
    lead = await amocrm_client.leads.get_by_id(id=8756815)
    print(lead)
    await amocrm_client.deinitialize()


if __name__ == "__main__":

    with open('config.yml') as config_file:
        config = yaml.safe_load(config_file)

    amocrm_config = AmoCrmApiClientConfig(**config)

    amocrm_client = create_amo_crm_api_client(
        config=amocrm_config,
    )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test(amocrm_client))

```
***
## Example config.yml

```yaml
integration_id: xxxxxxxx-xxxx-xxxx-xxx-xxxxxxxxxxxx
secret_key: secret_key
auth_code: auth_code
redirect_uri: https://mycompany.ru/
base_url: https://account.amocrm.ru/

rate_limiter: 
  interval_length: 1 
  max_request_count: 7
  forced_delay: 1

repeater:
  tries: 5
  delay: 1.0
  max_delay: 5.0
  backoff: 0

storage:
  type: redis
  settings:
    host: 127.0.0.1
    port: 6379
    database: 1
    prefix: amocrm-api-client

```

# License

__Amocrm Api Client__  is offered under the MIT license.
