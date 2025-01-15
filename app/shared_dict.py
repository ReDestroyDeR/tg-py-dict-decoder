import json
from os.path import exists


class SharedStrDict:
    __data: dict[str, str]

    def __init__(self, data=None):
        if data is None:
            data = {}
        self.__data = data

    def get(self, key: str) -> str | None:
        return self.__data.get(key)


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
