import datetime
from asyncio.events import AbstractEventLoop
from typing import Any, Generator, List, Union

from .base import BaseResource


__all__ = [
    'TechportResource',
]


class TechportTechnologyArea(object):
    __slots__ = [
        '_id',
        '_code',
        '_title',
        '_priority',
        '_data',
    ]

    def __init__(self, data: dict) -> None:
        self._id = data.get("id")
        self._code = data.get("code")
        self._title = data.get("title")
        self._priority = data.get("priority")
        self._data = data

    @property
    def id(self) -> int:
        return self._id

    @property
    def code(self) -> str:
        return self._code

    @property
    def title(self) -> str:
        return self._title

    @property
    def priority(self) -> Union[Any, None]:
        return self._priority

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "TechportTechnologyArea":
        return cls(data)


class TechportFile(object):
    __slots__ = [
        '_id',
        '_url',
        '_size',
        '_data',
    ]

    def __init__(self, data: dict) -> None:
        self._id = data.get("id")
        self._url = data.get("url")
        self._size = data.get("size")  # Filesize in bytes
        self._data = data

    @property
    def id(self) -> int:
        return self._id

    @property
    def url(self) -> str:
        return self._url

    @property
    def size(self) -> int:
        return self._size

    @property
    def kb(self) -> float:
        return self._size / 1024

    @property
    def mb(self) -> float:
        return self.kb / 1024

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "TechportFile":
        return cls(data)


class TechportLibraryItem(object):
    __slots__ = [
        '_id',
        '_title',
        '_type',
        '_description',
        '_external_url',
        '_published_by',
        '_published_date',
        '_data'
    ]
    _cache = {}

    def __init__(self, data: dict) -> None:
        self._id = data.get("id")
        self._title = data.get("title")
        self._type = data.get("type")
        self._description = data.get("description")
        self._external_url = data.get("externalUrl")
        self._published_by = data.get("publishedBy")
        self._published_date = data.get("publishedDate")
        self._data = data

    def __iter__(self):
        return self

    def __next__(self):
        for fl in self.files:
            yield fl

    @property
    def id(self) -> int:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def type(self) -> str:
        return self._type

    @property
    def description(self) -> str:
        return self._description

    @property
    def external_url(self) -> Union[str, None]:
        return self._external_url

    @property
    def url(self) -> Union[str, None]:
        return self.external_url

    @property
    def published_by(self) -> Union[str, None]:
        return self._published_by

    @property
    def published_date(self) -> Union[str, None]:
        return self._published_date

    @property
    def published_datetime(self) -> Union[datetime.datetime, None]:
        if not self._published_date:
            return None
        return datetime.datetime.strptime(self._published_date, "")  # TODO: Find formatting

    def _process_files(self) -> Union[Generator[TechportFile], TechportFile, None]:
        if not (fl := self._data.get("files")):
            return None
        elif len(fl) != 1:
            for data in fl:
                yield TechportFile(data)
        else:
            return TechportFile(fl[0])

    @property
    def files(self) -> Union[Generator[TechportFile], TechportFile, None]:
        if self not in self._cache:
            self._cache[self] = self._process_files()
        return self._cache[self]

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "TechportLibraryItem":
        return cls(data)


class TechportOrganisation(object):
    __slots__ = [
        '_name',
        '_type',
        '_acronym',
        '_city',
        '_state',
        '_country',
        '_data',
    ]

    def __init__(self, data: dict) -> None:
        self._name = data.get("name")
        self._type = data.get("type")
        self._acronym = data.get("acronym")
        self._city = data.get("city")
        self._state = data.get("state")
        self._country = data.get("country")
        self._data = data.get("data")

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> str:
        return self._type

    @property
    def acronym(self) -> str:
        return self._acronym

    @property
    def city(self) -> str:
        return self._city

    @property
    def state(self) -> str:
        return self._state

    @property
    def country(self) -> str:
        return self._country

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "TechportOrganisation":
        return cls(data)


class TechportResource(BaseResource):
    __slots__ = [
        '_id',
        '_last_updated',
        '_title',
        '_status',
        '_start_date',
        '_end_date',
        '_description',
        '_benefits',
        '_tech_mat_start',
        '_tech_mat_current',
        '_tech_mat_end',
        '_responsible_prog',
        '_responsible_mdo',
        '_locations',
        '_prog_directors',
        '_prog_managers',
        '_proj_managers',
        '_prin_investigator',
        '_closeout_docs',
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict,
                 loop: AbstractEventLoop = None) -> None:
        super(TechportResource, self).__init__(data, loop=loop)
        self._id = data.get("id")
        self._last_updated = data.get("lastUpdated")
        self._title = data.get("title")
        self._status = data.get("status")
        self._start_date = data.get("startDate")
        self._end_date = data.get("endDate")
        self._description = data.get("description")
        self._benefits = data.get("benefits")
        self._tech_mat_start = data.get("technologyMaturityStart")
        self._tech_mat_current = data.get("technologyMaturityCurrent")
        self._tech_mat_end = data.get("technologyMaturityEnd")
        self._responsible_prog = data.get("responsibleProgram")
        self._responsible_mdo = data.get("responsibleMissionDirectorateOrOffice")
        self._locations = data.get("workLocations")
        self._prog_directors = data.get("programDirectors")
        self._prog_managers = data.get("programManagers")
        self._proj_managers = data.get("projectManagers")
        self._prin_investigator = data.get("principleInvestigators")
        self._closeout_docs = data.get("closeoutDocuments")
        self._data = data

    @property
    def id(self) -> int:
        return self._id

    @property
    def last_updated(self) -> str:
        return self._last_updated

    @property
    def last_updated_datetime(self) -> datetime.datetime:
        return datetime.datetime.strptime(self._last_updated, "%Y-%m-%d")

    @property
    def title(self) -> str:
        return self._title

    @property
    def status(self) -> str:
        return self._status

    @property
    def start_date(self) -> str:
        return self._start_date

    @property
    def start_datetime(self) -> datetime.datetime:
        return datetime.datetime.strptime(self._start_date, "%b %Y")

    @property
    def end_date(self) -> str:
        return self._end_date

    @property
    def end_datetime(self) -> datetime.datetime:
        return datetime.datetime.strptime(self._end_date, "%b %Y")

    @property
    def description(self) -> str:
        return self._description

    @property
    def benefits(self) -> str:
        return self._benefits

    @property
    def tech_mat_start(self) -> int:
        return int(self._tech_mat_start)

    @property
    def tech_mat_current(self) -> int:
        return int(self._tech_mat_current)

    @property
    def tech_mat_end(self) -> Union[int, None]:
        if not self._tech_mat_end:
            return None
        return int(self._tech_mat_end)

    @property
    def responsible_program(self) -> str:
        return self._responsible_prog

    @property
    def responsible_mission_directorate_or_office(self) -> str:
        return self._responsible_mdo

    @property
    def responsible_mdo(self) -> str:
        return self.responsible_mission_directorate_or_office

    @property
    def work_locations(self) -> List[str]:
        return self._locations

    @property
    def program_directors(self) -> List[str]:
        return self._prog_directors

    @property
    def program_managers(self) -> List[str]:
        return self._prog_managers

    @property
    def project_managers(self) -> List[str]:
        return self._proj_managers

    @property
    def principal_investigators(self) -> List[str]:
        return self._prin_investigator

    def _process_library(self) -> Union[Generator[TechportLibraryItem], TechportLibraryItem, None]:
        if not (li := self._data.get("libraryItems")):
            return None
        elif len(li) != 1:
            for data in li:
                yield TechportLibraryItem(data)
        else:
            return TechportLibraryItem(li[0])

    @property
    def library_items(self) -> Union[Generator[TechportLibraryItem], TechportLibraryItem, None]:
        if (li := f"{self}library") not in self._cache:
            self._cache[li] = self._process_library()
        return self._cache[li]

    @property
    def closeout_documents(self) -> Union[List[str], None]:
        return self._closeout_docs

    @property
    def closeout_docs(self) -> Union[List[str], None]:
        return self.closeout_docs

    def _process_orgs(self) -> Union[Generator[TechportOrganisation], TechportOrganisation, None]:
        if not (org := self._data.get("supportingOrganizations")):
            return None
        elif len(org) != 1:
            for data in org:
                yield TechportOrganisation(data)
        else:
            return TechportOrganisation(org[0])

    @property
    def supporting_organisations(self) -> Union[Generator[TechportOrganisation], TechportOrganisation, None]:
        if not (org := f"{self}organisation") in self._cache:
            self._cache[org] = self._process_orgs()
        return self._cache[org]

    @property
    def supporting_organizations(self) -> Union[Generator[TechportOrganisation], TechportOrganisation, None]:
        return self.supporting_organisations

    def _process_tas(self, ta_type: str) -> Union[Generator[TechportTechnologyArea], TechportTechnologyArea, None]:
        if not (ta := self._data.get(ta_type)):
            return None
        elif len(ta) != 1:
            for data in ta:
                yield TechportTechnologyArea(data)
        else:
            return TechportTechnologyArea(ta[0])

    @property
    def primary_tas(self) -> Union[Generator[TechportTechnologyArea], TechportTechnologyArea, None]:
        if (ta := f"{self}primarytas") not in self._cache:
            self._cache[ta] = self._process_tas("primaryTas")
        return self._cache[ta]

    @property
    def additional_tas(self) -> Union[Generator[TechportTechnologyArea], TechportTechnologyArea, None]:
        if (ta := f"{self}additionaltas") not in self._cache:
            self._cache[ta] = self._process_tas("additionalTas")
        return self._cache[ta]

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict,
                  loop: AbstractEventLoop = None):
        return cls(data, loop=loop)
