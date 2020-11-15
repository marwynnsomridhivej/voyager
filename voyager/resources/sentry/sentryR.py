import datetime

from .sentrybase import SentryBase


class SentryDataR(SentryBase):
    __slots__ = [
        '_des',
        '_removed',
        '_data,'
    ]

    def __init__(self, data: dict) -> None:
        self._des = data.get("des")
        self._removed = data.get("removed")
        self._data = data

    @property
    def des(self) -> str:
        return self._des

    @property
    def removed(self) -> str:
        return self._removed

    @property
    def removed_dt(self) -> datetime.datetime:
        return datetime.datetime.strptime(self.removed, "%Y-%m-%d %H:%M")

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "SentryDataR":
        return cls(data)
