import typing as t

import aiofiles
from Crypto.Cipher import AES
import ujson

from .core import TokenBundle
from .core import TokenStorage


__all__ = ["FileTokenStorage"]


class FileTokenStorage(TokenStorage):

    __slots__ = (
        "__filepath",
        "__cipher",
    )

    def __init__(
        self,
        filepath: str = "credentials.txt",
        encryption_key: str = "secret",
    ) -> None:
        self.__filepath = filepath
        self.__cipher = AES.new(encryption_key)

    async def _save_data(self, data: t.Mapping[str, t.Any]) -> None:
        encoded_string = self.__cipher.encrypt(ujson.dumps(data) * 16)
        async with aiofiles.open(self.__filepath, "wb") as afp:
            await afp.write(encoded_string)

    async def _recover_data(self) -> t.Mapping[str, t.Any]:
        try:
            async with aiofiles.open(self.__filepath, "rb") as afp:
                encoded_string = await afp.read()
                content = self.__cipher.decrypt(encoded_string)
                return ujson.loads(content[0: len(content) // 16])
        except (FileNotFoundError, ujson.JSONDecodeError, ValueError):
            return {}

    async def set_tokens(self, tokens: TokenBundle) -> None:
        await self._save_data(tokens._asdict())

    async def get_tokens(self) -> TokenBundle:
        try:
            return TokenBundle(**(await self._recover_data()))
        except TypeError:
            raise KeyError("The token storage is empty.")

    async def clear(self) -> None:
        await self._save_data({})
