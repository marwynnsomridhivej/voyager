from typing import Union

_ATTRS = {
    'name',
    '2mass',
    'cd',
    'cpd',
    'gj',
    'hd',
    'hip',
    'hr',
    'iras',
    'sao',
    'tyc',
    'wise',
}


class ExoplanetAlias(object):
    __slots__ = [
        '_data',
    ]
    _cache = {}

    def __init__(self, data: list) -> None:
        self._data = data

    def _process_dict(self) -> dict:
        return {
            attr: value for attr in _ATTRS if (
                value := getattr(self, attr)
            )
        }

    @property
    def to_dict(self) -> dict:
        if (sf := f"{self}dict") not in self._cache:
            self._cache[sf] = self._process_dict()
        return self._cache[sf]

    @classmethod
    def from_dict(cls, data: dict) -> "ExoplanetAlias":
        _ATTRS = [
            'name',
            '2mass',
            'cd',
            'cpd',
            'gj',
            'hd',
            'hip',
            'hr',
            'iras',
            'sao',
            'tyc',
            'wise',
        ]
        send_data = {
            name.lower(): alias for name, alias in data.items()
            if alias and name.lower() in _ATTRS
        }
        return cls(send_data)


def _add_func(name: str):
    @property
    def fn(self) -> Union[str, None]:
        def _extract(attr: str) -> Union[str, None]:
            if attr == "name":
                return self._data[1].get("aliasdis")
            for alias in self._data:
                if not (s := alias.get("aliasdis")):
                    return None
                elif s.startswith(attr.upper()):
                    return s
            else:
                return None

        if name not in self._cache:
            self._cache[name] = _extract(name)
        return self._cache[name]
    setattr(ExoplanetAlias, name, fn)


for attr in _ATTRS:
    _add_func(attr)
