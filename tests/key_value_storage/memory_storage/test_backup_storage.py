import pytest

from amo_crm_api_client.storage.impl.instances.memory.impl.backup_storage import (
    BackupStorageFileConfigModel,
    BackupStorageFile,
)


@pytest.fixture()
def backup_storage(tmpdir):
    path = tmpdir.join("test_backup_file.txt")
    config = BackupStorageFileConfigModel(
        backup_file_path=str(path),
        encryption_key="test_secret",
    )
    return BackupStorageFile(
        config=config,
    )


@pytest.mark.asyncio
async def test_backup_storage_in_file(backup_storage):
    data = {
        "a": 121,
        "b": "string",
    }
    await backup_storage.save_data(data)
    recovered_data = await backup_storage.recover_data()
    assert recovered_data == data
