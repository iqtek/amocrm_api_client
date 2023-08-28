import typing as t

from aiofile import async_open
from Crypto import Cipher
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
        self.__cipher = Cipher.AES.new(encryption_key)

    async def _save_data(self, data: t.Mapping[str, t.Any]) -> None:
        encoded_string = self.__cipher.encrypt(ujson.dumps(data))
        async with async_open(self.__filepath, "w") as afp:
            await afp.write(encoded_string)

    async def _recover_data(self) -> t.Mapping[str, t.Any]:
        try:
            async with async_open(self.__filepath, "r") as afp:
                encoded_string = await afp.readline()
                return self.__cipher.encrypt(ujson.loads(encoded_string))
        except Exception:
            return {}

    async def set_tokens(self, tokens: TokenBundle) -> None:
        await self._save_data(tokens._asdict())

    async def get_tokens(self) -> TokenBundle:
        return TokenBundle(**(await self._recover_data()))

    async def clear(self) -> None:
        await self._save_data({})
