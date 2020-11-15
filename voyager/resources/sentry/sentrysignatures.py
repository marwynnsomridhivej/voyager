from typing import Union


class SentrySignature(object):
    __slots__ = [
        '_source',
        '_version'
        '_data',
    ]

    def __init__(self, data: dict) -> None:
        self._source = data.get("source")
        try:
            self._version = int(data.get("version"))
        except ValueError:
            self._version = data.get("version")
        self._data = data

    @property
    def source(self) -> str:
        return self._source

    @property
    def version(self) -> Union[int, str]:
        return self._version

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "SentrySignature":
        return cls(data)
