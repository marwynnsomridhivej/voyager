import datetime
from typing import Generator, Union


class GenelabStudyFile(object):
    __slots__ = [
        '_filename',
        '_remote_url',
        '_filesize',
        '_date_created',
        '_data',
    ]

    def __init__(self, data: dict) -> None:
        self._filename = data.get("file_name")
        self._remote_url = data.get("remote_url")
        self._filesize = data.get("file_size")
        self._date_created = data.get("date_created")
        self._data = data

    @property
    def filename(self) -> str:
        return self._filename

    @property
    def extension(self) -> str:
        return self.filename.split(".")[-1]

    @property
    def remote_url(self) -> str:
        return "https://genelab-data.ndc.nasa.gov" + self._remote_url

    @property
    def filesize(self) -> int:
        return self._filesize

    @property
    def date_created(self) -> int:
        return self._date_created

    @property
    def datetime_created(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self.date_created)

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "GenelabStudyFile":
        return cls(data)


class GenelabStudy(object):
    __slots__ = [
        '_name',
        '_data',
    ]
    _cache = {}

    def __init__(self, name: str, data: dict) -> None:
        self._name = name
        self._data = data

    def __iter__(self):
        return self

    def __next__(self):
        for fl in self.files:
            yield fl

    @property
    def name(self) -> str:
        return self._name

    def _process_files(self) -> Union[Generator[GenelabStudyFile, None, None], GenelabStudyFile, None]:
        if not (fl := self._data.get("study_files")):
            return None
        elif len(fl) != 1:
            return (GenelabStudyFile(data) for data in fl)
        else:
            return GenelabStudyFile(fl[0])

    @property
    def files(self) -> Union[Generator[GenelabStudyFile, None, None], GenelabStudyFile, None]:
        if self not in self._cache:
            self._cache[self] = self._process_files()
        return self._cache[self]

    @property
    def to_dict(self) -> dict:
        if (dt := f"{self}dict") not in self._cache:
            self._cache[dt] = {
                "name": self.name,
                "study_files": self._data.get("study_files")
            }
        return self._cache[dt]

    @classmethod
    def from_dict(cls, data: dict) -> "GenelabStudy":
        return cls(data.get("name"), {key: value for key, value in data.items() if key != "name"})
