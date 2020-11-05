import datetime
from asyncio.events import AbstractEventLoop
from collections import namedtuple
from io import BytesIO
from typing import List, Tuple

import aiohttp

from ..decorators import check_pil_importable
from ..exceptions import VoyagerException
from .base import BaseResource

try:
    from PIL import Image
except ImportError:
    pass


__all__ = [
    'EPICResource',
]


_CC = namedtuple("Centroid Coordinates", ["lat", "lon"])
_DSCOVR = namedtuple("DSCOVR j2000 Position", ["x", "y", "z"])
_LUNAR = namedtuple("Lunar j2000 Position", ["x", "y", "z"])
_SUN = namedtuple("Sun j2000 Position", ["x", "y", "z"])
_AQ = namedtuple("Attitude Quaternions", ["q0", "q1", "q2", "q3"])


class EPICImage(object):
    __slots__ = [
        '_name',
        '_base',
        '_data',
        '_loop',
    ]
    _NAT = "https://epic.gsfc.nasa.gov/archive/natural/"
    _ENH = "https://epic.gsfc.nasa.gov/archive/enhanced/"

    def __init__(self, data: dict,
                 loop: AbstractEventLoop = None) -> None:
        self._name = data.get("identifier")
        self._base = (data.get("date")).split(" ", 1)[0].replace("-", "/")
        self._loop = loop
        self._data = data

    @property
    def normal_png(self) -> str:
        return self._NAT + self._base + f"/png/epic_1b_{self._name}.png"

    @property
    def normal_jpg(self) -> str:
        return self._NAT + self._base + f"/jpg/epic_1b_{self._name}.jpg"

    @property
    def normal_thumbnail(self) -> str:
        return self._NAT + self._base + f"/thumb/epic_1b_{self._name}.jpg"

    @property
    def enhanced_png(self) -> str:
        return self._ENH + self._base + f"/png/epic_RGB_{self._name}.png"

    @property
    def enhanced_jpg(self) -> str:
        return self._ENH + self._base + f"/jpg/epic_RGB_{self._name}.jpg"

    @property
    def enhanced_thumbnail(self) -> str:
        return self._ENH + self._base + f"/thumb/epic_RGB_{self._name}.jpg"

    async def _process_raw_image(self, url: str) -> Image:
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as resp:
                ret = await resp.raw()
        return Image.open(BytesIO(ret))

    @check_pil_importable
    async def get_image(self, format: str = "png", mode: str = "natural") -> Image:
        if not (fmt := format.lower()) in ['png', 'jpg', 'thumb']:
            raise VoyagerException(f"{format} is not a supported image format")
        elif not (md := mode.lower()) in ['natural', 'enhanced']:
            raise VoyagerException(f"{mode} is not a valid mode")
        else:
            url = getattr(self, f"{md}_{fmt}")

        if (req := f"{self}{fmt}{md}{url}") not in self._cache:
            self._cache[req] = self._process_raw_image(url)
        return self._cache[req]

    @check_pil_importable
    async def show(self, format: str = "png", mode: str = "natural") -> None:
        image = await self._loop.run_in_executor(
            None, self.get_image(format=format, mode=mode)
        )
        return await self._loop.run_in_executor(None, image.show())


class EPICResource(BaseResource):
    __slots__ = [
        '_identifier',
        '_caption',
        '_version',
        '_centroid_coordinates',
        '_dscovr_j2000_position',
        '_lunar_j2000_position',
        '_sun_j2000_position',
        '_attitude_quaternions',
        '_date',
        '_data',
    ]
    _cache = {}
    _nt_map = {
        'centroid_coordinates': _CC,
        'dscovr_j2000_position': _DSCOVR,
        'lunar_j2000_position': _LUNAR,
        'sun_j2000_position': _SUN,
        'attitude_quaternions': _AQ,
    }

    def __init__(self, data: dict,
                 loop: AbstractEventLoop = None) -> None:
        super(EPICResource, self).__init__(data, loop=loop)
        self._identifier = data.get("identifier")
        self._caption = data.get("caption")
        self._version = data.get("version")
        self._centroid_coordinates = data.get("centroid_coordinates")
        self._dscovr_j2000_position = data.get("discovr_j2000_position")
        self._lunar_j2000_position = data.get("lunar_j2000_position")
        self._sun_j2000_position = data.get("sun_j2000_position")
        self._attitude_quaternions = data.get("attitude_quaternions")
        self._date = data.get("date")
        self._data = data

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def id(self) -> str:
        return self.identifier

    @property
    def caption(self) -> str:
        return self._caption

    @property
    def version(self) -> str:
        return self._version

    def _process_coords(self, ct: str) -> namedtuple:
        return (self._nt_map[ct])(*(getattr(self, f"_{ct}")).values())

    @property
    def centroid_coords(self) -> Tuple[float, float]:
        if (cc := f"{self}cc") not in self._cache:
            self._cache[cc] = self._process_coords("centroid_coordinates")
        return self._cache[cc]

    @property
    def dscovr_pos(self) -> Tuple[float, float, float]:
        if (dp := f"{self}dp") not in self._cache:
            self._cache[dp] = self._process_coords("dscovr_j2000_position")
        return self._cache[dp]

    @property
    def lunar_pos(self) -> Tuple[float, float, float]:
        if (lp := f"{self}lp") not in self._cache:
            self._cache[lp] = self._process_coords("lunar_j2000_position")
        return self._cache[lp]

    @property
    def sun_pos(self) -> Tuple[float, float, float]:
        if (sp := f"{self}sp") not in self._cache:
            self._cache[sp] = self._process_coords("sun_j2000_position")
        return self._cache[sp]

    @property
    def attitude_quaternions(self) -> Tuple[float, float, float, float]:
        if (aq := f"{self}aq") not in self._cache:
            self._cache[aq] = self._process_coords("attitude_quaternions")
        return self._cache[aq]

    @property
    def aq(self) -> Tuple[float, float, float, float]:
        return self.attitude_quaternions

    @property
    def date(self) -> str:
        return self._date

    @property
    def coords(self) -> List[Tuple[float]]:
        return (
            self.centroid_coords,
            self.dscovr_pos,
            self.lunar_pos,
            self.sun_pos,
            self.attitude_quaternions,
        )

    @property
    def datetime(self) -> datetime.datetime:
        return datetime.datetime.strptime(self._date, "%Y-%m-%d %H:%M:%S")

    def _process_image(self) -> EPICImage:
        return EPICImage(self._data, loop=self._loop)

    @property
    def image(self) -> EPICImage:
        if (img := f"{self}img") not in self._cache:
            self._cache[img] = self._process_image()
        return self._cache[img]

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict,
                  loop: AbstractEventLoop = None) -> "EPICResource":
        return cls(data, loop=loop)
