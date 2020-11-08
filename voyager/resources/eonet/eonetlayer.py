from typing import List


class EONETLayer(object):
    __slots__ = [
        '_name',
        '_service_url',
        '_service_type_id',
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict) -> None:
        self._name = data.get("name")
        self._service_url = data.get("serviceUrl")
        self._service_type_id = data.get("serviceTypeId")
        self._data = data

    @property
    def name(self) -> str:
        return self._name

    @property
    def service_url(self) -> str:
        return self._service_url

    @property
    def url(self) -> str:
        return self.service_url

    @property
    def service_type_id(self) -> str:
        return self._service_type_id

    @property
    def type_id(self) -> str:
        return self.service_type_id

    @property
    def parameters(self) -> List[dict]:
        if self not in self._cache:
            self._cache[self] = self._data.get("parameters")
        return self._cache[self]

    @property
    def params(self) -> List[dict]:
        return self.parameters

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "EONETLayer":
        return cls(data)
