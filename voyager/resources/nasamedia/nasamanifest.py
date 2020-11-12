from typing import Generator, Union


class NASAManifest(object):
    __slots__ = [
        '_data',
    ]

    def __init__(self, data: dict) -> None:
        self._data = data

    @property
    def href(self) -> str:
        return self._data.get("href")

    @property
    def url(self) -> str:
        return self.href

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "NASAManifest":
        return cls(data)


class NASAManifestCollection(object):
    __slots__ = [
        '_version',
        '_href',
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict) -> None:
        self._version = data.get("version")
        self._href = data.get("href")
        self._data = data

    @property
    def version(self) -> str:
        return self._version

    @property
    def href(self) -> str:
        return self._href

    def _process_manifests(self) -> Union[Generator[NASAManifest, None, None], NASAManifest, None]:
        if not (mf := self._data.get("items")):
            return None
        elif len(mf) != 1:
            return (NASAManifest(data) for data in mf)
        else:
            return NASAManifest(mf[0])

    @property
    def manifests(self) -> Union[Generator[NASAManifest, None, None], NASAManifest, None]:
        if self not in self._cache:
            self._cache[self] = self._process_manifests()
        return self._cache[self]

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "NASAManifestCollection":
        return cls(data)
