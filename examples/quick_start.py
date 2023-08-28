from asyncio import get_event_loop

from amocrm_api_client import AmoCrmApiClient
from amocrm_api_client import AmoCrmApiClientConfig
from amocrm_api_client import create_amocrm_api_client
from amocrm_api_client.token_provider import StandardTokenProviderFactory


async def main() -> None:

    base_url = "https://iqtekdev.amocrm.ru/"

    settings = {
        "backup_file_path": "./credentials.txt",
        "encryption_key": "asterisk_ng",
        "integration_id": "cf086dcc-6d5a-4c8a-9c73-0aefa84b657c",
        "secret_key": "LVt49pTDf9HM1luo2xGmL4JDRZCLWya4LhOmeV9CZ4Z4GDgiRWaEL0U6QcMHg3T9",
        "auth_code": "auth_code",
        "base_url": "https://iqtekdev.amocrm.ru/",
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
    contacts_page = await amo_client.users.get_page()
    print(contacts_page)
    await amo_client.deinitialize()


if __name__ == "__main__":
    event_loop = get_event_loop()
    event_loop.run_until_complete(main())
