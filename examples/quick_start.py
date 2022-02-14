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
