import json
from os.path import exists
from asyncio import Lock


class SharedStrDict:
    __data: dict[str, str]

    def __init__(self, data=None):
        if data is None:
            data = {}
        self.__data = data
        self.__lock = Lock()

    async def clone_data(self) -> dict[str, str]:
        return await self.__over_dict(dict.copy)

    async def append(self, key: str, value: str) -> None:
        def __append(d: dict[str, str]) -> None:
            d[key] = value

        await self.__over_dict(__append)

    async def get(self, key: str) -> str | None:
        def __get(d: dict[str, str]) -> str | None:
            return d.get(key)

        return await self.__over_dict(__get)

    async def __over_dict(self, fun):
        await self.__lock.acquire()
        try:
            return fun(self.__data)
        finally:
            self.__lock.release()


__path = 'data/abbr.json'
__dict_key = 'dict'


def load_dict() -> SharedStrDict:
    if exists(__path):
        with open(__path, 'r', encoding='utf-8') as f:
            raw = json.load(f)
            data = raw[__dict_key]
            return SharedStrDict(data)
    else:
        return SharedStrDict()


async def save_dict(shared_dict: SharedStrDict) -> None:
    copy = await shared_dict.clone_data()
    with open(__path, 'w', encoding='utf-8') as f:
        json.dump({__dict_key: copy}, f, ensure_ascii=False)

