from typing import Union


class NASAMediaLink(object):
    __slots__ = [
        '_prompt',
        '_rel',
        '_href',
        '_render',
        '_data',
    ]

    def __init__(self, data: dict) -> None:
        self._prompt = data.get("prompt")
        self._rel = data.get("rel")
        self._href = data.get("href")
        self._render = data.get("render")
        self._data = data

    @property
    def prompt(self) -> Union[str, None]:
        return self._prompt

    @property
    def ref(self) -> Union[str, None]:
        return self._rel

    @property
    def href(self) -> Union[str, None]:
        return self._href

    @property
    def url(self) -> Union[str, None]:
        return self.href

    @property
    def render(self) -> Union[str, None]:
        return self._render

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "NASAMediaLink":
        return cls(data)
