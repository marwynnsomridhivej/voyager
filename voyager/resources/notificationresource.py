from asyncio.events import AbstractEventLoop
from .base import BaseResource


__all__ = [
    'NotificationResource',
]


class NotificationResource(BaseResource):
    __slots__ = [
        '_type',
        '_id',
        '_url',
        '_timestamp',
        '_content',
    ]

    def __init__(self, data: dict,
                 loop: AbstractEventLoop = None) -> None:
        super(NotificationResource, self).__init__(data, loop=loop)
        self._type = data.get("messageType")
        self._id = data.get("messageID")
        self._url = data.get("messageURL")
        self._timestamp = data.get("messageIssueTime")
        self._content = data.get("messageBody")

    @property
    def type(self) -> str:
        return self._type

    @property
    def message_type(self) -> str:
        return self.type

    @property
    def id(self) -> str:
        return self._id

    @property
    def message_id(self) -> str:
        return self.id

    @property
    def url(self) -> str:
        return self._url

    @property
    def message_url(self) -> str:
        return self.url

    @property
    def timestamp(self) -> str:  # TODO: Implement datetime.datetime
        return self._timestamp

    @property
    def message_issue_time(self) -> str:
        return self.timestamp

    @property
    def content(self) -> str:
        return self._content

    @property
    def message_body(self) -> str:
        return self.content

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict,
                  loop: AbstractEventLoop = None) -> "NotificationResource":
        return cls(data, loop=loop)
