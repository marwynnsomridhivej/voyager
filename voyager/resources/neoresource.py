import datetime as dt
from asyncio.events import AbstractEventLoop
from collections import namedtuple
from typing import List, Union

from ..exceptions import ResourceException, VoyagerException
from .base import BaseResource

__all__ = [
    'NEOResource',
]


_Diameter = namedtuple("Diameter", ['min', 'max'])


class NEOLinks(object):
    __slots__ = [
        '_next',
        '_self',
        '_data',
    ]

    def __init__(self, links: dict) -> None:
        self._next = links.get("next")
        self._self = links.get("self")
        self._data = links

    def __hash__(self) -> int:
        return hash(self._links)

    def __len__(self) -> int:
        return len(self._links)

    @property
    def next(self) -> str:
        return self._next

    @property
    def self(self) -> str:
        return self._self

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "NEOLinks":
        return cls(data)


class NEOPage(object):
    __slots__ = [
        '_size',
        '_total_elements',
        '_total_pages',
        '_number',
        '_data',
    ]

    def __init__(self, page: dict) -> None:
        self._size = page.get("size")
        self._total_elements = page.get("total_elements")
        self._total_pages = page.get("total_pages")
        self._number = page.get("number")
        self._data = page

    def __hash__(self) -> int:
        return hash(self._page)

    def __len__(self) -> int:
        return self._size or 0

    @property
    def size(self) -> Union[int, None]:
        return self._size

    @property
    def total_elements(self) -> Union[int, None]:
        return self._total_elements

    @property
    def total_pages(self) -> Union[int, None]:
        return self._total_pages

    @property
    def number(self) -> Union[int, None]:
        return self._number

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "NEOPage":
        return cls(data)


class NEOOrbitClass(object):
    __slots__ = [
        '_type',
        '_description',
        '_range',
        '_data',
    ]

    def __init__(self, data: dict) -> None:
        self._type = data.get("orbit_class_type")
        self._description = data.get("orbit_class_description")
        self._range = data.get("orbit_class_range")
        self._data = data

    @property
    def type(self) -> str:
        return self._type

    @property
    def description(self) -> str:
        return self._description

    @property
    def range(self) -> str:
        return self._range

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "NEOOrbitClass":
        return cls(data)


class NEOOrbitalData(object):
    __slots__ = [
        '_id',
        '_determination_date',
        '_first_observe_date',
        '_last_observe_date',
        '_data_arc_days',
        '_observations_used',
        '_uncertainty',
        '_min_orbit_intersection',
        '_jupiter_tisserand_invariant',
        '_epoch_osculation',
        '_eccentricity',
        '_semi_major_axis',
        '_inclination',
        '_ascending_node_longitude',
        '_orbital_period',
        '_perihelion_distance',
        '_perihelion_argument',
        '_aphelion_distance',
        '_perihelion_time',
        '_mean_anomaly',
        '_mean_motion',
        '_equinox',
        '_orbit_class',
        '_data'
    ]

    def __init__(self, data: dict) -> None:
        self._id = data.get("orbit_id")
        self._determination_date = data.get("orbit_determination_date")
        self._first_observe_date = data.get("first_observation_date")
        self._last_observe_date = data.get("last_observation_date")
        self._data_arc_days = data.get("data_arc_in_days")
        self._observations_used = data.get("observations_used")
        self._uncertainty = data.get("orbit_uncertainty")
        self._min_orbit_intersection = data.get("minimum_orbit_intersection")
        self._jupiter_tisserand_invariant = data.get("jupiter_tisserand_invariant")
        self._epoch_osculation = data.get("epoch_osculation")
        self._eccentricity = data.get("eccentricity")
        self._semi_major_axis = data.get("semi_major_axis")
        self._inclination = data.get("inclination")
        self._ascending_node_longitude = data.get("ascending_node_longitude")
        self._orbital_period = data.get("orbital_period")
        self._perihelion_distance = data.get("perihelion_distance")
        self._perihelion_argument = data.get("perihelion_argument")
        self._aphelion_distance = data.get("aphelion_distance")
        self._perihelion_time = data.get("perihelion_time")
        self._mean_anomaly = data.get("mean_anomaly")
        self._mean_motion = data.get("mean_motion")
        self._equinox = data.get("equinox")
        self._orbit_class = NEOOrbitClass(data.get("orbit_class"))
        self._data = self.to_dict

    @property
    def id(self) -> int:
        return int(self._id)

    @property
    def determination_date(self) -> str:
        return self._determination_date

    @property
    def determination_datetime(self) -> dt.datetime:
        return dt.datetime.strptime(
            self._determination_date,
            "%Y-%m-%d %H:%M:%S")

    @property
    def first_observation_date(self) -> str:
        return self._first_observe_date

    @property
    def first_observation_datetime(self) -> dt.datetime:
        return dt.datetime.strptime(
            self._first_observe_date,
            "%Y-%m-%d"
        )

    @property
    def last_observation_date(self) -> str:
        return self._last_observe_date

    @property
    def last_observation_datetime(self) -> dt.datetime:
        return dt.datetime.strptime(
            self._last_observe_date,
            "%Y-%m-%d"
        )

    @property
    def data_arc_in_days(self) -> int:
        return self._data_arc_days

    @property
    def observations_used(self) -> int:
        return self._observations_used

    @property
    def uncertainty(self) -> int:
        return int(self._uncertainty)

    @property
    def minumum_intersection(self) -> float:
        return float(self._min_orbit_intersection)

    @property
    def jupiter_tisserand_invariant(self) -> float:
        return float(self._jupiter_tisserand_invariant)

    @property
    def epoch_osculation(self) -> float:
        return float(self._epoch_osculation)

    @property
    def eccentricity(self) -> float:
        return float(self._eccentricity)

    @property
    def semi_major_axis(self) -> float:
        return float(self._semi_major_axis)

    @property
    def inclination(self) -> float:
        return float(self._inclination)

    @property
    def ascending_node_longitude(self) -> float:
        return float(self._ascending_node_longitude)

    @property
    def period(self) -> float:
        return float(self._orbital_period)

    @property
    def perihelion_distance(self) -> float:
        return float(self._perihelion_distance)

    @property
    def perihelion_argument(self) -> float:
        return float(self._perihelion_argument)

    @property
    def aphelion_distance(self) -> float:
        return float(self._aphelion_distance)

    @property
    def perihelion_time(self) -> float:
        return float(self._perihelion_time)

    @property
    def mean_anomaly(self) -> float:
        return float(self._mean_anomaly)

    @property
    def mean_motion(self) -> float:
        return float(self._mean_motion)

    @property
    def equinox(self) -> str:
        return self._equinox

    @property
    def orbit_class(self) -> NEOOrbitClass:
        return self._orbit_class

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "NEOOrbitalData":
        return cls(data)


class NEOCloseApproachData(object):
    __slots__ = [
        '_date',
        '_fulldate',
        '_epoch',
        '_relvel',
        '_missdist',
        '_orbiting_body',
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict) -> None:
        self._date = data.get("close_approach_date")
        self._fulldate = data.get("close_approach_date_full")
        self._epoch = data.get("epoch_date_close_approach")
        self._relvel = data.get("relative_velocity")
        self._missdist = data.get("miss_distance")
        self._orbiting_body = data.get("orbiting_body")
        self._data = data

    @property
    def shortdate(self) -> str:
        return self._date

    def _process_datetime(self, type: str) -> dt.datetime:
        if type == "short":
            return dt.datetime.strptime(self._date, "%Y-%m-%d")
        elif type == "full":
            return dt.datetime.strptime(self._fulldate, "%Y-%b-%d %H:%M")
        else:
            raise VoyagerException("Invalid type passed for datetime conversion")

    @property
    def shortdatetime(self) -> dt.datetime:
        if (name := f"{self}short") not in self._cache:
            self._cache[name] = self._process_datetime("short")
        return self._cache[name]

    @property
    def date(self) -> str:
        return self._fulldate

    @property
    def datetime(self) -> dt.datetime:
        if (name := f"{self}full") not in self._cache:
            self._cache[name] = self._process_datetime("full")
        return self._cache[name]

    @property
    def epoch(self) -> dt.datetime:
        return self._epoch  # TODO: Come back here to give appropriate return

    @property
    def kps(self) -> float:
        return float(self._relvel.get("kilometers_per_second"))

    @property
    def kph(self) -> float:
        return float(self._relvel.get("kilometers_per_hour"))

    @property
    def mph(self) -> float:
        return float(self._relvel.get("miles_per_hour"))

    @property
    def astronomical_miss_distance(self) -> float:
        return float(self._missdist.get("astronomical"))

    @property
    def lunar_miss_distance(self) -> float:
        return float(self._missdist.get("lunar"))

    @property
    def kilometer_miss_distance(self) -> float:
        return float(self._missdist.get("kilometers"))

    @property
    def mile_miss_distance(self) -> float:
        return float(self._missdist.get("miles"))

    @property
    def orbiting_body(self) -> str:
        return self._orbiting_body

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "NEOCloseApproachData":
        return cls(data)


class NEOObject(object):
    __slots__ = [
        '_links',
        '_id',
        '_neo_reference_id',
        '_name',
        '_designation',
        '_jpl_url',
        '_abs_mag_h',
        '_diameter',
        '_hazardous',
        '_orbital_data',
        '_sentry',
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict) -> None:
        self._links = data.get("links")
        self._id = data.get("id")
        self._neo_reference_id = data.get("neo_reference_id")
        self._name = data.get("name")
        self._designation = data.get("designation")
        self._jpl_url = data.get("nasa_jpl_url")
        self._abs_mag_h = data.get("absolute_magnitude_h")
        self._diameter = data.get("estimated_diameter")  # TODO: Implement methods
        self._hazardous = data.get("is_potentially_hazardous_asteroid")
        self._orbital_data = NEOOrbitalData(data.get("orbital_data"))
        self._sentry = data.get("is_sentry_object")
        self._data = data

    @property
    def links(self) -> NEOLinks:
        return NEOLinks(self._links)

    @property
    def self(self) -> str:
        return self.links.self

    @property
    def id(self) -> int:
        return int(self._id)

    @property
    def neo_reference_id(self) -> int:
        return int(self._neo_reference_id)

    @property
    def name(self) -> str:
        return self._name

    @property
    def designation(self) -> str:  # TODO: Check return type
        return self._designation

    @property
    def jpl_url(self) -> str:
        return self._jpl_url

    @property
    def absolute_magnitude_h(self) -> int:
        return self._abs_mag_h

    @property
    def kilometer_diameter(self) -> _Diameter:
        diameter = self._diameter.get("kilometers")
        return _Diameter(diameter.get("min"), diameter.get("max"))

    @property
    def meter_diameter(self) -> _Diameter:
        diameter = self._diameter.get("meters")
        return _Diameter(diameter.get("min"), diameter.get("max"))

    @property
    def mile_diameter(self) -> _Diameter:
        diameter = self._diameter.get("miles")
        return _Diameter(diameter.get("min"), diameter.get("max"))

    @property
    def feet_diameter(self) -> _Diameter:
        diameter = self._diameter.get("feet")
        return _Diameter(diameter.get("min"), diameter.get("max"))

    @property
    def maybe_hazardous(self) -> bool:
        return self._hazardous

    def _process_close_approach(self) -> Union[NEOCloseApproachData, List[NEOCloseApproachData], None]:
        if len((cad := self._data.get("close_approach_data"))) != 1:
            return [NEOCloseApproachData(data) for data in cad]
        elif not cad:
            return None
        elif len(cad) == 1:
            return NEOCloseApproachData(cad)
        else:
            raise ResourceException("Invalid resource returned in the request")

    @property
    def close_approach(self) -> Union[NEOCloseApproachData, List[NEOCloseApproachData], None]:
        if self not in self._cache:
            self._cache[self] = self._process_close_approach()
        return self._cache[self]

    @property
    def orbit(self) -> NEOOrbitalData:
        return self._orbital_data

    @property
    def is_sentry_object(self) -> bool:
        return self._sentry

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "NEOObject":
        return cls(data)


class NEOResource(BaseResource):
    __slots__ = [
        '_links',
        '_page'
        '_element_count',
        'search_type',
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict,
                 loop: AbstractEventLoop = None) -> None:
        super(NEOResource, self).__init__(data, loop=loop)
        self._links = NEOLinks(data.get("links", {}))
        self._page = NEOPage(data.get("page", {}))
        self._element_count = data.get("element_count")
        self._search_type = data.get("search_type")
        self._data = data

    def __iter__(self):
        self.__index = 0
        return self.neo

    def __next__(self):
        try:
            ret = self.neo[self.__index]
            self.__index += 1
            return ret
        except IndexError:
            raise StopIteration

    @property
    def links(self) -> NEOLinks:
        return self._links

    @property
    def page(self) -> NEOPage:
        return self._page

    def _process_neo(self) -> Union[List[NEOObject], List[List[NEOObject]], NEOObject, None]:
        if self._search_type == "feed-none" or self._search_type == "browse":
            return [
                NEOObject(data for data in self._data.get("near_earth_objects"))
            ] or None
        elif self._search_type == "feed-query":
            return [
                [NEOObject(data) for data in subdict]
                for subdict in self._data.get("near_earth_objects")
            ] or None
        elif self._search_type == "lookup":
            return NEOObject(self._data)
        else:
            raise ResourceException("Invalid resource returned in the request")

    @property
    def neo(self) -> Union[List[NEOObject], List[List[NEOObject]], NEOObject, None]:
        if self not in self._cache:
            self._cache[self] = self._process_neo()
        return self._cache[self]

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict,
                  loop: AbstractEventLoop = None) -> "NEOResource":
        return cls(data, loop=loop)
