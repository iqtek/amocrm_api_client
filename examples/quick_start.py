from asyncio import get_event_loop

from amocrm_api_client import AmoCrmApiClient
from amocrm_api_client import AmoCrmApiClientConfig
from amocrm_api_client import create_amocrm_api_client
from amocrm_api_client.token_provider import StandardTokenProviderFactory


async def main() -> None:

    base_url = "https://iqtekdev.amocrm.ru/"

    settings = {
        "backup_file_path": "./backup_file",
        "encryption_key": "my_key_for_encrypting_tokens",
        "integration_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        "secret_key": "secret_key",
        "auth_code": "auth_code",
        "base_url": "https://mycompany.amocrm.ru/",
        "redirect_uri": "https://mycompany.ru/",
    }

    # Create a standard token provider.
    token_provider_factory = StandardTokenProviderFactory()
    token_provider = token_provider_factory.get_instance(settings=settings)

    amo_client: AmoCrmApiClient = create_amocrm_api_client(
        token_provider=token_provider,
        config=AmoCrmApiClientConfig(base_url=base_url)
    )

    await amo_client.initialize()
    info = await amo_client.account.get_info()
    print(info)
    await amo_client.deinitialize()


if __name__ == "__main__":
    event_loop = get_event_loop()
    event_loop.run_until_complete(main())
